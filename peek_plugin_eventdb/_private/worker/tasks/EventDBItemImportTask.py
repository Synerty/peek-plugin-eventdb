import logging
from datetime import datetime
from typing import List

import pytz
from sqlalchemy.sql.expression import select
from txcelery.defer import DeferrableTask

from peek_plugin_base.storage.StorageUtil import makeCoreValuesSubqueryCondition
from peek_plugin_base.worker import CeleryDbConn
from peek_plugin_eventdb._private.storage.EventDBItem import EventDBItem
from peek_plugin_eventdb._private.storage.EventDBModelSet import getOrCreateEventDBModelSet
from peek_plugin_base.worker.CeleryApp import celeryApp
from peek_plugin_eventdb.tuples.ImportEventDBItemTuple import ImportEventDBItemTuple

logger = logging.getLogger(__name__)


@DeferrableTask
@celeryApp.task(bind=True)
def importEventDBItems(self, modelSetKey: str,
                      newItems: List[ImportEventDBItemTuple]) -> List[str]:
    """ Compile Grids Task

    :param self: A celery reference to this task
    :param modelSetKey: The model set name
    :param newItems: The list of new items
    :returns: A list of grid keys that have been updated.
    """

    startTime = datetime.now(pytz.utc)

    session = CeleryDbConn.getDbSession()
    engine = CeleryDbConn.getDbEngine()
    conn = engine.connect()
    transaction = conn.begin()

    eventdbTable = EventDBItem.__table__
    try:

        eventdbModelSet = getOrCreateEventDBModelSet(session, modelSetKey)

        # This will remove duplicates
        itemsByKey = {i.key: i for i in newItems}

        allKeys = list(itemsByKey)
        existingKeys = set()

        # Query for existing keys, in 1000 chinks
        chunkSize = 1000
        offset = 0
        while True:
            chunk = allKeys[offset:offset + chunkSize]
            if not chunk:
                break
            offset += chunkSize
            stmt = (select([eventdbTable.c.key])
                    .where(eventdbTable.c.modelSetId == eventdbModelSet.id)
            .where(makeCoreValuesSubqueryCondition(
                engine, eventdbTable.c.key, chunk
            ))
            )

            result = conn.execute(stmt)

            existingKeys.update([o[0] for o in result.fetchall()])

        inserts = []
        newKeys = []

        for newItem in itemsByKey.values():
            if newItem.key in existingKeys:
                continue

            inserts.append(dict(
                modelSetId=eventdbModelSet.id,
                key=newItem.key,
                dataType=newItem.dataType,
                rawValue=newItem.rawValue,
                displayValue=newItem.displayValue,
                importHash=newItem.importHash
            ))

            newKeys.append(newItem.key)

        if not inserts:
            return []

        conn.execute(EventDBItem.__table__.insert(), inserts)

        transaction.commit()
        logger.info("Inserted %s EventDBItems, %s already existed, in %s",
                    len(inserts), len(existingKeys), (datetime.now(pytz.utc) - startTime))

        return newKeys

    except Exception as e:
        transaction.rollback()
        logger.debug("Task failed, but it will retry. %s", e)
        raise self.retry(exc=e, countdown=10)

    finally:
        conn.close()
        session.close()

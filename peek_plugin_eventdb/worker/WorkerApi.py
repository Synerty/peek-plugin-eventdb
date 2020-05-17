from typing import List, Dict

from sqlalchemy import select

from peek_plugin_base.storage.StorageUtil import makeCoreValuesSubqueryCondition, \
    makeOrmValuesSubqueryCondition
from peek_plugin_eventdb._private.storage.EventDBItem import EventDBItem
from peek_plugin_eventdb._private.storage.EventDBModelSet import EventDBModelSet, \
    getOrCreateEventDBModelSet
from peek_plugin_eventdb.tuples.EventDBDisplayValueTuple import EventDBDisplayValueTuple
from peek_plugin_eventdb.tuples.EventDBRawValueTuple import EventDBRawValueTuple


class WorkerApi:
    """ Worker Api

    This class allows other classes to work with the EventDB plugin on the
    worker service.

    """
    _FETCH_SIZE = 5000

    @classmethod
    def getEventDBDisplayValues(cls,
                               ormSession,
                               modelSetKey: str,
                               eventdbKeys: List[str]
                               ) -> List[EventDBDisplayValueTuple]:
        """ Get Live DB Display Values

        Return an array of items representing the display values from the EventDB.

        :param ormSession: The SQLAlchemy orm session from the calling code.
        :param modelSetKey: The name of the model set to get the keys for
        :param eventdbKeys: An array of EventDB Keys.

        :returns: An array of tuples.
        """
        if not eventdbKeys:
            return []

        eventdbModelSet = getOrCreateEventDBModelSet(ormSession, modelSetKey)

        eventdbKeys = set(eventdbKeys)  # Remove duplicates if any exist.
        qry = (
            ormSession.query(EventDBItem)
                .filter(EventDBItem.modelSetId == eventdbModelSet.id)
                .filter(makeOrmValuesSubqueryCondition(
                ormSession, EventDBItem.key, list(eventdbKeys)
            ))
                .yield_per(cls._FETCH_SIZE)
        )

        results = []

        for item in qry:
            results.append(
                EventDBDisplayValueTuple(key=item.key,
                                        displayValue=item.displayValue,
                                        rawValue=item.rawValue,
                                        dataType=item.dataType)
            )

        return results


import logging
from datetime import datetime
from typing import Optional, List, Tuple

from peek_plugin_eventdb._private.storage.EventDBModelSetTable import EventDBModelSetTable
from peek_plugin_eventdb.tuples import loadPublicTuples
from peek_plugin_eventdb.tuples.EventDBEventTuple import EventDBEventTuple
from sqlalchemy.dialects import postgresql
from vortex.Payload import Payload
from vortex.Tuple import TUPLE_TYPES_BY_NAME

logger = logging.getLogger(__name__)


class EventDBImportInPgTask:
    """ EventDB Import In PostGreSQL Tasks

    The methods in this class are run in the databases plpython extension.
    """

    @classmethod
    def importEvents(cls, plpy,
                     modelSetKey: str,
                     eventsEncodedPayload: bytes
                     ) -> Tuple[int, Optional[datetime], Optional[datetime]]:

        if EventDBEventTuple.tupleName() not in TUPLE_TYPES_BY_NAME:
            loadPublicTuples()

        # Reconstruct the data
        events = Payload().fromEncodedPayload(eventsEncodedPayload).tuples
        if not events:
            return 0, None, None

        dates = [e.dateTime for e in events]
        maxDate = max(dates)
        minDate = min(dates)

        # Get the model set id
        modelSetId = cls._getModelSetId(plpy, modelSetKey, createIfMissing=True)

        # Now insert the events
        cls._loadEvents(plpy, events, modelSetId)

        return len(events), maxDate, minDate

    @classmethod
    def deleteEvents(cls, plpy,
                     modelSetKey: str,
                     eventKeys: List[str]) -> int:

        # Get the model set id
        modelSetId = cls._getModelSetId(plpy, modelSetKey, createIfMissing=False)
        if modelSetId is None:
            plpy.debug("ModelSet with key %s doesn't exist" % modelSetKey)
            return 0

        # Now insert the events
        cls._deleteEvents(plpy, modelSetId, eventKeys)

        return len(eventKeys)

    @classmethod
    def _getModelSetId(cls, plpy, modelSetKey, createIfMissing) -> Optional[int]:
        msTbl = EventDBModelSetTable.__table__
        qryModelSetSql = str(msTbl
                             .select()
                             .where(msTbl.c.key == modelSetKey)
                             .compile(dialect=postgresql.dialect(),
                                      compile_kwargs={"literal_binds": True}))

        while True:
            rows = plpy.execute(qryModelSetSql, 1)
            if len(rows):
                return rows[0]["id"]

            if not createIfMissing:
                return None

            plpy.execute('''INSERT INTO pl_eventdb."EventDBModelSet"( key, name)
                            VALUES ('%s', '%s')''' % (modelSetKey, modelSetKey))

    @classmethod
    def _loadEvents(cls, plpy, events, modelSetId: int):
        keys = list(set([e.key for e in events if e.key]))
        if keys:
            cls._deleteEvents(plpy, modelSetId, keys)

        plan = plpy.prepare('''INSERT INTO pl_eventdb."EventDBEvent"
                                ("dateTime", "key", "modelSetId", value)
                                VALUES ($1, $2, $3, $4);''',
                            ["timestamp", "text", "integer", "jsonb"])
        for event in events:
            plpy.execute(plan, [event.dateTime, event.key, modelSetId, event.value])

    @classmethod
    def _deleteEvents(cls, plpy, modelSetId: int, eventKeys: List[str]):
        sql = '''DELETE FROM pl_eventdb."EventDBEvent"
                 WHERE key in (%s)
                    AND "modelSetId" = %s;'''
        sql %= (', '.join("'%s'" % k for k in eventKeys), modelSetId)
        plpy.execute(sql)

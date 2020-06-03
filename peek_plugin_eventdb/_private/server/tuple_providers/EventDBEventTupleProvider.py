import logging
from datetime import datetime

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_plugin_base.storage.RunPyInPg import runPyInPg
from peek_plugin_eventdb.tuples.EventDBEventTuple import EventDBEventTuple
from twisted.internet.defer import Deferred, inlineCallbacks
from vortex.Payload import Payload
from vortex.SerialiseUtil import ISO8601
from vortex.Tuple import addTupleType, Tuple, TupleField
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

logger = logging.getLogger(__name__)



class EventDBEventTupleProvider(TuplesProviderABC):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    @inlineCallbacks
    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> Deferred:
        return (yield runPyInPg(logger,
                                self._dbSessionCreator,
                                self._loadInPg,
                                filt=filt,
                                tupleSelector=tupleSelector)).encode()

    @classmethod
    def _loadInPg(cls, plpy, filt: dict, tupleSelector:TupleSelector):
        selector = tupleSelector.selector
        modelSetKey = selector.get('modelSetKey')
        criteria = selector.get('criteria', [])
        newestDateTime = selector.get('newestDateTime')
        oldestDateTime = selector.get('oldestDateTime')

        if not modelSetKey:
            raise Exception("modelSetKey is None")

        # Load in the ModelSet ID
        sql = """
            SELECT id FROM pl_eventdb."EventDBModelSet" where key = '%s'
            """ % modelSetKey

        rows = plpy.execute(sql, 1)
        if not len(rows):
            raise Exception("ModelSet with key %s not found" % modelSetKey)

        modelSetId = rows[0]["id"]

        # Create the basic SQL
        sql = """
            SELECT "dateTime", key, value
            FROM pl_eventdb."EventDBEvent"
            WHERE "modelSetId" = %s """ % modelSetId

        # Add in the date time criteria
        if newestDateTime:
            sql += """ AND "dateTime" <= timestamp with time zone '%s' """ \
                   % newestDateTime

        if oldestDateTime:
            sql += """ AND timestamp with time zone '%s' <= "dateTime" """ \
                   % oldestDateTime

        for cri in criteria:
            if isinstance(cri.value, str):
                sql += """ AND "value"->>'%s' like '%s' """ \
                       % (criteria.property.key, '%' + criteria.value + '%')

            elif isinstance(cri.value, list):
                criSql = []
                for value in cri.value:
                    try:
                        quotedVal = int(value)
                    except ValueError:
                        quotedVal = "'%s'" % value

                    criSql.append(""" "value" @> '{"%s":%s}'::jsonb """
                                  % (criteria.property.key, quotedVal))

                sql += """ AND (%s) """ % ' OR '.join(criSql)

            else:
                raise Exception("Unknown criteria type")

        # TODO, We probably need some pagination.

        def convertDate(strIn: str) -> datetime:
            if len(strIn.split('+')[1]) == 2:
                strIn += '00'
            return datetime.strptime(strIn, ISO8601)

        tuples = []

        cursor = plpy.cursor(sql)
        while True:
            rows = cursor.fetch(1000)
            if not rows:
                break
            for row in rows:
                tuples.append(EventDBEventTuple(dateTime=convertDate(row["dateTime"]),
                                                key=row["key"],
                                                value=row["value"]))

        payloadEnvelope = Payload(filt=filt, tuples=tuples).makePayloadEnvelope()
        vortexMsg = payloadEnvelope.toVortexMsg()
        return vortexMsg.decode()

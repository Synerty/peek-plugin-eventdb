import logging
from datetime import datetime

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_plugin_base.storage.RunPyInPg import runPyInPg
from peek_plugin_eventdb._private.storage.EventDBPropertyTable import EventDBPropertyTable
from peek_plugin_eventdb.tuples import loadPublicTuples
from peek_plugin_eventdb.tuples.EventDBEventTuple import EventDBEventTuple
from twisted.internet.defer import Deferred, inlineCallbacks
from vortex.Payload import Payload
from vortex.SerialiseUtil import ISO8601
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

logger = logging.getLogger(__name__)


class EventDBEventTupleProvider(TuplesProviderABC):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    @inlineCallbacks
    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> Deferred:
        # Uncomment this to print the SQL being created
        #
        # criterias = tupleSelector..get('criteria', [])
        # newestDateTime = tupleSelector..get('newestDateTime')
        # oldestDateTime = tupleSelector..get('oldestDateTime')
        #
        # sql = self._makeSql(criterias, 0, newestDateTime, oldestDateTime)
        # logger.info(sql)

        return (yield runPyInPg(logger,
                                self._dbSessionCreator,
                                self._loadInPg,
                                self._importTuples,
                                filt=filt,
                                tupleSelectorStr=tupleSelector.toJsonStr())).encode()

    @classmethod
    def _importTuples(cls):
        # noinspection PyUnresolvedReferences
        from peek_plugin_eventdb.tuples import EventDBPropertyCriteriaTuple
        loadPublicTuples()

    @classmethod
    def _loadInPg(cls, plpy, filt: dict, tupleSelectorStr: str):
        tupleSelector = TupleSelector().fromJsonStr(tupleSelectorStr)

        selector = tupleSelector.selector
        modelSetKey = selector.get('modelSetKey')
        criterias = selector.get('criteria', [])
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

        sql = cls._makeSql(criterias, modelSetId, newestDateTime, oldestDateTime)

        # TODO, We probably need some pagination.

        def convertDate(strIn: str) -> datetime:
            dateTime, offset = strIn.split('+')
            if '.' not in dateTime:
                dateTime += '.000'
            if len(offset) == 2:
                offset += '00'
            return datetime.strptime('%s+%s' % (dateTime, offset), ISO8601)

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

    @classmethod
    def _makeSql(cls, criterias, modelSetId, newestDateTime, oldestDateTime):
        P = EventDBPropertyTable
        # Create the basic SQL
        sql = """
            SELECT "dateTime", key, value
            FROM pl_eventdb."EventDBEvent"
            WHERE "modelSetId" = %s
            """ % modelSetId

        # Add in the date time criteria
        if newestDateTime:
            sql += """     AND "dateTime" <= timestamp with time zone '%s' \n""" \
                   % newestDateTime

        if oldestDateTime:
            sql += """     AND timestamp with time zone '%s' <= "dateTime" \n""" \
                   % oldestDateTime

        for cri in criterias:
            if not cri.value:
                continue

            if cri.property.showFilterAs == P.SHOW_FILTER_AS_FREE_TEXT:
                assert isinstance(cri.value, str), "Property value isn't a str"
                sql += """     AND "value"->>'%s' like '%s' \n""" \
                       % (cri.property.key, '%' + cri.value + '%')

            elif cri.property.showFilterAs == P.SHOW_FILTER_SELECT_MANY \
                or cri.property.showFilterAs == P.SHOW_FILTER_SELECT_ONE:

                if not isinstance(cri.value, list):
                    cri.value = [cri.value]

                criSql = []
                for value in cri.value:
                    try:
                        quotedVal = int(value)

                    except ValueError:
                        if value.lower() == 'true':
                            quotedVal = 'true'

                        elif value.lower() == 'false':
                            quotedVal = 'false'

                        else:
                            quotedVal = '"%s"' % value

                    criSql.append("""     "value" @> '{"%s":%s}'::jsonb """
                                  % (cri.property.key, quotedVal))

                sql += """     AND (%s) \n""" % '\n OR '.join(criSql)

                sql += """ LIMIT 5000
                           ORDER BY "dateTime" """

            else:
                raise Exception("Unknown criteria type")

        return sql

import logging

from twisted.internet.defer import Deferred, inlineCallbacks
from vortex.Payload import Payload
from vortex.Tuple import addTupleType, Tuple, TupleField
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_plugin_base.storage.RunPyInPg import runPyInPg
from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix
from peek_plugin_eventdb.tuples.EventDBEventTuple import EventDBEventTuple

logger = logging.getLogger(__name__)


@addTupleType
class _Param(Tuple):
    __tupleType__ = eventdbTuplePrefix + '_Param'

    filt = TupleField()
    tupleSelector: TupleSelector = TupleField()


class EventDBEventTupleProvider(TuplesProviderABC):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    @inlineCallbacks
    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> Deferred:
        param = _Param(filt=filt, tupleSelector=tupleSelector)
        return (yield runPyInPg(logger,
                                self._dbSessionCreator,
                                self._loadInPg,
                                param.toJsonDict())).encode()

    @classmethod
    def _loadInPg(cls, plpy, paramDict: dict):
        param = _Param().fromJsonDict(paramDict)
        selector = param.tupleSelector.selector
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

        # TODO, We probably need some pagination.

        tuples = []

        cursor = plpy.cursor(sql)
        while True:
            rows = cursor.fetch(1000)
            if not rows:
                break
            for row in rows:
                tuples.append(EventDBEventTuple(dateTime=row["dateTime"],
                                                key=row["key"],
                                                value=row["value"]))

        payloadEnvelope = Payload(filt=param.filt, tuples=tuples).makePayloadEnvelope()
        vortexMsg = payloadEnvelope.toVortexMsg()
        return vortexMsg.decode()

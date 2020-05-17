from vortex.Tuple import addTupleType, TupleField, Tuple

from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix


@addTupleType
class AdminStatusTuple(Tuple):
    __tupleType__ = eventdbTuplePrefix + "AdminStatusTuple"

    rawValueQueueStatus: bool = TupleField(False)
    rawValueQueueSize: int = TupleField(0)
    rawValueProcessedTotal: int = TupleField(0)
    rawValueLastError: str = TupleField()
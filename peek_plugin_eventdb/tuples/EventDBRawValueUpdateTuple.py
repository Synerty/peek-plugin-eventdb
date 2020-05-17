from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix

from vortex.Tuple import Tuple, addTupleType


@addTupleType
class EventDBRawValueUpdateTuple(Tuple):
    """ Live DB Raw Value Update

    This tuple represents an update to the raw value for a live db item

    """
    __tupleType__ = eventdbTuplePrefix + 'EventDBRawValueUpdateTuple'
    __slots__ = ("key", "rawValue")

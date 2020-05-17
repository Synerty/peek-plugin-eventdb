from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix

from vortex.Tuple import Tuple, addTupleType


@addTupleType
class EventDBDisplayValueUpdateTuple(Tuple):
    """ Live DB Display Value Update

    This tuple represents an update to the display value for a live db item

    """
    __tupleType__ = eventdbTuplePrefix + 'EventDBDisplayValueUpdateTuple'
    __slots__ = ("key", "displayValue")

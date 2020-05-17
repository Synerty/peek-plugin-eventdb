from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix

from vortex.Tuple import Tuple, addTupleType


@addTupleType
class EventDBRawValueTuple(Tuple):
    """ Live DB Raw Value Tuple

    This tuple represents a raw key / value pair in the Live Db

    """
    __tupleType__ = eventdbTuplePrefix + 'EventDBRawValueTuple'
    __slots__ = ("id", "key", "rawValue")

    def __init__(self, id=None, key=None, rawValue=None):
        # DON'T CALL SUPER INIT
        self.id = id
        self.key = key
        self.rawValue = rawValue

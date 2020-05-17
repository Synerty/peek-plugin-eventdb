from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix

from peek_plugin_eventdb._private.storage.EventDBItem import EventDBItem
from vortex.Tuple import Tuple, addTupleType


@addTupleType
class ImportEventDBItemTuple(Tuple):
    """ Live DB Display Value Tuple

    This tuple stores a value of a key in the Live DB database.

    """
    __tupleType__ = eventdbTuplePrefix + 'ImportEventDBItemTuple'
    __slots__ = ("key", "dataType", "rawValue", "displayValue", "importHash")

    DATA_TYPE_NUMBER_VALUE = EventDBItem.NUMBER_VALUE
    DATA_TYPE_STRING_VALUE = EventDBItem.STRING_VALUE
    DATA_TYPE_COLOR = EventDBItem.COLOR
    DATA_TYPE_LINE_WIDTH = EventDBItem.LINE_WIDTH
    DATA_TYPE_LINE_STYLE = EventDBItem.LINE_STYLE
    DATA_TYPE_GROUP_PTR = EventDBItem.GROUP_PTR

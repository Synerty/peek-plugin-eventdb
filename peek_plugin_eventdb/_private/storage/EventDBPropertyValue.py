from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from vortex.Tuple import addTupleType, Tuple

from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix
from .DeclarativeBase import DeclarativeBase
from .EventDBProperty import EventDBProperty


@addTupleType
class EventDBPropertyValue(Tuple, DeclarativeBase):
    __tablename__ = 'EventDBPropertyValue'
    __tupleType__ = eventdbTuplePrefix + __tablename__

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False, unique=True)
    comment = Column(String)

    propertyId = Column(Integer, ForeignKey('EventDBProperty.id', ondelete='CASCADE'),
                        nullable=False)
    property = relationship(EventDBProperty)

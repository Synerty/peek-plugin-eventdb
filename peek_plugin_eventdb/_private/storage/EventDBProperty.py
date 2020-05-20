from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from vortex.Tuple import addTupleType, Tuple

from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix
from .DeclarativeBase import DeclarativeBase
from .EventDBModelSet import EventDBModelSet


@addTupleType
class EventDBProperty(Tuple, DeclarativeBase):
    __tablename__ = 'EventDBProperty'
    __tupleType__ = eventdbTuplePrefix + __tablename__

    id = Column(Integer, primary_key=True, autoincrement=True)

    modelSetId = Column(Integer, ForeignKey('EventDBModelSet.id', ondelete='CASCADE'),
                        nullable=False)
    modelSet = relationship(EventDBModelSet)

    key = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    isFreeText = Column(Boolean, nullable=False)
    comment = Column(String)

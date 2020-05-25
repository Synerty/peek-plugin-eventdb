from sqlalchemy import Column, ForeignKey, Boolean, Index
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from vortex.Tuple import addTupleType, Tuple, TupleField

from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix
from .DeclarativeBase import DeclarativeBase
from .EventDBModelSetTable import EventDBModelSetTable


@addTupleType
class EventDBPropertyTable(Tuple, DeclarativeBase):
    __tablename__ = 'EventDBProperty'
    __tupleType__ = eventdbTuplePrefix + 'EventDBPropertyTable'

    SHOW_FILTER_AS_FREE_TEXT = 1
    SHOW_FILTER_AS_CHECK_BOXES = 2
    SHOW_FILTER_AS_DROP_DOWN = 3


    id = Column(Integer, primary_key=True, autoincrement=True)

    modelSetId = Column(Integer, ForeignKey('EventDBModelSet.id', ondelete='CASCADE'),
                        nullable=False)
    modelSet = relationship(EventDBModelSetTable)

    key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    comment = Column(String)

    useForFilter = Column(Boolean)
    useForDisplay = Column(Boolean)

    displayByDefaultOnSummaryView = Column(Boolean)
    displayByDefaultOnDetailView = Column(Boolean)

    showFilterAs = Column(Integer)

    valuesFromAdminUi = TupleField()

    __table_args__ = (
        Index("idx_EventDBProp_name", modelSetId, key, unique=True),
        Index("idx_EventDBProp_value", modelSetId, name, unique=True),
    )

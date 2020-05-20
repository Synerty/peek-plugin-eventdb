import logging

from sqlalchemy import Column, DateTime, BigInteger, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Index, ForeignKey
from vortex.Tuple import Tuple, addTupleType

from peek_plugin_eventdb._private.PluginNames import eventdbTuplePrefix
from .DeclarativeBase import DeclarativeBase

logger = logging.getLogger(__name__)


@addTupleType
class EventDBEvent(Tuple, DeclarativeBase):
    __tablename__ = 'EventDBEvent'
    __tupleType__ = eventdbTuplePrefix + __tablename__

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    dateTime = Column(DateTime(True), nullable=False)

    value = Column(JSONB, nullable=False)

    key = Column(String)

    modelSetId = Column(Integer,
                        ForeignKey('EventDBModelSet.id', ondelete='CASCADE'),
                        nullable=False)

    __table_args__ = (
        Index("idx_EventDBEvent_modelSetId", modelSetId, unique=False),
        Index("idx_EventDBEvent_key", key, unique=True),
    )

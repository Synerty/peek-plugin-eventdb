import logging
from typing import Optional

from sqlalchemy import Column, BigInteger, Index
from sqlalchemy import Integer, String
from vortex.Tuple import Tuple, addTupleType

from peek_abstract_chunked_index.private.tuples.ACIProcessorQueueTupleABC import \
    ACIProcessorQueueTupleABC
from .DeclarativeBase import DeclarativeBase
from ..PluginNames import eventdbTuplePrefix

logger = logging.getLogger(__name__)


@addTupleType
class EventDBRawValueQueue(Tuple, DeclarativeBase,
                          ACIProcessorQueueTupleABC):
    __tablename__ = 'EventDBRawValueQueue'
    __tupleType__ = eventdbTuplePrefix + __tablename__

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    modelSetId = Column(Integer, nullable=False)
    key = Column(String, nullable=False)
    rawValue = Column(String)

    @classmethod
    def sqlCoreLoad(cls, row):
        return EventDBRawValueQueue(id=row.id, modelSetId=row.modelSetId,
                                   key=row.key, rawValue=row.rawValue)

    @property
    def ckiUniqueKey(self):
        """ See EventDBRawValueQueueTuple.ckiUniqueKey """
        return "%s:%s" % (self.modelSetId, self.key)

    __table_args__ = (
        Index("idx_EventDBRawValueQueue_all", id, modelSetId, key, rawValue, unique=False),
    )


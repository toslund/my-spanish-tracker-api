# from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .user import User  # noqa: F401


class Definition(Base):
    __tablename__ = 'definition'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ## TODO change to uuid type in production
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True)
    content = Column(String(), nullable=False)
    rank = Column(Integer, nullable=True)
    region = Column(String(), nullable=True)
    note = Column(String(), nullable=True)
    date_added = Column(DateTime, nullable=False, server_default=func.now())
    date_deprecated = Column(DateTime, nullable=True)
    ## relationship
    # many definitions -> one vocab
    vocab_uuid = Column(Integer, ForeignKey('vocab.uuid'))
    vocab = relationship("Vocab", back_populates="definitions")

# from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .user import User  # noqa: F401


class Definition(Base):
    __tablename__ = 'definition'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ## TODO change to uuid type in production
    uuid = Column(String(36), nullable=False, unique=True)
    definition = Column(String(), nullable=False)
    rank = Column(Integer, nullable=True)
    region = Column(String(), nullable=True)
    note = Column(String(), nullable=True)
    date_added = Column(DateTime, nullable=True)
    date_deprecated = Column(DateTime, nullable=True)
    ## relationship
    # many definitions -> one vocab
    vocab_uuid = Column(Integer, ForeignKey('vocab.uuid'))
    vocab = relationship("Vocab", back_populates="definitions")

    # parent_id = Column(Integer, ForeignKey('parent.id'))
    # parent = relationship("Parent", back_populates="children")

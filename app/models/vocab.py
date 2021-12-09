# from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .user import User  # noqa: F401


class Vocab(Base):
    __tablename__ = 'vocab'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ## TODO change to uuid type in production
    uuid = Column(String(36), nullable=False, unique=True)
    word = Column(String(50), nullable=False)
    pos = Column(String(10), nullable=True)
    note_data = Column(String(), nullable=True)
    note_qaqc = Column(String(), nullable=True)
    note_grammar = Column(String(), nullable=True)
    note = Column(String(), nullable=True)
    date_added = Column(DateTime, nullable=True)
    date_deprecated = Column(DateTime, nullable=True)
    ## RELATIONSHIPS
    ## many vocab -> one lemma
    lemma_uuid = Column(Integer, ForeignKey('lemma.uuid'), primary_key=True) ## FOREIGN KEY
    lemma = relationship("Lemma", back_populates="vocabs")
    ## one vocab -> many definitions
    definitions = relationship("Definition", back_populates="vocab")
    ## one vocab -> many questions
    questions = relationship("Question", back_populates="vocab")

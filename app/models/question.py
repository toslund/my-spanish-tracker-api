from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Question(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    ## TODO change to uuid type in production
    uuid = Column(String(36), nullable=False, unique=True)
    correct = Column(Boolean, nullable=False)
    correctness = Column(Integer, nullable=True)
    date_added = Column(DateTime, nullable=True)
    ## TODO change to uuid type in production
    ## relationship
    deck_uuid = Column(String(36), ForeignKey("deck.uuid"))
    deck = relationship("Deck", back_populates="questions")

    vocab_uuid = Column(String(36), ForeignKey("vocab.uuid"))
    vocab = relationship("Vocab", back_populates="questions")
    

    
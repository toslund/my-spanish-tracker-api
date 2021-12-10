from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, index=True)
    ## TODO change to uuid type in production
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True)
    correct = Column(Boolean, nullable=False)
    correctness = Column(Integer, nullable=True)
    date_added = Column(DateTime, nullable=False, server_default=func.now())
    ## TODO change to uuid type in production
    ## relationship
    deck_uuid = Column(UUID(as_uuid=True), ForeignKey("deck.uuid"))
    deck = relationship("Deck", back_populates="questions")

    vocab_uuid = Column(UUID(as_uuid=True), ForeignKey("vocab.uuid"))
    vocab = relationship("Vocab", back_populates="questions")
    

    
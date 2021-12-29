from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401

class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True, index=True)
    ## TODO change to uuid type in production
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True)
    date_added = Column(DateTime, nullable=False, server_default=func.now())
    ## TODO change to uuid type in production
    ## relationship
    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))
    owner = relationship("User", back_populates="decks")

    questions = relationship("Question", back_populates="deck")
    

    
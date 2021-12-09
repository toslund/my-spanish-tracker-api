from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Deck(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    ## TODO change to uuid type in production
    uuid = Column(String(36), nullable=False, unique=True)
    date_added = Column(DateTime, nullable=True)
    ## TODO change to uuid type in production
    ## relationship
    owner_uuid = Column(String(36), ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")

    questions = relationship("Question", back_populates="deck")
    

    
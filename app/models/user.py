import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    ## TODO change to uuid type in production
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True,  default=uuid.uuid4)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    date_added = Column(DateTime, nullable=False, server_default=func.now())
    items = relationship("Item", back_populates="owner", cascade="all, delete")
    decks = relationship("Deck", back_populates="owner", cascade="all, delete")
    questions = relationship("Question", back_populates="owner", cascade="all, delete")
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ## TODO change to uuid type in production
    uuid = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, index=True)
    description = Column(String, index=True)
    date_added = Column(DateTime, nullable=False, server_default=func.now())
    ## TODO change to uuid
    owner_uuid = Column(Integer, ForeignKey("user.uuid"))
    owner = relationship("User", back_populates="items")

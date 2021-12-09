from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ## TODO change to uuid type in production
    uuid = Column(String(36), nullable=False)
    title = Column(String, index=True)
    description = Column(String, index=True)
    ## TODO change to uuid
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")

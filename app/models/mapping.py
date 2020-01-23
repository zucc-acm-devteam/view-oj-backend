from sqlalchemy import Column, String

from app.models.base import Base


class Mapping(Base):
    __tablename__ = 'mapping'

    key = Column(String(100), primary_key=True)
    value = Column(String(10000))

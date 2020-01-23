from sqlalchemy import Column, Integer, String

from app.models.base import Base


class OJ(Base):
    __tablename__ = 'oj'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    url = Column(String(1000))
    status = Column(Integer, nullable=False)

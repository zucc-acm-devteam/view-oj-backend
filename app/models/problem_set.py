from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class ProblemSet(Base):
    __tablename__ = 'problem_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    create_time = Column(DateTime)

from sqlalchemy import Column, Integer

from app.models.base import Base


class ProblemRelationship(Base):
    __tablename__ = 'problem_relationship'

    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, nullable=False)
    problem_set_id = Column(Integer, nullable=False)

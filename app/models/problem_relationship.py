from sqlalchemy import Column, ForeignKey, Integer

from app.models.base import Base
from app.models.problem import Problem
from app.models.problem_set import ProblemSet


class ProblemRelationship(Base):
    __tablename__ = 'problem_relationship'

    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey(Problem.id))
    problem_set_id = Column(Integer, ForeignKey(ProblemSet.id))

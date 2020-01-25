from sqlalchemy import Column, DateTime, Integer, String, ForeignKey

from app.models.base import Base
from app.models.problem import Problem
from app.models.user import User


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    problem_id = Column(Integer, ForeignKey(Problem.id))
    add_rating = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

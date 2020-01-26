from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base
from app.models.problem import Problem
from app.models.user import User


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    fields = ['id', 'username', 'problem_id', 'problem', 'add_rating', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    problem_id = Column(Integer, ForeignKey(Problem.id))
    add_rating = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

    @property
    def problem(self):
        return Problem.get_by_id(self.problem_id)

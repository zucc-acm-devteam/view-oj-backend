from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.problem_set.problem_set import ProblemSet
from app.models.user import User


class UserRelationship(Base):
    __tablename__ = 'user_relationship'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    problem_set_id = Column(Integer, ForeignKey(ProblemSet.id))

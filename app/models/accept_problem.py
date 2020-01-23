from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    problem_id = Column(Integer, nullable=False)
    add_rating = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

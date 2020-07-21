from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base
from app.models.camp_models.camp_problem import CampProblem
from app.models.camp_models.course_contest import CourseContest
from app.models.user import User


class CampAcceptProblem(Base):
    __tablename__ = 'camp_accept_problem'

    fields = ['id', 'username', 'problem', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    contest_id = Column(Integer, ForeignKey(CourseContest.id))
    problem_id = Column(Integer, ForeignKey(CampProblem.id))
    create_time = Column(DateTime, nullable=False)

    @property
    def problem(self):
        return CampProblem.get_by_id(self.problem_id)

    @classmethod
    def get_by_username_and_problem_id(cls, username, problem_id):
        r = cls.search(username=username, problem_id=problem_id)['data']
        if r:
            return r[0]
        return None

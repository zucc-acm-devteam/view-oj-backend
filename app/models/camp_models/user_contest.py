from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.models.base import Base
from app.models.camp_models.camp_accept_problem import CampAcceptProblem
from app.models.camp_models.course_contest import CourseContest
from app.models.user import User


class UserContest(Base):
    __tablename__ = 'user_contest'

    fields = ['id', 'username', 'contest', 'ac_cnt', 'rank', 'rating', 'accepted_problems']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    contest_id = Column(Integer, ForeignKey(CourseContest.id))
    ac_cnt = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    rating = Column(Float, default=0)

    @property
    def contest(self):
        return CourseContest.get_by_id(self.contest_id)

    @property
    def accepted_problems(self):
        return CampAcceptProblem.search(
            contest_id=self.contest_id,
            username=self.username
        )['data']

    @classmethod
    def get_by_username_and_contest_id(cls, username, contest_id):
        r = cls.search(username=username, contest_id=contest_id)['data']
        if r:
            return r[0]
        return None

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app.models.base import Base
from app.models.camp_models.camp_oj import CampOJ
from app.models.camp_models.course import Course
from app.models.user import User


class CourseOJUsername(Base):
    __tablename__ = 'course_oj_username'

    fields = ['username', 'oj', 'oj_username', 'last_success_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    oj_id = Column(String(100), ForeignKey(CampOJ.id))
    oj_username = Column(String(100), nullable=False)
    last_success_time = Column(DateTime)
    course_id = Column(Integer, ForeignKey(Course.id))

    @property
    def oj(self):
        return CampOJ.get_by_id(self.oj_id)

    @property
    def course(self):
        return Course.get_by_id(self.course_id)

    @property
    def rating(self):
        from app.models.camp_models.course import Course
        from app.models.camp_models.user_contest import UserContest
        contests = Course.get_by_id(self.course_id).contests
        res = 0
        for contest in contests:
            user_contest = UserContest.get_by_username_and_contest_id(
                username=self.username,
                contest_id=contest.id
            )
            if user_contest:
                res += user_contest.rating
        return res

    @classmethod
    def get_by_username_and_course_id(cls, username, course_id):
        r = cls.search(username=username, course_id=course_id)['data']
        if r:
            return r[0]
        else:
            return None

    def delete(self):
        from app.models.camp_models.user_contest import UserContest
        from app.models.camp_models.camp_accept_problem import CampAcceptProblem
        contests = self.course.contests
        for contest in contests:
            UserContest.get_by_username_and_contest_id(
                self.username,
                contest.id
            ).delete()
            accept_problems = CampAcceptProblem.search(
                username=self.username,
                contest_id=contest.id
            )['data']
            for accept_problem in accept_problems:
                accept_problem.delete()
        super().delete()

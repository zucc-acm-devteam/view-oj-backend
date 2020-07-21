from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.camp_models.course import Course


class CourseContest(Base):
    __tablename__ = 'course_contest'

    fields = ['id', 'name']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    max_pass = Column(Integer, default=0)
    participants = Column(Integer, default=0)
    contest_cid = Column(String(100))
    course_id = Column(Integer, ForeignKey(Course.id))

    @property
    def problems(self):
        from app.models.camp_models.camp_problem import CampProblem
        return CampProblem.search(contest_id=self.id)['data']

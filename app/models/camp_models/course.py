from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.camp_models.camp import Camp
from app.models.camp_models.camp_oj import CampOJ


class Course(Base):
    __tablename__ = 'course'

    fields = ['id', 'name', 'camp_oj', 'contests']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    camp_oj_id = Column(Integer, ForeignKey(CampOJ.id))
    spider_username = Column(String(100))
    spider_password = Column(String(100))
    camp_id = Column(Integer, ForeignKey(Camp.id))

    @property
    def camp_oj(self):
        return CampOJ.get_by_id(self.camp_oj_id)

    @property
    def contests(self):
        from app.models.camp_models.course_contest import CourseContest
        return CourseContest.search(course_id=self.id, page_size=-1)['data']

    def append_contest(self, **kwargs):
        from app.models.camp_models.course_contest import CourseContest
        CourseContest.create(course_id=self.id, **kwargs)

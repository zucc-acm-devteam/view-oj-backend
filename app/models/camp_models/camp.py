from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Camp(Base):
    __tablename__ = 'camp'

    fields = ['id', 'name']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    @property
    def courses(self):
        from app.models.camp_models.course import Course
        return Course.search(camp_id=self.id, page_size=-1)['data']

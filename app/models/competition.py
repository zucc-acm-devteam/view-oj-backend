import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, asc

from app.models.base import Base, db


class Competition(Base):
    __tablename__ = 'competition'
    fields = ['id', 'name', 'link', 'start_time', 'end_time', 'remark']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1000), nullable=False)
    link = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    remark = Column(Text, default='')

    @classmethod
    def search_from_now(cls, page=1, page_size=20):
        res = cls.query
        res = res.filter(getattr(cls, 'end_time') >= datetime.datetime.now())
        res = res.order_by(asc(getattr(cls, 'start_time')))
        data = {
            'meta': {
                'count': res.count(),
                'page': page,
                'page_size': page_size
            }
        }

        if page_size != -1:
            res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data

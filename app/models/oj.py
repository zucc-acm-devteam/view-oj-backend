from sqlalchemy import Column, Integer, String

from app.models.base import Base


class OJ(Base):
    __tablename__ = 'oj'

    fields = ['id', 'name', 'status']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    url = Column(String(1000))
    status = Column(Integer, nullable=False)

    @classmethod
    def get_by_name(cls, name):
        r = cls.search(name=name)['data']
        if r:
            return r[0]
        return cls.create(name=name, status=0)

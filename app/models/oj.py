from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base


class OJ(Base):
    __tablename__ = 'oj'

    fields = ['id', 'name', 'status', 'need_password', 'allow_team', 'allow_child_account']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    url = Column(String(1000))
    status = Column(Integer, nullable=False)
    need_password = Column(Boolean, nullable=False, default=False)
    need_single_thread = Column(Boolean, nullable=False, default=False)
    allow_team = Column(Boolean, nullable=False, default=False)
    allow_child_account = Column(Boolean, nullable=False, default=False)

    @classmethod
    def get_by_name(cls, name):
        r = cls.search(name=name)['data']
        if r:
            return r[0]
        return cls.create(name=name, status=0)

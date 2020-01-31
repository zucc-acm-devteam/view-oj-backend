from sqlalchemy import Column, String

from app.models.base import Base


class Mapping(Base):
    __tablename__ = 'mapping'

    key = Column(String(100), primary_key=True)
    value = Column(String(10000))

    @classmethod
    def get_by_id(cls, id_):
        res = cls.query.get(id_)
        if res:
            return res
        return cls.create(key=id_)

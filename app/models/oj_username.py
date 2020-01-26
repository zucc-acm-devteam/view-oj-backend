from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base
from app.models.user import User


class OJUsername(Base):
    __tablename__ = 'oj_username'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    oj_id = Column(Integer, nullable=False)
    oj_username = Column(String(100), nullable=False)
    oj_password = Column(String(100))
    oj_cookies = Column(String(10000))
    last_success_time = Column(DateTime)

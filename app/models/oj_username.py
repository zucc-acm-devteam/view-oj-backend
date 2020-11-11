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

    @classmethod
    def get_by_username_and_oj_id(cls, username, oj_id):
        r = cls.search(username=username, oj_id=oj_id)['data']
        if r:
            return r[0]

    def delete(self):
        from app.models.base import db
        from app.models.accept_problem import AcceptProblem
        from app.models.codeforces_rounds import CodeforcesRounds
        from app.models.oj import OJ
        db.session.query(AcceptProblem). \
            filter(AcceptProblem.referer_oj_id == self.oj_id). \
            filter(AcceptProblem.username == self.username).delete()
        if OJ.get_by_id(self.oj_id).name == 'codeforces':
            db.session.query(CodeforcesRounds). \
                filter(CodeforcesRounds.username == self.username).delete()
        super().delete()

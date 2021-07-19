from sqlalchemy import Column, DateTime, ForeignKey, Boolean, Integer, String

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
    is_team_account = Column(Boolean, nullable=False, default=False)
    is_child_account = Column(Boolean, nullable=False, default=False)

    @classmethod
    def get_by_username_and_oj_id(cls, username, oj_id):
        r = cls.search(username=username, oj_id=oj_id)['data']
        if r:
            return r[0]

    def delete(self):
        from app.models.accept_problem import AcceptProblem
        from app.models.base import db
        from app.models.codeforces_rounds import CodeforcesRounds
        from app.models.oj import OJ
        from app.models.user import User
        if not self.is_team_account:
            db.session.query(AcceptProblem). \
                filter(AcceptProblem.oj_username_id == self.id).delete()
        if OJ.get_by_id(self.oj_id).name == 'codeforces' and \
                not self.is_child_account and not self.is_team_account:
            db.session.query(CodeforcesRounds). \
                filter(CodeforcesRounds.username == self.username).delete()
            User.get_by_id(self.username).modify(codeforces_rating=0, contest_num=0, last_cf_date=None)

        super().delete()

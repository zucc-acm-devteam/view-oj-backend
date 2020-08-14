from flask_login import UserMixin
from sqlalchemy import Column, Date, Integer, String, cast, func

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    fields = ['username', 'nickname', 'group', 'permission', 'status', 'name_color', 'name_back_color']

    username = Column(String(100), primary_key=True)
    nickname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    group = Column(String(100))
    permission = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0)
    rating = Column(Integer, nullable=False, default=0)
    codeforces_rating = Column(Integer, nullable=False, default=0)
    contest_num = Column(Integer, nullable=False, default=0)
    name_color_ = Column('name_color', String(100))
    name_back_color_ = Column('name_back_color', String(100))

    @property
    def id(self):
        return self.username

    @property
    def oj_username(self):
        from app.models.oj_username import OJUsername
        from app.models.oj import OJ
        res = OJUsername.search(username=self.username, page_size=-1)['data']
        r = list()
        for i in OJ.search(status=1, page_size=-1)['data']:
            oj_username = None
            last_success_time = None
            for j in res:
                if j.oj_id == i.id:
                    oj_username = j.oj_username
                    last_success_time = j.last_success_time
                    break
            r.append({
                'oj': i,
                'oj_username': oj_username,
                'last_success_time': last_success_time
            })
        return r

    @property
    def problem_distributed(self):
        from app.models.accept_problem import AcceptProblem
        from app.models.oj import OJ
        from app.models.problem import Problem
        res = []
        oj_list = OJ.search(page_size=-1)['data']
        for i in oj_list:
            res.append({
                'oj': i,
                'num': AcceptProblem.query.filter(
                    AcceptProblem.username == self.username,
                    AcceptProblem.problem_id.in_(db.session.query(Problem.id).filter_by(oj_id=i.id).subquery())
                ).count()
            })
        return res

    @property
    def rating_trend(self):
        from app.models.accept_problem import AcceptProblem
        return [{
            'date': i[0],
            'add_rating': int(i[1])
        } for i in
            db.session.query(cast(AcceptProblem.create_time, Date), func.sum(AcceptProblem.add_rating)).filter(
                AcceptProblem.username == self.username
            ).group_by(cast(AcceptProblem.create_time, Date)).order_by(cast(AcceptProblem.create_time, Date)).all()]

    @property
    def name_color(self):
        if self.name_color_ is None:
            return None
        return self.name_color_.split(',')

    @property
    def name_back_color(self):
        if self. name_back_color_ is None:
            return None
        return self.name_back_color_.split(',')

    def check_password(self, password):
        return self.password == password

    @staticmethod
    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return AuthFailed()

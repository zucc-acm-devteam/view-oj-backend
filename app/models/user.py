from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, func

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    fields = ['username', 'nickname', 'group', 'permission', 'status']

    username = Column(String(100), primary_key=True)
    nickname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    group = Column(String(100))
    permission = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    @property
    def id(self):
        return self.username

    @property
    def rating(self):
        from app.models.accept_problem import AcceptProblem
        add_rating = db.session.query(func.sum(AcceptProblem.add_rating)) \
            .filter(AcceptProblem.username == self.username).all()[0][0]
        add_rating = 0 if add_rating is None else int(add_rating)
        return current_app.config['DEFAULT_USER_RATING'] + add_rating

    @property
    def oj_username(self):
        from app.models.oj_username import OJUsername
        from app.models.oj import OJ
        res = OJUsername.search(username=self.username, page_size=100)['data']
        r = list()
        for i in OJ.search(status=1, page_size=100)['data']:
            oj_username = None
            last_success_time = None
            for j in res:
                if j.oj_id == i.id:
                    oj_username = j.oj_username
                    last_success_time = j.last_success_time
                    break
            r.append({
                'oj_id': i.id,
                'oj_name': i.name,
                'oj_username': oj_username,
                'last_success_time': last_success_time
            })
        return r

    @property
    def problem_distributed(self):
        from app.models.oj import OJ
        oj_list = OJ.search(page_size=1000)['data']
        for i in oj_list:
            pass
        pass

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

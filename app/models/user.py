from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, func

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.accept_problem import AcceptProblem
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    fields = ['username', 'nickname', 'group', 'permission', 'status', 'rating']

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

        add_rating = db.session.query(func.sum(AcceptProblem.add_rating)).all()[0][0]
        if add_rating is None:
            add_rating = 0
        else:
            add_rating = int(add_rating)
        return current_app.config['DEFAULT_USER_RATING'] + add_rating

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

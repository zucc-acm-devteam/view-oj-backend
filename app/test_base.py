import datetime

import pytest

from app import create_app, db
from app.models.accept_problem import AcceptProblem
from app.models.oj import OJ
from app.models.oj_username import OJUsername
from app.models.problem import Problem
from app.models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///../view-oj.db"

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            User.create(username='admin', nickname='admin', password='admin', permission=1, status=1)
            User.create(username='user', nickname='user', password='user', permission=0, status=0)

            OJ.create(name='test-oj', status=1)
            OJ.create(name='codeforces', status=1)
            OJ.create(name='hdu', status=0)

            Problem.create(oj_id=1, problem_pid='1000', rating=1500)
            Problem.create(oj_id=2, problem_pid='1001', rating=1500)

            AcceptProblem.create(username='admin', problem_id=1, add_rating=5,
                                 create_time=datetime.datetime(2019, 1, 1))
            AcceptProblem.create(username='admin', problem_id=2, add_rating=5)
            AcceptProblem.create(username='user', problem_id=1, add_rating=5)

            OJUsername.create(username='admin', oj_id=2, oj_username='taoting')
        yield client

    db.session.remove()

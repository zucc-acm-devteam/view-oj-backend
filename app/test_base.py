import pytest
from app import create_app, db
from app.models.accept_problem import AcceptProblem
from app.models.oj import OJ
from app.models.problem import Problem
from app.models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    app.debug = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            User.create(username='admin', nickname='admin', password='admin', permission=-1, status=1)
            User.create(username='user', nickname='user', password='user', permission=0, status=0)

            OJ.create(name='test-oj1', status=1)
            OJ.create(name='test-oj2', status=0)

            Problem.create(oj_id=1, problem_pid='1000', rating=1500)

            AcceptProblem.create(username='admin', problem_id=1, add_rating=5)
        yield client

    db.session.remove()

import pytest
from app import create_app, db
from app.models.oj import OJ
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
            OJ.create(name='test-oj', status=1)
        yield client

    db.session.remove()

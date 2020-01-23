import unittest

from app import create_app, db
from app.models.oj import OJ
from app.models.user import User


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app.debug = True
        self.app_context = self.app.app_context()
        self.test_client = self.app.test_client()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        User.create(username='admin', nickname='admin', password='admin', permission=-1, status=1)
        User.create(username='user', nickname='user', password='user', permission=0, status=0)

        OJ.create(name='test-oj', status=1)

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewsTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="test", email="test@test.com", password="password", image_url=None)
        self.testuser_id = 9999
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("cat", "test1@test.com", "password", None)
        self.u1_id = 4444
        self.u1.id = self.u1_id
        self.u2 = User.signup("dog", "test2@test.com", "password", None)
        self.u2_id = 5555
        self.u2.id = self.u2_id
        self.u3 = User.signup("hamster", "test3@test.com", "password", None)
        self.u4 = User.signup("turtle", "test4@test.com", "password", None)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@test", str(resp.data))
            self.assertIn("@dog", str(resp.data))
            self.assertIn("@cat", str(resp.data))
            self.assertIn("@hamster", str(resp.data))
            self.assertIn("@turtle", str(resp.data))
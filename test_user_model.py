"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
import unittest
from unittest import TestCase

from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        # User.query.delete()
        # Message.query.delete()
        # Follows.query.delete()

        db.drop_all()
        db.create_all()

        user1 = User.signup("1", "test1@test.com", "password", None)
        uid1 = 1
        user1.id = uid1

        user2 = User.signup("2", "test2@test.com", "password", None)
        uid2 = 2
        user2.id = uid2

        db.session.commit()

        user1= User.query.get(uid1)
        user2= User.query.get(uid2)

        self.user1 = user1
        self.uid1 = uid1

        self.user2 = user2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_follows(self):
        self.user1.following.append(self.user2)

        self.assertEqual(len(self.user2.following), 0)
        self.assertEqual(len(self.user2.followers), 1)
        self.assertEqual(len(self.user1.followers), 0)
        self.assertEqual(len(self.user1.following), 1)

        self.assertEqual(self.u1.following[0].id, self.user2.id)
        self.assertEqual(self.u2.followers[0].id, self.user1.id)

    def test_valid_signup(self):
        user_test = User.signup("test", "test@testtttt.com", "password", None)
        uid = 8
        user_test.id = uid
        db.session.commit()

        user_test = User.query.get(uid)
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, "test")

    def test_valid_auth(self):
        u = User.authenticate(self.user1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

    
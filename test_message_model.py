"""Tests for message model."""

import os
from unittest import TestCase

from models import db, connect_db, Message, Follows, User, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test view functions for messages."""
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 6
        u = User.signup("test", "test@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        msg = Message(text="test warble", user_id=self.uid)

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test warble")

    def test_message_likes(self):
        msg1 = Message(text="test warble", user_id=self.uid)
        msg2 = Message(text="another test warble", user_id=self.uid)

        user = User.signup("anothertestytest", "testytest@test.com", "password", None)
        uid= 7
        user.id = uid
        db.session.add_all([msg1, msg2, user])
        db.session.commit()

        user.likes.append(msg1)
        db.session.commit()
        
        like = Likes.query.filter(Likes.user_id== uid).all()

        self.assertEqual(len(like), 1)
        self.assertEqual(like[0].message_id, msg1.id)
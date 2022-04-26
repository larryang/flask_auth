""" fixture to add/delete user """
import pytest
from app import db
from app.db.models import User, Song


@pytest.fixture
def add_db_user_fixture(application):
    """ setup database user and delete """

    with application.app_context():
        assert db.session.query(User).count() == 0 # pylint: disable=no-member

        user_email = 'testuser@test.com'
        user_password = 'testtest'
        user = User(user_email, user_password)
        db.session.add(user) # pylint: disable=no-member

        user = User.query.filter_by(email=user_email).first()
        assert user.email == user_email
        db.session.commit() # pylint: disable=no-member

        yield user

        db.session.delete(user) # pylint: disable=no-member
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Song).count() == 0 # pylint: disable=no-member

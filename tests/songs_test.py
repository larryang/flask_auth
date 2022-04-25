""" test songs model/database """
import pytest
from app import db
from app.db.models import User, Song


@pytest.fixture
def add_db_user_fixture(application):
    """ setup database user and delete """

    with application.app_context():
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Song).count() == 0 # pylint: disable=no-member

        user_email = 'testuser@test.com'

        user = User(user_email, 'testtest')
        db.session.add(user) # pylint: disable=no-member

        user = User.query.filter_by(email=user_email).first()
        assert user.email == user_email
        db.session.commit() # pylint: disable=no-member

        yield user

        db.session.delete(user) # pylint: disable=no-member
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Song).count() == 0 # pylint: disable=no-member


def test_adding_songs(application, add_db_user_fixture):
    """ simple test of adding Songs to model """
    # pylint: disable=unused-argument,redefined-outer-name
    user = add_db_user_fixture
    user.songs = [ Song('title1', 'artist1', 1999, 'genre1'),
        Song('title2', 'artist2', 2000, 'genre2') ]
    db.session.commit() # pylint: disable=no-member

    assert db.session.query(Song).count() == 2 # pylint: disable=no-member
    song1 = Song.query.filter_by(title='title1').first()
    assert song1.title == "title1"

    #changing the title of the song
    song1.title = "SuperSongTitle"
    #saving the new title of the song
    db.session.commit() # pylint: disable=no-member
    song2 = Song.query.filter_by(title='SuperSongTitle').first()
    assert song2.title == "SuperSongTitle"

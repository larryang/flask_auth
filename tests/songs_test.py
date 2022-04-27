""" test songs model/database """
import os
from app import db
from app.db.models import Song, User
from app import config
from tests.user_fixture import add_db_user_fixture # pylint: disable=unused-import


def test_adding_songs(application, add_db_user_fixture):
    """ simple test of adding Songs to model """
    # pylint: disable=unused-argument,redefined-outer-name
    user = add_db_user_fixture
    assert db.session.query(Song).count() == 0 # pylint: disable=no-member

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


def test_upload_songs(application, add_db_user_fixture):
    """ unit test file upload """
    # pylint: disable=unused-argument,redefined-outer-name

    assert db.session.query(Song).count() == 0 # pylint: disable=no-member

    # from https://blog.entirely.digital/flask-pytest-testing-uploads/
    root = config.Config.BASE_DIR
    filename = 'sample.csv'
    filepath = root + '/../tests/' + filename
    user = User.query.get(1) # shortcut, fixture only has 1 user

    upload_folder = config.Config.UPLOAD_FOLDER
    upload_file = os.path.join(upload_folder, filename)
    if os.path.exists(upload_file):
        os.remove(upload_file)

    with application.test_client(user=user) as client:
        with open(filepath, 'rb') as file:
            data = {
                'file': (file, filename),
                #'csrf_token': current_
            }
            resp = client.post('songs/upload', data=data)

    assert resp.status_code == 302

    assert db.session.query(Song).count() == 2 # pylint: disable=no-member
    song1 = Song.query.filter_by(artist="Public Enemy").first()
    assert song1.title == "Don't Believe The Hype"

    assert os.path.exists(upload_file)
    os.remove(upload_file)

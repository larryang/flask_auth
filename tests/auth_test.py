"""This test authorization pages"""
from app.db.models import User
from app import db
from tests.user_fixture import add_db_user_fixture # pylint: disable=unused-import


def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_register(client):
    """ POST to /register """
    new_email = 'newuser@test.test'
    new_password = 'Test1234!'
    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('register', data=data)

    assert resp.status_code == 302

    # verify new user is in database
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user) # pylint: disable=no-member


def test_login(client, add_db_user_fixture):
    """ POST to login """
    data = {
        'email' : 'testuser@test.com',
        'password' : 'testtest'
    }
    resp = client.post('login', data=data)

    assert resp.status_code == 302

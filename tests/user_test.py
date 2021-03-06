""" test user model/database """
import logging

#from faker import Faker
from app import db
from app.db.models import User, Song

def test_adding_user(application):
    """ example test to show how to access database """
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Song).count() == 0 # pylint: disable=no-member
        #showing how to add a record
        #create a record
        user = User('keith@webizly.com', 'testtest')
        #add it to get ready to be committed
        db.session.add(user) # pylint: disable=no-member
        #call the commit
        #db.session.commit()
        #assert that we now have a new user
        #assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='keith@webizly.com').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'

        #checking cascade delete
        db.session.delete(user) # pylint: disable=no-member
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Song).count() == 0 # pylint: disable=no-member

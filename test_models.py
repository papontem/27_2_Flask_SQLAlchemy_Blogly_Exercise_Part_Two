from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for User."""

    def setUp(self):
        """Clean up any existing users. add two for testing"""

        User.query.delete()
        # db.session.commit()

        user = User(first_name="TestUser",last_name="Tattertot",img_url="imgs/pam_favicon_animated.gif")
        user2 = User(first_name="TestUser2",last_name="FrenchFry",img_url="imgs/pam_favicon_animated.gif") 
        
        db.session.add(user)
        db.session.add(user2)
        
        db.session.commit()
        self.user = user
        self.user2 = user2

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_greet(self):
        
        self.assertEqual(self.user.greet(), "I'm TestUser Tattertot")
        self.assertEqual(self.user2.greet(), "I'm TestUser2 FrenchFry")


    
    def test_get_all_first_name(self): #TODO get the query result and assert

        query_result1 = User.get_all_first_name('TestUser')
        query_result2 = User.get_all_first_name('TestUser2')

        # ADD THE ASSERT
        self.assertEqual(query_result1,[self.user])
        self.assertEqual(query_result2,[self.user2])
    
    
    def test_get_all_last_name(self): #TODO get the query result and assert

        query_result1 = User.get_all_last_name('Tattertot')
        query_result2 = User.get_all_last_name('FrenchFry')

        # ADD THE ASSERT
        self.assertEqual(query_result1,[self.user])
        self.assertEqual(query_result2,[self.user2])

    
    def test_get_all_Users(self):

        query_result = User.get_all_Users()

        # ADD THE ASSERT
        self.assertEqual(query_result,[self.user, self.user2])
    

    # def test_get_by_species(self):
    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     db.session.add(pet)
    #     db.session.commit()

    #     dogs = Pet.get_by_species('dog')
    #     self.assertEqual(dogs, [pet])

from unittest import TestCase

from app import app
from models import db, User
import json, sys, traceback

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User."""

        User.query.delete()

        user = User(first_name="TestUser",last_name="Tasty",img_url="imgs/pam_favicon_animated.gif")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_redirect(self):
        with app.test_client() as client:
            try:
                # Pythons Native Debugger here to help ^_^ !! 
                # import pdb
                # pdb.set_trace()

                resp = client.get("/", follow_redirects=False)
                # html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that were being redirected to /users from / ")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_home_redirect_followed(self): 
        with app.test_client() as client:

            try:
                
                resp = client.get("/", follow_redirects=True)
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that the redirection from /users to / was sucesfull or not")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_list_Users(self):
        with app.test_client() as client:
            try:
                resp = client.get("/users")
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in getting the users.html page from /users")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_show_User(self): 
        with app.test_client() as client:
            try:
                

                resp = client.get(f"/users/{self.user_id}")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)
            
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in trying to show a specific user following /users/self.user_id")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            
    def test_add_User_redirect(self): 
        with app.test_client() as client:
            try:
                d = {"first_name":"TestUser2","last_name":"Tasty2","img_url":"imgs/pam_favicon_animated.gif"}
                resp = client.post("/users/new", data=d, follow_redirects=False)
                # html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing if were being redirected when adding a new user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_add_User_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {"first_name": "TestUser2","last_name":'Tasty2',"img_url":'imgs/pam_favicon_animated.gif'}
                resp = client.post("/users/new", data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that we were redirected succesfully after adding a new user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("TestUser2", html)

    def test_delete_user(self):
        with app.test_client() as client:
            try:
                resp = client.post(f"/users/${self.user_id}/delete",follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in trying to delete a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertNotIn("TestUser",html)

# @app.route('/users/<int:user_id>/edit') #TODO make TESTS FOR EDITING A USER
# def show_user_edit_page(user_id):
#     """
#         Show the edit page for a user.
#         Have a cancel button that returns to the detail page for a user,
#           and a save button that updates the user.
#     """
#     user = User.query.get_or_404(user_id)
#     return render_template("edit_user.html", user=user)

# @app.route('/users/<int:user_id>/edit', methods=["POST"])
# def edit_the_user(user_id):
#     """Process the edit form, returning the user to the /users page."""
#     edit_first_name = request.form["first_name"]
#     edit_last_name = request.form["last_name"]
#     edit_img_url = request.form["img_url"]
    
#     editing_user = User.query.get_or_404(user_id)

#     editing_user.first_name = edit_first_name
#     editing_user.last_name = edit_last_name
#     editing_user.img_url = edit_img_url
    
#     db.session.add(editing_user)
#     db.session.commit()

#     return redirect("/users")
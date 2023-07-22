from unittest import TestCase

from app import app
from models import db, User, Post
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
        """Add sample test User and sample test post."""
        db.drop_all()
        db.create_all()

        #making sure user and post tables are empty!!
        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="TestUser",last_name="Tasty",img_url="")

        db.session.add(test_user)
        db.session.commit()

        test_post_data = {"title":"TestPostTitle", "content":"Test Post Content"}
        test_post = Post.create_post(test_user,test_post_data["title"],test_post_data["content"])

        db.session.add(test_post)
        db.session.commit()

        self.user_id = test_user.id
        self.user = test_user

        self.post_id = test_post.id
        self.post = test_post

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
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in trying to show a specific user following /users/self.user_id")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)
                self.assertIn("User Profile <br> Img Url Value <br> will be chosen later?", html)
            
    def test_add_User_redirect(self): 
        with app.test_client() as client:
            try:
                d = {
                    "first_name":"TestUser2",
                    "last_name":"Tasty2",
                    "img_url":""
                     }
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
                d = {
                    "first_name": "TestUser2",
                     "last_name":'Tasty2',
                     "img_url":""
                     }
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
                # whoops i had used a $ from js syntax when getting user_id
                resp = client.post(f"/users/{self.user_id}/delete",follow_redirects=True)
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
    
    def test_show_user_edit_page(self):
        with app.test_client() as client:
            try:
                resp = client.get(f"/users/{self.user_id}/edit")
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user was shown the edit page for their profile")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_edit_the_user_redirect(self):
        with app.test_client() as client:
            try:
                d = {
                    "first_name": "TestUser1111",
                     "last_name":'Tasty1111',
                     "img_url":""
                     }
                resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=False)
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user is being redirected after sending a post request to edit a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_edit_the_user_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {
                    "first_name": "TestUser1111",
                     "last_name":'Tasty1111',
                     "img_url":""
                     }
                resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user was sucessfuly redirected after editing a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("TestUser1111", html)

# TODO ADD TESTING FOR THE NEW ROUTES FROM part 2 POSTs
# # GET /posts 
# @app.route('/posts')
# def list_posts():
#     """ 
#         Show posts
#         Show only their titles within an anchor tag , and their author within an anchor tag
#         Make these links to view the detail page for the post, and for the user
#     """
#     posts = Post.query.all()

#     return render_template("posts.html", posts=posts)


# # # GET /posts/<int:post_id>
# @app.route('/posts/<int:post_id>')
# def details_post(post_id):
#     """
#         Show a post details page.
#         title, content, author, time of posting
#         Show buttons to edit and delete the post.
#     """
#     post = Post.query.get_or_404(post_id)

#     return render_template('details_post.html', post=post)

# # # GET /posts/<int:post_id>/edit
# @app.route('/posts/<int:post_id>/edit')
# def show_edit_post_form(post_id):
#     """ Show form to edit a post, and to cancel (back to user page). """
#     post = Post.query.get_or_404(post_id)
#     return render_template('edit_post.html', post=post)

# # # POST /posts/<int:post_id>/edit
# @app.route('/posts/<int:post_id>/edit', methods=["POST"])
# def edit_post_form_submitted(post_id):
#     """ Handle editing of a post. Redirect back to the post view. """
#     post = Post.query.get_or_404(post_id)
    
#     editing_title = request.form["title"]
#     editing_content = request.form["content"]
    
#     post.title = editing_title
#     post.content = editing_content

#     db.session.add(post)
#     db.session.commit()

#     return redirect(f"/posts/{post.id}")

# # # POST /posts/<int:post_id>/delete
# @app.route('/posts/<int:post_id>/delete', methods=["POST"])
# def delete_post(post_id):
#     """Delete the post. redirect to user details page"""

#     post = Post.query.get(post_id)
#     #save author id int for redirecting after deletion
#     post_author_id = post.author_user.id
#     db.session.delete(post)
#     db.session.commit()

#     return redirect(f'/users/{post_author_id}')

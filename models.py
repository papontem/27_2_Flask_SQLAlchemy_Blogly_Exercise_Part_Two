"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS BELOW:
# All models should subclass db.Model
class User(db.Model):
    """ Users Table"""
    # Specify the tablename with __tablename__
    __tablename__ = 'users'
    
    #Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    img_url = db.Column(db.Text(), nullable=False, default='no_url_given')

    @classmethod
    def get_all_first_name(cls, name):
        return cls.query.filter_by(first_name=name).all()
    
    @classmethod
    def get_all_last_name(cls, name):
        return cls.query.filter_by(last_name=name).all()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    def __repr__(self):
        u = self
        return f"<User id#={u.id} | first_name={u.first_name} | last_name={u.last_name} | img_url={u.img_url}>"
    

    def greet(self):
        return f"I'm {self.first_name} {self.last_name}"
    
class Post(db.Model):
    """ Posts Table """
    __tablename__ = 'posts'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Foreign keys
    # [name_of_key_in_posts] = db.Column(db.[datatype] , db.ForeignKey('[model_table_name].[model_table_columns_name]'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    author_user = db.relationship('User', backref='posts')

    @classmethod
    def get_by_user(cls, usr):
        """ When given a 'usr', assuming its a user object instance, this function returns posts made by that user """
        return usr.posts
    
    @classmethod
    def get_all_posts_with_users(cls):
        # join between the users and posts tables
        query_result = db.session.query(User, cls).join(cls, User.id == cls.user_id).all()

        # # Query the Post model and include the User relationship
        # query_result = Post.query.options(db.joinedload('author')).all()

        # The result will be a list of tuples, where each tuple contains a User object and a Post object.
        return query_result

    def create_post(author, title, content):
        # Create a new Post object and set its attributes, have sqlalchemy server call its now() function for making datetime values
        new_post = Post(title=title, content=content, created_at=db.func.now())

        # Set the relationship with the author
        new_post.author_user = author

        return new_post
    
    

    def __repr__(self):
        p = self
        return f"<Post id#={p.id} | title={p.title} | created_at={p.created_at}>"
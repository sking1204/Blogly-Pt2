from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.iconpacks.net/icons/1/free-user-icon-295-thumb.png"


def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.Text,
                           nullable = False)
    
    last_name = db.Column(db.Text,
                          nullable = False)
    
    image_url = db.Column(db.Text,
                          nullable = False,
                          default=DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
  


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key = True, 
                   autoincrement = True)
    
    title = db.Column(db.Text,
                      nullable = False)
                      
    content = db.Column(db.Text,
                        nullable = False)
                      
    created_at = db.Column(db.DateTime,
                           default =datetime.now,
                            nullable = False )
                           
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                      nullable = False)
    

    

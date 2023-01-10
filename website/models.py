from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

    """
    When creating a relationship, it's referencing a class, not an attribute,
    so we need to use the uppercase version of it. This will be a 
    list that stores the recipes created by the user
    """
    recipes = db.relationship('Recipe')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(150))
    description = db.Column(db.String(250))
    servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    ingredients = db.Column(db.String(1500))
    directions = db.Column(db.String(1500))
    nutrition = db.Column(db.String(1500))
    is_public = db.Column(db.Boolean(), default=False)

    """
    Foreign key is a column in the Recipe (or any) db that will reference a 
    different column in another db. In this instance, we need to use the fk to 
    access the Users db so that we can associate recipes to their creators. Also
    note that the reference is lower-case
    """
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


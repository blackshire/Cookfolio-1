from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'database'
DB_LOCATION = f'postgresql://Steve:Pizzaslut69!@localhost/{DB_NAME}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234asdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_LOCATION
    db.init_app(app)

    from .views import views
    from .auth import auth

    # Registering the imported blueprints so that they can be used
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Recipe

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Tells flask to search for users by their ID

    return app


def create_database(app):
    if not path.exists('RecipePlanner/database.db'):
        with app.app_context():
            db.create_all()
        print('DB Created!')

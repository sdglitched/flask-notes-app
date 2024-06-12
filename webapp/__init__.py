from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webapp import sec_key as sck
from os import path


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = sck.sce_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note

    create_db(app)

    return app

def create_db(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app = app)

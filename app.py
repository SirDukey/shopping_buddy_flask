import os

from extensions import db
from flask import Flask
from routes import main
from utils import get_product_quantity


basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


def create_app(database_uri=DATABASE_URI):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.jinja_env.globals.update(get_product_quantity=get_product_quantity)

    db.init_app(app)

    app.register_blueprint(main)
    return app

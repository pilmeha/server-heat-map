from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

from app import routes, models

with app.app_context():
    db.create_all()

from flask_migrate import Migrate
migrate = Migrate(app, db)
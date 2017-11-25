from flask import Flask
from src.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
with app.app_context():
    db.create_all()

import src.urls
import src.db_populate
from src.db_populate import sched
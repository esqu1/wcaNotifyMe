from flask import Flask
from notifyme.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
with app.app_context():
    db.create_all()

import notifyme.views
import notifyme.db_populate
from notifyme.db_populate import sched
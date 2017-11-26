from flask import Flask
from notifyme.models import db
from mailer.models import mail, create_msg
import os

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
)
db.init_app(app)
mail.init_app(app)
with app.app_context():
    db.create_all()

import notifyme.views
import notifyme.db_populate
from notifyme.db_populate import sched
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=False, nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    comp = db.relationship('Competition', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        return '<Registration %r %r>' % (self.email, self.comp)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    website = db.Column(db.String, unique=True, nullable=True)
    open_time = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return '<Competition %r>' % self.name
from notifyme import app, db
from flask import request, jsonify, render_template
from .models import Registration, Competition
import re


@app.route('/')
def main():
    names = map(lambda x: x[0], db.session.query(Competition.name).all())
    return render_template('index.html', comps=names)


@app.route('/submitted', methods=['POST'])
def submit():
    if request.method == 'POST':
        if valid_email(request.form['email']):
            comp_name = request.form['comp_name']
            if comp_name == 'Select a competition':
                return jsonify({'error': 'No competition selected.'})
            with app.app_context():
                result = Competition.query.filter_by(name=comp_name).all()
                if len(result) <= 0:
                    return jsonify({'error': "Invalid competition name."})
                else:
                    s = db.session.query(Registration.email,
                                         Registration.comp_name).\
                        filter(Registration.email == request.form['email'],
                               Registration.comp_name == result[0].name).\
                        count()
                    if s == 0:
                        reg = Registration(email=request.form['email'],
                                           comp=result[0])
                        db.session.add(reg)
                        db.session.commit()
                        # TODO: add cron job for sending email
                        return jsonify({'result': 'OK'})
                    else:
                        return jsonify({'error': "You've already signed up!"})
        else:
            return jsonify({'error': "Invalid parameters."})
    else:
        return jsonify({'error': "GET method not supported."})


def valid_email(email):
    if email == '':
        return False
    return re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                    email) is not None

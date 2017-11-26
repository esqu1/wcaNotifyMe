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
            with app.app_context():
                result = Competition.query.filter_by(name=comp_name).all()
                if len(result) <= 0:
                    return jsonify({'error': "Invalid competition name."})
                else:
                    reg = Registration(email=request.form['email'],
                                       comp=result[0])
                    db.session.add(reg)
                    db.session.commit()
                    return jsonify({'result': 'OK'})
        else:
            return jsonify({'error': "Invalid parameters."})
    else:
        return jsonify({'error': "GET method not supported."})


def valid_email(email):
    if email == '':
        return False
    return re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                    email) is not None

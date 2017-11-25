from src import app, db
from flask import request, jsonify, render_template
from .models import Registration, Competition
import re


@app.route('/')
def main():
    # return rendering of home page
    return render_template('index.html')


@app.route('/submitted', methods=['POST'])
def submit():
    # will be an ajax request from the form, should return a response
    if request.method == 'POST':
        if valid_email(request.form['email']) and valid_comp(request.form['comp_name']):
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
    return re.match('[a-zA-Z0-9-+_]+@[a-zA-Z0-9-+_]+\.[a-zA-Z0-9-+_]+', email) is not None


def valid_comp(comp_name):
    return True

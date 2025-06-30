from flask import Blueprint, request, jsonify, session , render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

auth_bp = Blueprint('auth', __name__)
USER_DATA_FILE = 'users.json'

@auth_bp.route('/signup', methods=['GET'])
def show_signup_form():
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')



@auth_bp.route('/signup', methods=['POST'])
def signup() :
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('signup.html', error='Username and password required')


    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

    if username in users:
        return render_template('signup.html', error='User already exists')

    users[username] = generate_password_hash(password)

    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

    return render_template('upload.html' , username = username)



@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('login.html', error='Username and password required')

    if not os.path.exists(USER_DATA_FILE):
        return render_template('login.html', error='No users registered yet')

    with open(USER_DATA_FILE, 'r') as f:
        users = json.load(f)

    if username not in users or not check_password_hash(users[username], password):
        return render_template('login.html', error='Invalid credentials')

    session['username'] = username
    return render_template('upload.html', username=username)



@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200

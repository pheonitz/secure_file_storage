from flask import Flask, request, jsonify , render_template , redirect , session
import os
import json
from werkzeug.utils import secure_filename
from app.utils import hash_password
from flask import session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
DATA_FILE = os.path.join(PROJECT_ROOT, 'file_metadata.json')


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'file_metadata.json'

@app.route('/')
def home():
    return render_template('auth.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt', 'jpg', 'png'}


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect('/')

    username = session['username']

    if request.method == 'GET':
        return render_template('upload.html', username=username)

    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing file or password'}), 400

    file = request.files['file']
    password = request.form['password']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)

    # ✅ First define this:
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    # ✅ Then use it to make file path
    file_path = os.path.join(user_folder, filename)
    print("Saving to path:", file_path)

    # ✅ Save the file
    file.save(file_path)

    # ✅ Save metadata
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    if username not in data:
        data[username] = {}

    data[username][filename] = hash_password(password)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return render_template('upload.html', username=username, message=f'✅ File {filename} uploaded successfully!')

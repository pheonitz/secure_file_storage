from flask import Flask, request, jsonify , render_template
import os
import json
from werkzeug.utils import secure_filename
from app.utils import hash_password

app = Flask(__name__)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
DATA_FILE = os.path.join(PROJECT_ROOT, 'file_metadata.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'file_metadata.json'


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt', 'jpg', 'png'}

    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing file or password'}), 400

    file = request.files['file']
    password = request.form['password']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    hashed_pw = hash_password(password)

    # Save metadata to JSON (temporary storage)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[filename] = hashed_pw

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

    return jsonify({'message': f'File {filename} uploaded successfully'})

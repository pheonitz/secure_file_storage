from flask import Flask, request, jsonify
import os
import json
from werkzeug.utils import secure_filename
from app.utils import hash_password

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'file_metadata.json'

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing file or password'}), 400

    file = request.files['file']
    password = request.form['password']
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

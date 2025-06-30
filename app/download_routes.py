from flask import Blueprint, request, jsonify, send_file
import os
import json
from app.utils import verify_password

download_bp = Blueprint('download', __name__)

UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'file_metadata.json'

@download_bp.route('/download/<filename>', methods=['POST'])
def download_file(filename):
    password = request.form.get('password')

    if not password:
        return jsonify({'error': 'Password required'}), 400

    if not os.path.exists(DATA_FILE):
        return jsonify({'error': 'File not found'}), 404

    with open(DATA_FILE, 'r') as f:
        metadata = json.load(f)

    if filename not in metadata:
        return jsonify({'error': 'File not found in metadata'}), 404

    hashed = metadata[filename]
    if not verify_password(password, hashed):
        return jsonify({'error': 'Invalid password'}), 403

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 410

    return send_file(file_path, as_attachment=True)

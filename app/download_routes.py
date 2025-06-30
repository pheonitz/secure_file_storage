from flask import Blueprint, request, jsonify, send_file
import os
import json
from app.utils import verify_password
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

download_bp = Blueprint('download', __name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # go up to root
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
DATA_FILE = os.path.join(PROJECT_ROOT, 'file_metadata.json')



@download_bp.route('/download/<filename>', methods=['POST'])
def download_file(filename):
    filename = filename.strip()

    if filename not in metadata:
        print(f"❌ File '{filename}' not found in metadata")
        return jsonify({'error': 'File not found in metadata'}), 404

    hashed = metadata[filename]
    password = request.form.get('password')

    if not password:
        return jsonify({'error': 'Password required'}), 400

    if not verify_password(password, hashed):
        return jsonify({'error': 'Invalid password'}), 403

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 410

    return send_file(file_path, as_attachment=True)

from flask import Blueprint, request, render_template, send_file, session, redirect, url_for
import os
import json
from app.utils import verify_password
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)
download_bp = Blueprint('download', __name__)

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
DATA_FILE = os.path.join(PROJECT_ROOT, 'file_metadata.json')


@download_bp.route('/download/<filename>', methods=['POST'])
@limiter.limit("5 per minute")
def download_file(filename):
    if 'username' not in session:
        return render_template('upload.html', error="❌ Please log in to download files.")

    username = session['username']
    filename = filename.strip()

    # Check if metadata file exists
    if not os.path.exists(DATA_FILE):
        return render_template('upload.html', username=username, error="❌ No file metadata found.")

    with open(DATA_FILE, 'r') as f:
        metadata = json.load(f)

    # Check if user and file exist in metadata
    if username not in metadata or filename not in metadata[username]:
        return render_template('upload.html', username=username, error=f"❌ File '{filename}' not found.")

    password = request.form.get('password')
    if not password:
        return render_template('upload.html', username=username, error="❌ Password is required.")

    hashed = metadata[username][filename]
    if not verify_password(password, hashed):
        return render_template('upload.html', username=username, error="❌ Invalid password.")

    # Construct final path
    file_path = os.path.join(UPLOAD_FOLDER, username, filename)
    if not os.path.exists(file_path):
        return render_template('upload.html', username=username, error=f"❌ File not found on server at {file_path}")

    return send_file(file_path, as_attachment=True)

from app.utils import hash_password, verify_password
from flask import Flask
from app.routes import app as upload_app
from app.download_routes import download_bp

# Register the blueprint for download route
upload_app.register_blueprint(download_bp)

if __name__ == "__main__":
    upload_app.run(debug=True)

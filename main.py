from app.utils import hash_password, verify_password
from flask import Flask
from app.routes import app as upload_app
from app.download_routes import download_bp , limiter
from app.auth import auth_bp
import os


upload_app.secret_key = 'chaw'

upload_app.register_blueprint(auth_bp)


limiter.init_app(upload_app)

# Register the blueprint for download route
upload_app.register_blueprint(download_bp)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    upload_app.run(host="0.0.0.0", port=port)

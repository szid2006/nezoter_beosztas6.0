from flask import Flask
from .auth import auth
from .main import main

def create_app():
    app = Flask(__name__)
    app.secret_key = "nagyon_titkos"

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

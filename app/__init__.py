import os
from flask import Flask

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates")
    )

    app.secret_key = "nagyon_titkos"

    from .auth import auth
    from .main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

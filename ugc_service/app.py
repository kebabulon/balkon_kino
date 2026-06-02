import os
from flask import Flask

from .database import engine, close_db
from .routes import reviews_bp

def create_app(config=None):
    app = Flask(__name__)
    app.config["DJANGO_API_BASE_URL"] = os.getenv("DJANGO_API_BASE_URL", "http://127.0.0.1:8000/api")

    if config:
        app.config.update(config)

    app.register_blueprint(reviews_bp)
    app.teardown_appcontext(close_db)

    return app

app = create_app()

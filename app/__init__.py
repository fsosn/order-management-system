from flask import Flask
from .config import Config
from .routes import orders_bp
from .extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(orders_bp)

    return app

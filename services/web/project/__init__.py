import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('project.config.Config')
    db.init_app(app)

    # register blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .search import search_bp
    app.register_blueprint(search_bp)

    return app

from flask import Flask
from pathlib import Path
from .site import site
from .api import api

print("Hello from Init Script")

def create_app():


    app = Flask(__name__)

    from iscouttaskdispatch.database import db

    db_path = Path(app.instance_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path.absolute()}'
    app.config['FLASK_DB_SEEDS_PATH'] = (Path(app.root_path) / "./seeds.py").absolute()
    #app.config['SQLALCHEMY_ECHO'] = True  # Enable echoing of SQL statements

    # Initialize database with Flask SQLAlchemy or similar
    from .database import db
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(site)
    # Register API Blueprint if you have one
    app.register_blueprint(api)

    return app

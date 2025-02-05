from flask import Flask
from app.routes import setup_routes

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    setup_routes(app)
    return app

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.routes.chatbot_routes import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix="/api")

    return app

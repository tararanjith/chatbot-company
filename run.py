from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.chatbot_routes import chatbot_bp

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    app.run(port=3001, debug=True)

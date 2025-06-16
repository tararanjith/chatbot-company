from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.chatbot_routes import chatbot_bp
from config import logger  # ✅ Import the logger from your config

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    logger.info("Starting Flask server on port 3001...")
    app.run(port=3001, debug=True)

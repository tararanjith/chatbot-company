from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.routes import chatbot_bp
from config import logger  

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    logger.info("Starting Flask server on port 3001...")
    app.run(port=3001, debug=True)

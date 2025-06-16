from flask import Blueprint, request, jsonify
from app.services.chatbot_service import process_chat_request
from config import logger 

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat_route():
    try:
        data = request.get_json()
        logger.info(f"Received request data: {data}")  #  Log incoming request
        response = process_chat_request(data)
        logger.info(f"Sending response: {response}")  # Log outgoing response
        return jsonify(response), response.get("status_code", 200)
    except Exception as e:
        logger.exception("Error in chat_route")  # Logs traceback
        return jsonify({"message": "Internal server error"}), 500

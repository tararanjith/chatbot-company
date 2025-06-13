from flask import Blueprint, request, jsonify
from app.services.chatbot_service import process_chat_request

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat_route():
    data = request.get_json()
    response = process_chat_request(data)
    return jsonify(response), response.get("status_code", 200)

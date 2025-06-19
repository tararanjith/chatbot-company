from flask import Blueprint, request, jsonify
from app.services.chatbot_service import handle_chat_request, reset_session 

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat_route():
    return handle_chat_request(request)

@chatbot_bp.route("/api/reset-session", methods=["POST"])
def reset_session_route():
    return reset_session()

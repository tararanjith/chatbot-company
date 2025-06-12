from flask import Blueprint, request, jsonify
from app.services.chatbot_service import handle_chat

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat_route():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "").strip()

    response_data, new_session_id = handle_chat(user_message, session_id)

    # If there's an error in the data
    if "error" in response_data:
        return jsonify({"error": response_data["error"]}), 400

    # Return the response along with new session_id if needed
    return jsonify({
        "reply": response_data["reply"],
        "session_id": new_session_id  # could be None if not a new session
    })

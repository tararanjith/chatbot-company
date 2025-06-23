import uuid
import os
import json
import requests
from flask import request, make_response, jsonify
from dotenv import load_dotenv
from app.utils.helpers import load_website_data
from config import logger

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
website_data = load_website_data()
session_histories = {}

def build_response(text, session_id=None, is_new_session=False, status_code=200):
    return jsonify({
        "reply": text,
        "session_id": session_id if is_new_session else None
    }), status_code

def handle_chat_request(req):
    session_id = req.cookies.get("session_id")
    is_new_session = False

    if not session_id:
        session_id = str(uuid.uuid4())
        is_new_session = True
        logger.info(f"New session started: {session_id}")

    data = req.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        logger.warning("Empty message received.")
        return build_response("Message is required.", status_code=400)

    
    if session_id not in session_histories:
        session_histories[session_id] = []

    history = session_histories[session_id]
    history.append({"role": "user", "content": user_message})
    conversation_context = history[-10:]

    system_prompt = f"""You are Nova, a helpful assistant for Innovature.
Use only the following company information when answering questions:
{json.dumps(website_data, indent=2)}
If a question is not related to Innovature, respond with:
"I'm only able to answer questions related to Innovature and its services." after the user asks a question, make them feel free to ask more.
If you are not sure about a question related to Innovature, say you don't have that info and give the closest matching info.
Always reply briefly and factually. If the user greets you or thanks you, reply back politely. Give info in the most eye-catching way, so that the user is not bored.
reply in the following manner ,Simple questions: 1–2 sentences (15–30 words),Clarifications/help: 2–3 sentences (30–50 words),Support/fallback: Up to 4 sentences (max 75 words)
Keep it concise and avoid unnecessary filler. If the user claims to hold a position in the company, check the data and return the actual person's name holding the position after politely correcting them.
"""

    full_prompt = [{"role": "system", "content": system_prompt}] + conversation_context

    payload = {
        "model": "gpt-4o-mini",
        "messages": full_prompt
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            logger.exception("Failed to parse JSON from OpenRouter response")
            return build_response("Sorry, there was a problem understanding the server response.", session_id, is_new_session, 502)

        choices = data.get("choices")
        if not choices or not isinstance(choices, list):
            logger.warning("Missing or invalid 'choices' in OpenRouter response.")
            return build_response("Sorry, I didn't receive a proper response from the server.", session_id, is_new_session, 502)

        message = choices[0].get("message")
        if not message or "content" not in message:
            logger.warning("Missing 'message.content' in OpenRouter response.")
            return build_response("Sorry, the response content was incomplete.", session_id, is_new_session, 502)

        bot_reply = message["content"]
        logger.info(f"AI reply: {bot_reply[:100]}...")
        history.append({"role": "assistant", "content": bot_reply})

        final_response = build_response(bot_reply, session_id, is_new_session)
        response = make_response(final_response[0], final_response[1])
        if is_new_session:
            response.set_cookie("session_id", session_id, max_age=7*24*60*60)  # 7 days
        return response

 
    except requests.exceptions.HTTPError as e:
        logger.exception(f"HTTP error from OpenRouter: {e.response.status_code}")
        return build_response("Sorry, there was a server error while processing your request.", session_id, is_new_session, 502)

    except requests.exceptions.ConnectionError:
        logger.exception("Connection error with OpenRouter.")
        return build_response("Unable to connect to the server. Please check your internet connection or try again later.", session_id, is_new_session, 503)

    except requests.exceptions.Timeout:
        logger.exception("Request to OpenRouter timed out.")
        return build_response("The request took too long to respond. Please try again shortly.", session_id, is_new_session, 504)

    except requests.exceptions.RequestException:
        logger.exception("Unexpected error during OpenRouter API request.")
        return build_response("Sorry, something went wrong while talking to the server.", session_id, is_new_session, 500)



def reset_session():
    session_id = request.cookies.get("session_id")

    if session_id:
        if session_id in session_histories:
            del session_histories[session_id]
            logger.info(f"Session reset: {session_id} – Chat history cleared.")
        else:
            logger.info(f"Session reset requested: {session_id} – No active history found.")
    else:
        logger.info("Session reset requested – No session_id found in cookies.")

    response = make_response(jsonify({"message": "Session reset"}))
    response.set_cookie("session_id", "", max_age=0)  

    return response

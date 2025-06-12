import os
import json
import requests
import uuid
from dotenv import load_dotenv
from app.utils.helpers import load_website_data

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

website_data = load_website_data()
session_histories = {}

def handle_chat(user_message, session_id=None):
    user_message = user_message.strip() if user_message else ""
    session_id = session_id.strip() if session_id else ""

    if not user_message:
        return {"error": "Message is required."}, None

    is_new_session = False
    if not session_id:
        session_id = str(uuid.uuid4())
        is_new_session = True

    if session_id not in session_histories:
        session_histories[session_id] = []

    history = session_histories[session_id]

    # Extract company data
    about = website_data.get("about", "No about info.")
    services = ", ".join(website_data.get("services", []))
    industries = ", ".join(website_data.get("industries", []))
    contact = website_data.get("contact", {})
    address = contact.get("address", "Address not available.")
    email = contact.get("email", "Email not found.")
    phone = contact.get("phone", "Phone number not found.")
    socials = website_data.get("socials", {})
    vision = website_data.get("vision", "")
    mission = website_data.get("mission", "")
    offices = ", ".join(website_data.get("offices", []))
    core_values = ", ".join(website_data.get("core_values", []))
    wellbeing = website_data.get("employee_wellbeing", {})
    leadership = website_data.get("leadership_team", [])
    detailed_info = website_data.get("detailed_info", {})

    user_message_lower = user_message.lower()

    def build_response(text):
        return {
            "reply": text,
            "session_id": session_id if is_new_session else None
        }

    # Rule-based responses
    if any(k in user_message_lower for k in ["address", "located", "location"]):
        return build_response(f"Our address is: {address}"), session_id

    if any(k in user_message_lower for k in ["contact", "reach", "email"]):
        return build_response(f"You can reach us at {email}."), session_id

    if any(k in user_message_lower for k in ["phone", "call"]):
        return build_response(f"Our phone number is {phone}."), session_id

    if any(k in user_message_lower for k in ["social", "linkedin", "facebook", "twitter"]):
        links = "\n".join([f"{p.capitalize()}: {u}" for p, u in socials.items()])
        return build_response(f"Here are our social media links:\n{links}"), session_id

    if "vision" in user_message_lower and "mission" in user_message_lower:
        return build_response(f"Our vision is: {vision}\nOur mission is: {mission}"), session_id

    if "vision" in user_message_lower:
        return build_response(f"Our vision is: {vision}"), session_id

    if "mission" in user_message_lower:
        return build_response(f"Our mission is: {mission}"), session_id

    if any(k in user_message_lower for k in ["office", "offices"]):
        return build_response(f"Our offices are located in: {offices}."), session_id

    if any(k in user_message_lower for k in ["core values", "values", "principles"]):
        return build_response(f"Our core values are: {core_values}."), session_id

    if any(k in user_message_lower for k in ["wellbeing", "benefits", "perks", "employee welfare"]):
        desc = wellbeing.get("description", "")
        benefits = wellbeing.get("benefits", [])
        reply = f"{desc}\nWe provide: {', '.join(benefits)}."
        return build_response(reply), session_id

    

    if "leadership" in user_message_lower or "team" in user_message_lower:
        all_leaders = "\n".join([f'{m["name"]}, {m["position"]}' for m in leadership])
        return build_response(f"Our leadership team includes:\n{all_leaders}"), session_id

    if "ceo" in user_message_lower:
        if "global" in user_message_lower:
            ceo = next((m["name"] for m in leadership if "ceo, global" in m["position"].lower()), None)
            return build_response(f"The CEO of Innovature Global is {ceo}."), session_id
        elif "americas" in user_message_lower:
            ceo = next((m["name"] for m in leadership if "ceo, americas" in m["position"].lower()), None)
            return build_response(f"The CEO of Innovature Americas is {ceo}."), session_id
        else:
            ceos = [m["name"] for m in leadership if "ceo" in m["position"].lower()]
            return build_response(f"Our CEOs are {', '.join(ceos)}."), session_id

    for member in leadership:
        if member["name"].lower() in user_message_lower:
            session_histories[session_id + "_last_person"] = member["name"]
            return build_response(f"{member['name']} is our {member['position']}."), session_id

    # Detailed service info
    if any(k in user_message_lower for k in ["cloud solution", "cloud services", "cloud migration", "cloud native"]):
        return build_response(detailed_info.get("cloud_solutions", "Cloud services info not available.")), session_id

    if any(k in user_message_lower for k in ["digital transformation", "dx framework", "digital strategy", "modernization", "ai-led optimization"]):
        return build_response(detailed_info.get("digital_transformation", "Digital transformation info not available.")), session_id

    if any(k in user_message_lower for k in ["core ai services", "ai services", "artificial intelligence services", "ai and automation"]):
        return build_response(detailed_info.get("core_ai_services", "AI services info not available.")), session_id

    if any(k in user_message_lower for k in ["consulting", "startup growth", "offshore team scaling", "business support"]):
        return build_response(detailed_info.get("consulting", "Consulting info not found.")), session_id

    if any(k in user_message_lower for k in ["blog", "resource", "articles"]):
        return build_response("You can refer to the Blog section on our website to explore our latest articles and insights."), session_id

    # Fallback: call OpenRouter API
    history.append({"role": "user", "content": user_message})
    conversation_context = history[-10:]
    last_person = session_histories.get(session_id + "_last_person", "")

    system_prompt = f"""You are a helpful assistant for Innovature.
About: {about}
Services: {services}
Industries: {industries}
Contact Email: {email}
Contact Phone: {phone}
Address: {address}
Social Media: {', '.join([f'{k}: {v}' for k, v in socials.items()])}
Vision: {vision}
Mission: {mission}
Offices: {offices}
Core Values: {core_values}
Employee Wellbeing: {wellbeing.get('description', '')} Benefits include {', '.join(wellbeing.get('benefits', []))}.
Leadership Team: {', '.join([f"{m['name']} ({m['position']})" for m in leadership])}
Always try to keep your answers short and factual based on this company data. If the user says something like "hi", "hello", or "thanks", you can respond politely. But if they ask something unrelated to Innovature (like 'how to make coffee'), respond with:
"I'm only able to answer questions related to Innovature and its services." Remember previous questions to understand follow-ups.
"""
    if last_person:
        system_prompt += f"\nThe last mentioned person was {last_person}."

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
        data = response.json()

        choices = data.get("choices")
        if not choices or not isinstance(choices, list):
            return build_response("Sorry, the response format was unexpected."), session_id

        message = choices[0].get("message")
        if not message or "content" not in message:
            return build_response("Sorry, I couldn't understand the response."), session_id

        bot_reply = message["content"]
        history.append({"role": "assistant", "content": bot_reply})
        return build_response(bot_reply), session_id

    except requests.exceptions.RequestException as e:
        print("OpenRouter API error:", e)
        return build_response("Sorry, I'm having trouble processing your request right now."), session_id

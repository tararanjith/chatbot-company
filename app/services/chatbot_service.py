import os
import json
import requests
import uuid
from dotenv import load_dotenv
from app.utils.helpers import load_website_data
from config import logger

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

website_data = load_website_data()
session_histories = {}

def process_chat_request(data):
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "").strip()
    logger.info(f"Processing message: '{user_message}' | Session: {session_id or 'new session'}")

    if not user_message:
        logger.warning("Empty message received.")
        return {"error": "Message is required.", "status_code": 400}

    is_new_session = False
    if not session_id:
        session_id = str(uuid.uuid4())
        is_new_session = True
        logger.info(f"Started new session: {session_id}")

    if session_id not in session_histories:
        session_histories[session_id] = []

    history = session_histories[session_id]

    # Extract data from website.json
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

    def build_response(text):
        return {
            "reply": text,
            "session_id": session_id if is_new_session else None
        }

    msg = user_message.lower()

    # Rule-based responses
    if "located" in msg and any(k in msg for k in ["country", "countries", "in"]):
        logger.info("Matched rule: countries located in")
        return build_response(f"Our offices are located in: {offices}.")

    elif any(k in msg for k in ["address", "located", "location"]):
        logger.info("Matched rule: address")
        return build_response(f"Our address is: {address}")


    if any(k in msg for k in ["contact", "reach", "email"]):
        logger.info("Matched rule: email/contact")
        return build_response(f"You can reach us at {email}.")

    if any(k in msg for k in ["phone", "call"]):
        logger.info("Matched rule: phone")
        return build_response(f"Our phone number is {phone}.")

    if any(k in msg for k in ["social", "linkedin", "facebook", "twitter"]):
        logger.info("Matched rule: social links")
        links = "\n".join([f"{p.capitalize()}: {u}" for p, u in socials.items()])
        return build_response(f"Here are our social media links:\n{links}")

    if "vision" in msg and "mission" in msg:
        logger.info("Matched rule: vision and mission")
        return build_response(f"**Our Vision:** {vision}\n\n**Our Mission:** {mission}")
    if "vision" in msg:
        logger.info("Matched rule: vision")
        return build_response(f"**Our Vision:** {vision}")
    if "mission" in msg:
        logger.info("Matched rule: mission")
        return build_response(f"**Our Mission:** {mission}")

    if any(k in msg for k in ["core values", "values", "principles"]):
        logger.info("Matched rule: core values")
        return build_response(f"**Our Core Values:** {core_values}.")

    if any(k in msg for k in ["wellbeing", "benefits", "perks", "employee welfare"]):
        logger.info("Matched rule: employee wellbeing")
        desc = wellbeing.get("description", "")
        benefits = wellbeing.get("benefits", [])
        return build_response(f"{desc}\n\n**We provide:** {', '.join(benefits)}.")

    if "leadership" in msg or "team" in msg:
        logger.info("Matched rule: leadership team")
        all_leaders = "\n".join([f'- **{m["name"]}** – {m["position"]}' for m in leadership])
        return build_response(f"**Our leadership team includes:**\n\n{all_leaders}")

    if "ceo" in msg:
        logger.info("Matched rule: CEO")
        if "global" in msg:
            ceo = next((m["name"] for m in leadership if "ceo, global" in m["position"].lower()), None)
            session_histories[session_id + "_last_person"] = ceo
            return build_response(f"The CEO of Innovature Global is {ceo}.")
        elif "americas" in msg:
            ceo = next((m["name"] for m in leadership if "ceo, americas" in m["position"].lower()), None)
            session_histories[session_id + "_last_person"] = ceo
            return build_response(f"The CEO of Innovature Americas is {ceo}.")
        elif "india" in msg:
            ceo = next((m["name"] for m in leadership if "ceo, india" in m["position"].lower()), None)
            session_histories[session_id + "_last_person"] = ceo
            return build_response(f"The CEO of Innovature India is {ceo}.")
        else:
            ceos = [m["name"] for m in leadership if "ceo" in m["position"].lower()]
            if ceos:
                session_histories[session_id + "_last_person"] = ceos[0]
            return build_response(f"Our CEOs are {', '.join(ceos)}.")

    for member in leadership:
        if member["name"].lower() in msg:
            logger.info(f"Matched rule: name match for {member['name']}")
            session_histories[session_id + "_last_person"] = member["name"]
            return build_response(f"**{member['name']}** is our {member['position']}.")

    # Services and Consulting
    if any(k in msg for k in ["cloud solution", "cloud services", "cloud migration", "cloud native"]):
        logger.info("Matched rule: cloud services")
        return build_response(detailed_info.get("cloud_solutions", "Cloud services info not available."))

    if any(k in msg for k in ["digital transformation", "dx framework", "digital strategy", "modernization", "ai-led optimization"]):
        logger.info("Matched rule: digital transformation")
        return build_response(detailed_info.get("digital_transformation", "Digital transformation info not available."))

    if any(k in msg for k in ["core ai services", "ai services", "artificial intelligence services", "ai and automation"]):
        logger.info("Matched rule: AI services")
        return build_response(detailed_info.get("core_ai_services", "AI services info not available."))

    if any(k in msg for k in ["consulting", "startup growth", "offshore team scaling", "business support"]):
        logger.info("Matched rule: consulting")
        return build_response(detailed_info.get("consulting", "Consulting info not found."))

    if any(k in msg for k in ["blog", "resource", "articles"]):
        logger.info("Matched rule: blog/resources")
        return build_response("You can refer to the Blog section on our website to explore our latest articles and insights.")

    # AI fallback
    logger.info("No rule matched, using AI fallback")
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
Always try to keep your answers short and factual based on this company data. If the user says something like \"hi\", \"hello\", or \"thanks\", you can respond politely. But if they ask something unrelated to Innovature (like 'how to make coffee'), respond with:
\"I'm only able to answer questions related to Innovature and its services.\" Remember previous questions to understand follow-ups. Your name is Nova.
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
            logger.warning("Unexpected response format from OpenRouter.")
            return build_response("Sorry, the response format was unexpected.")
        message = choices[0].get("message")
        if not message or "content" not in message:
            logger.warning("Missing content in OpenRouter response.")
            return build_response("Sorry, I couldn't understand the response.")
        bot_reply = message["content"]
        logger.info(f"AI fallback reply: {bot_reply[:100]}...")
        history.append({"role": "assistant", "content": bot_reply})
        return build_response(bot_reply)

    except requests.exceptions.RequestException as e:
        logger.exception("OpenRouter API error")
        return build_response("Sorry, I'm having trouble processing your request right now.")
# AI Chatbot with Session-Based Memory

A modern, session-aware chatbot built with a **React frontend** and **Flask backend**, powered by the **OpenRouter API** using the `gpt-4o-mini` model. It supports follow-up questions, intelligent fallback responses, and a beautiful animated UI.

---

##  Tech Stack

- **Frontend**: React, Flexbox
- **Backend**: Python, Flask
- **AI Provider**: OpenRouter API (`gpt-4o-mini`)
- **Other Tools**: dotenv, logging, session-based memory

---

##  Features

-  Real-time chat interface with modern UI  
-  Session memory for contextual follow-up questions   
-  Graceful error handling for offline/API issues   
-  Fully responsive layout using **Flexbox + Media Queries** 
- **Reset Button** to clear the chat window and start fresh

---

##  Getting Started

### Backend Setup

1. Navigate to backend:
   cd backend

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Create a .env file with:
    OPENROUTER_API_KEY=your_api_key

5. Run the Flask server:
    python run.py

### Frontend Setup

1. Navigate to frontend:
    cd chatbot-frontend

2. Install dependencies:
    npm install

3. Start the frontend dev server:
    npm start







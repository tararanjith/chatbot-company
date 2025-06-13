// App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import aiImage from './assets/ai.png';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  useEffect(() => {
    const newSessionId = Date.now().toString();
    setSessionId(newSessionId);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await fetch('http://127.0.0.1:3001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: sessionId }),
      });

      const data = await response.json();
      const botMessage = { sender: 'bot', content: data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        sender: 'bot',
        content: '⚠️ Error: Could not reach the server.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="page-container">
      <header className="home-header">
  <div className="header-content">
    <img src="/logo.png" alt="Logo" className="header-logo" />
    <h2 className="header-title">Innovature</h2>
  </div>
</header>

      <section className="home-section">
        <img src={aiImage} alt="AI Background" className="hero-image" />
        <div className="overlay-text">
          <h1>Empowering Innovations with Artificial Intelligence</h1>
          <p>Unlocking Tomorrow</p>
        </div>
      </section>

      {/* Floating Chat Button */}
      <button className="chat-toggle" onClick={() => setIsChatOpen(!isChatOpen)}>💬</button>

      {/* Chat Container */}
      {isChatOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <img src="/logo.png" alt="Logo" className="logo" />
            <span>Nova Chatbot</span>
          </div>

          <div className="chat-box">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-bubble ${msg.sender}`}>
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            ))}
            {isTyping && (
              <div className="chat-bubble bot typing">
                <span className="typing-indicator">
                  <span></span><span></span><span></span>
                </span>
              </div>
            )}
          </div>

          <div className="chat-input-box">
            <input
              type="text"
              value={input}
              placeholder="Type your message..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

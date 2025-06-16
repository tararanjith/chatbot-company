import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import aiImage from './assets/ai.png';
import { RotateCcw } from 'lucide-react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);

  const messagesEndRef = useRef(null);
  const chatBoxRef = useRef(null);

  const generateSessionId = () => Date.now().toString();

  useEffect(() => {
    setSessionId(generateSessionId());
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const chatBox = chatBoxRef.current;
    if (!chatBox) return;

    const handleScroll = () => {
      const isAtBottom =
        chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight < 50;
      setShowScrollButton(!isAtBottom);
    };

    chatBox.addEventListener('scroll', handleScroll);
    return () => chatBox.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const resetChat = () => {
    setMessages([]);
    setSessionId(generateSessionId());
  };

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

      <button className="chat-toggle" onClick={() => setIsChatOpen(!isChatOpen)}>💬</button>

      {isChatOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <img src="/logo.png" alt="Logo" className="logo" />
            <span>Nova Chatbot</span>
            <button className="reset-icon" onClick={resetChat} title="Reset Chat">
              <RotateCcw size={20} strokeWidth={2} />
            </button>
          </div>

          <div className="chat-box" ref={chatBoxRef}>
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
            <div ref={messagesEndRef} />
          </div>

          {showScrollButton && (
            <button className="scroll-button" onClick={scrollToBottom} title="Scroll to bottom">
              ↓
            </button>
          )}

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

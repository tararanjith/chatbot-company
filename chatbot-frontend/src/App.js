import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import ChatToggle from './components/ChatToggle';
import ChatWindow from './components/ChatWindow';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const messagesEndRef = useRef(null);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const resetChat = async () => {
  setMessages([]);

  await fetch('http://localhost:3001/api/reset-session', {
    method: 'POST',
    credentials: 'include', 
  });
};


  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:3001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
        credentials: 'include' 
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
    <div className="app-container">
      <Header />
      <div className="main-content">
        <div className="left-section">
          <HeroSection />
        </div>
        <div className="right-section">
          <ChatToggle
            isChatOpen={isChatOpen}
            toggleChat={() => setIsChatOpen(!isChatOpen)}
          />
          {isChatOpen && (
            <ChatWindow
              messages={messages}
              isTyping={isTyping}
              resetChat={resetChat}
              chatBoxRef={chatBoxRef}
              messagesEndRef={messagesEndRef}
              input={input}
              setInput={setInput}
              sendMessage={sendMessage}
              handleKeyPress={handleKeyPress}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

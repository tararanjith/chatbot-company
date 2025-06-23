import { RotateCcw } from 'lucide-react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';

function ChatWindow({
  messages,
  isTyping,
  showScrollButton,
  scrollToBottom,
  resetChat,
  chatBoxRef,
  messagesEndRef,
  input,
  setInput,
  sendMessage,
  handleKeyPress,
}) {
  return (
    <div className="chat-container">
      <div className="chat-header">
        <img src="/logo.png" alt="Logo" className="logo" />
        <span>Nova Chatbot</span>
        <button
          className="reset-icon"
          onClick={resetChat}
          title="Reset Chat"
          aria-label="Reset chat"
        >
          <RotateCcw size={20} strokeWidth={2} />
        </button>
      </div>

      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} msg={msg} />
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
        <button
          className="scroll-button"
          onClick={scrollToBottom}
          title="Scroll to bottom"
        >
          ↓
        </button>
      )}

      <ChatInput
        input={input}
        setInput={setInput}
        sendMessage={sendMessage}
        handleKeyPress={handleKeyPress}
        isTyping={isTyping}
      />
    </div>
  );
}

export default ChatWindow;

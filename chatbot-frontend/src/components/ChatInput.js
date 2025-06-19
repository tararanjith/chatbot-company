function ChatInput({ input, setInput, sendMessage, handleKeyPress }) {
  const handleSend = () => {
    if (input.trim()) {
      sendMessage();
    }
  };

  return (
    <div className="chat-input-box">
      <input
        type="text"
        value={input}
        placeholder="Type your message..."
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        aria-label="Chat input"
      />
      <button onClick={handleSend} aria-label="Send message">Send</button>
    </div>
  );
}

export default ChatInput;

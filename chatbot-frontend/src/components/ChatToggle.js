import { MessageCircle } from 'lucide-react'; 

function ChatToggle({ isChatOpen, toggleChat }) {
  return (
    <button className="chat-toggle" onClick={toggleChat}>
      <MessageCircle size={24} />
    </button>
  );
}

export default ChatToggle;

import ReactMarkdown from 'react-markdown';

function MessageBubble({ msg }) {
  return (
    <div
      className={`chat-bubble ${msg.sender}`}
      role="textbox"
      aria-label={`${msg.sender === 'user' ? 'User' : 'Bot'} message`}
    >
      <ReactMarkdown>{msg.content}</ReactMarkdown>
    </div>
  );
}

export default MessageBubble;

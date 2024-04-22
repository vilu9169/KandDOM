import React from 'react';
import Markdown from 'marked-react'; // Assuming you're using Markdown

function ChatMessage({ text }) {
  // Parse Markdown into HTML
  const html = Markdown(text);

  return (
    <div className="chat-message" dangerouslySetInnerHTML={{ __html: html }} />
  );
}

export default ChatMessage;
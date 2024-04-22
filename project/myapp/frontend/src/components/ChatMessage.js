import React from 'react';
import { marked } from 'marked'; // Importing marked library

function ChatMessage({ text }) {
  // Parse Markdown into HTML
  const html = marked(text);

  return (
    <div className="chat-message" dangerouslySetInnerHTML={{ __html: html }} />
  );
}

export default ChatMessage;

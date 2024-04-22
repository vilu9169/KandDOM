import React from 'react';
import { marked } from 'marked'; // Importing marked library

function ChatMessage({ text }) {
  // Parse Markdown into HTML
  // Create a custom renderer
  const renderer = new marked.Renderer();

  // Override the heading renderer function to render headings with smaller font sizes
  renderer.heading = function (text, level) {
    if (level === 1) {
      return `<h${level} style="font-size: 1.5em;">${text}</h${level}>`;
    } else if (level === 2) {
      return `<h${level} style="font-size: 1.2em;">${text}</h${level}>`;
    } else {
      return `<h${level} style="font-size: 1.0em;">${text}</h${level}>`;
    }
  };

  // Set the custom renderer as an option for marked
  marked.setOptions({
    renderer: renderer
  });
  const html = marked(text);

  return (
    <div className="chat-message" dangerouslySetInnerHTML={{ __html: html }} />
  );
}

export default ChatMessage;

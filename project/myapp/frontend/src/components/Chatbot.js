import React, { useContext, useRef, useEffect } from 'react';
import { ResponseContext } from './ResponseContextProvider';
import PerfectScrollbar from 'perfect-scrollbar';
import 'perfect-scrollbar/css/perfect-scrollbar.css'; // Import Perfect Scrollbar CSS
import Markdown from 'marked-react';
import ChatMessage from './ChatMessage';

const Chatbot = () => {
  const { messages } = useContext(ResponseContext);
  const chatWindowRef = useRef(null);
  let ps;

  useEffect(() => {
    if (chatWindowRef.current) {
      ps = new PerfectScrollbar(chatWindowRef.current, {
        wheelPropagation: true // Example option, you can add more options here
      });
    }

    scrollToBottom();

    return () => {
      if (ps) {
        ps.destroy();
      }
    };
  }, []); // Only initialize PerfectScrollbar once on component mount

  useEffect(() => {
    updateScrollbar();
  }, [messages]); // Update scrollbar whenever messages change

  const updateScrollbar = () => {
      scrollToBottom(); // Scroll to bottom
  };

  const scrollToBottom = () => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight; // Set scroll position to bottom
    }
  };

  return (
    <div className="chatbot-container" ref={chatWindowRef}>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.user ? 'user-message' : 'ai-message'}`}
          >
            <p className='user-text'>{message.user ? 'You' : 'Pythia'}</p>
            <p className='message-text'><ChatMessage text={message.text} /></p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chatbot;

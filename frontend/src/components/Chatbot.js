import React, { useContext, useState } from 'react';
import axios from 'axios';
import { MessageContext } from './MessageContextProvider';
import { ResponseContext } from './ResponseContextProvider';

const Chatbot = () => {
  const {messages} = useContext(ResponseContext);

  return (
    <div className="chatbot-container position-absolute">
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.user ? 'user-message' : 'ai-message'}`}
          >
            <p className='user-text'>{message.user ? 'You' : 'Pythia'}</p>
            <p className='message-text'>{message.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Chatbot;
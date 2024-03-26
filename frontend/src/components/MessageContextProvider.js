import React, { createContext, useState } from 'react';
import { AppContext } from './ShowSettingsHandler';

const MessageContext = createContext();

const MessageContextProvider = ({ children }) => {
  const [message, setMessage]= useState('');

  return (
      <MessageContext.Provider value={{ message, setMessage }}>
          {children}
      </MessageContext.Provider>
  );
};

export { MessageContext, MessageContextProvider };
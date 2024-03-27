import React, { createContext, useState } from 'react';
import { AppContext } from './ShowSettingsHandler';

const ResponseContext = createContext();

const ResponseContextProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Fix the typo here

  return (
      <ResponseContext.Provider value={{ messages, setMessages }}> {/* Fix the typo here */}
          {children}
      </ResponseContext.Provider>
  );
};

export { ResponseContext, ResponseContextProvider};

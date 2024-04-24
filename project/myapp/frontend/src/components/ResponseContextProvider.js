import React, { createContext, useState, useContext } from 'react';
import { AppContext } from './ShowSettingsHandler';
import axios from 'axios';
const ResponseContext = createContext();

const ResponseContextProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Fix the typo here
  const { currentFile } = useContext(AppContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const getChatHistory = async (fileid) => {
    const body = {
      embedding_id: fileid ? fileid : currentFile
    };
    try {
      const { data } = await axios.post(baseURL + "api/getchat/", body);
      setMessages(data.messages);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
    }
  };
  return (
      <ResponseContext.Provider value={{ messages, setMessages, getChatHistory }}> {/* Fix the typo here */}
          {children}
      </ResponseContext.Provider>
  );
};

export { ResponseContext, ResponseContextProvider};

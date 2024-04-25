import React, { createContext, useState, useContext, useRef, createRef } from 'react';
import { AuthContext } from './AuthContextProvider';
import axios from 'axios';
const ResponseContext = createContext();

const ResponseContextProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Fix the typo here
  const [ pinnedMessages, setPinnedMessages ] = useState([]);
  const { currentFile } = useContext(AuthContext);
  const pinRef = useRef([]);
  const arrLength = pinnedMessages.length;
  
  if (pinRef.current.length !== arrLength) {
    // add or remove refs
    pinRef.current = Array(arrLength)
      .fill()
      .map((_, i) => pinRef.current[i] || createRef());
  }

  const baseURL = process.env.REACT_APP_API_URL;
  const getChatHistory = async (fileid) => {
    const body = {
      embedding_id: fileid ? fileid : currentFile
    };
    try {
      const { data } = await axios.post(baseURL + "api/getchat/", body);
      setMessages(data.messages);
      setPinnedMessages(data.pinned);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
    }
  };
  let contextData = {
    pinnedMessages: pinnedMessages,
    messages:messages,
    setMessages:setMessages,
    getChatHistory:getChatHistory,
    pinRef:pinRef,
  };
  return (
      <ResponseContext.Provider value={contextData}> {/* Fix the typo here */}
          {children}
      </ResponseContext.Provider>
  );
};

export { ResponseContext, ResponseContextProvider};

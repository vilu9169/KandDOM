import React, { createContext, useState, useContext, useEffect, createRef } from 'react';
import { AuthContext } from './AuthContextProvider';
import axios from 'axios';
const ResponseContext = createContext();

const ResponseContextProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Fix the typo here
  const [ pinnedMessages, setPinnedMessages ] = useState([]);
  const { currentFile } = useContext(AuthContext);
  const [ pinRef, setPinRef ] = useState([]);
  const arrLength = pinnedMessages.length;

  useEffect(() => {
    // add or remove refs
    setPinRef((pinRef) =>
      Array(arrLength)
        .fill()
        .map((_, i) => pinRef[i] || createRef()),
    );
  }, [arrLength]);

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

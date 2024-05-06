import React, { createContext, useState, useContext, useRef, createRef, useEffect } from 'react';
import { AuthContext } from './AuthContextProvider';
import axios from 'axios';
const ResponseContext = createContext();

const ResponseContextProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Fix the typo here
  const [ pinnedMessages, setPinnedMessages ] = useState([]);
  const { currentFile } = useContext(AuthContext);
  const pinRef = useRef([]);
  const arrLength = pinnedMessages.length;
  const { currentGroup } = useContext(AuthContext);
  useEffect(() => {
    // Ensure pinRef is properly populated when pinnedMessages change
    pinRef.current = Array(arrLength)
      .fill()
      .map((_, i) => pinRef.current[i] || createRef());
    console.log("pinRef.current", pinRef.current);
  }, [pinnedMessages]);

  const baseURL = process.env.REACT_APP_API_URL;


  /*const getChatHistory = async (fileid) => {
    const body = {
      embedding_id: fileid ? fileid : currentFile
    };
    try {
      const { data } = await axios.post(baseURL + "api/getchat/", body);
      setMessages(data.messages);
      let i = 0;
      for (const pin of data.pinned) {
        pin.index = i;
        i++;
      }
      setPinnedMessages(data.pinned);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
    }
  };*/


  const getChatHistory = async (fileid) => {
    const body = {
      embedding_id: fileid ? fileid : currentFile,
      group: currentGroup ? true : false,
    };
    let {data} = {};
    try {
      if (!currentGroup && !currentFile) {
        console.error("No file ID provided for fetching chat history");
        return;
      }
      else  {
        console.log("body", body);
        data = await axios.post(baseURL + "api/getchat/", body);
        setMessages(data.messages);
        console.log("data.pinned", data.pinned);
      }
  
      if (Array.isArray(data.pinned)) {
        const pins = data.pinned.map((pin, index) => ({ ...pin, index }));
        console.log("pinnedMessages", pins);
        setPinnedMessages(pins);
      } else {
        // Handle unexpected data format for pinned messages
        console.error('Unexpected data format for pinned messages:', data.pinned);
        setPinnedMessages([]);
      }
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
      setPinnedMessages([]);
    }
  };



  let contextData = {
    pinnedMessages: pinnedMessages,
    messages:messages,
    setMessages:setMessages,
    getChatHistory:getChatHistory,
    pinRef:pinRef,
    arrLength:arrLength
  };
  return (
      <ResponseContext.Provider value={contextData}> {/* Fix the typo here */}
          {children}
      </ResponseContext.Provider>
  );
};

export { ResponseContext, ResponseContextProvider};

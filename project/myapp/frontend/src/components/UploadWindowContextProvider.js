
import React, { createContext, useState } from 'react';


const UploadWindowContext = createContext();

const UploadWindowContextProvider = ({ children }) => {
  const [showUploadWindow, setShowUploadWindow] = useState(false);
  const {file, setFile} = useState(null);
  const handleShowUploadWindow = () => {
    setShowUploadWindow(!showUploadWindow);
  };
  


  return (
    <UploadWindowContext.Provider value={{ showUploadWindow, handleShowUploadWindow, setFile }}>
      {children}
    </UploadWindowContext.Provider>
  );
};

export { UploadWindowContext, UploadWindowContextProvider };
import React, { createContext, useState } from 'react';

const UploadWindowContext = createContext();

const UploadWindowContextProvider = ({ children }) => {
  const [showUploadWindow, setShowUploadWindow] = useState(true);
  const [file, setFile] = useState(null);
  const [value, setValue] = useState(0);

  const handleShowUploadWindow = (newValue) => {
    if (newValue !== value) {
      setShowUploadWindow(true);
    } else {
      setShowUploadWindow(prevShowUploadWindow => !prevShowUploadWindow); 
    }
    setValue(newValue);
  };

  return (
    <UploadWindowContext.Provider value={{ showUploadWindow, handleShowUploadWindow, setFile, value }}>
      {children}
    </UploadWindowContext.Provider>
  );
};

export { UploadWindowContext, UploadWindowContextProvider };

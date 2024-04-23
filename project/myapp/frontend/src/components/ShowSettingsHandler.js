
import React, { createContext, useState } from 'react';

const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleButtonClick = () => {
    setButtonClicked(!buttonClicked);
  };

  return (
    <AppContext.Provider value={{ buttonClicked, handleButtonClick }}>
      {children}
    </AppContext.Provider>
  );
};

export { AppContext, AppProvider };
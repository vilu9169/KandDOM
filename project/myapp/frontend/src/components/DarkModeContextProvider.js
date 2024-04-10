import React, { createContext, useState } from 'react';
import { AppContext } from './ShowSettingsHandler';

const DarkModeContext = createContext();

const DarkModeContextProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode]= useState(false);

  return (
      <DarkModeContext.Provider value={{ isDarkMode, setIsDarkMode }}>
          {children}
      </DarkModeContext.Provider>
  );
};

export { DarkModeContext, DarkModeContextProvider };
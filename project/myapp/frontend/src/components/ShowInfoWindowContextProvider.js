import React, { createContext, useState } from "react";

const showInfoWindowContext = createContext();


const ShowInfoWindowContextProvider = ({ children }) => {
    const [showInfoWindow, setShowInfoWindow] = useState(false);
    
    const handleShowInfo = () => {
        setShowInfoWindow(!showInfoWindow);
    }
    
    return (
        <showInfoWindowContext.Provider value={{ showInfoWindow, handleShowInfo }}>
        {children}
        </showInfoWindowContext.Provider>
    );
    }

export { showInfoWindowContext, ShowInfoWindowContextProvider };
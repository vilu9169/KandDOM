import React from 'react';

const LoadingScreen = (loadingText) => {
    return (
    <div className="spinner-container">
        <h2 className=' text-center'>{loadingText}</h2>
        <div className="spinner"></div>
    </div>
    );
};

export default LoadingScreen;
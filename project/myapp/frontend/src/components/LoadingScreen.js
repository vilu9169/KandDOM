import React from 'react';

const LoadingScreen = (props) => {
    return (
    <div className="spinner-container">
        <h2 className=' text-center'>{props.loadingText}</h2><br/>
        <div className="spinner"></div>
    </div>
    );
};

export default LoadingScreen;
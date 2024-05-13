import React from 'react';

const LoadingScreen = (props) => {
    return (
    <div className="m-auto p-2 h-75 bg-2 spinner-container">
        <h2 className=' text-center'>{props.loadingText}</h2><br/>
        <div className="spinner"></div>
    </div>
    );
};

export default LoadingScreen;
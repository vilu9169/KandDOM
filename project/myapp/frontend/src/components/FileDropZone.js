import React, { useState } from 'react';

const FileDropZone = ({ onFileUpload }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;

    // Upload files to the server
    onFileUpload(files);
  };

  return (
    <div
      className={`h-75 w-75 d-flex align-items-center justify-content-center file-drop-zone ${isDragging ? 'dragging' : ''}`}
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <p className='m-0 p-1'>Drag and drop files here</p>
    </div>
  );
};

export default FileDropZone;
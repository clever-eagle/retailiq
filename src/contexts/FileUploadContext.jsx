import React, { createContext, useContext, useState } from 'react';

// Create the context
const FileUploadContext = createContext();

// Custom hook to use the context
export const useFileUpload = () => {
  const context = useContext(FileUploadContext);
  if (!context) {
    throw new Error('useFileUpload must be used within a FileUploadProvider');
  }
  return context;
};

// Provider component
export const FileUploadProvider = ({ children }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const addFile = (file) => {
    setUploadedFiles(prev => [...prev, file]);
  };

  const updateFile = (fileId, updates) => {
    setUploadedFiles(prev => 
      prev.map(f => f.id === fileId ? { ...f, ...updates } : f)
    );
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const getSuccessfulFiles = () => {
    return uploadedFiles.filter(file => file.status === 'success');
  };

  const clearAllFiles = () => {
    setUploadedFiles([]);
  };

  const value = {
    uploadedFiles,
    addFile,
    updateFile,
    removeFile,
    getSuccessfulFiles,
    clearAllFiles,
    setUploadedFiles
  };

  return (
    <FileUploadContext.Provider value={value}>
      {children}
    </FileUploadContext.Provider>
  );
};

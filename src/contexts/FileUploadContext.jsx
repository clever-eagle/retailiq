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

// CSV parsing utility
const parseCSVContent = (csvContent) => {
  const lines = csvContent.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  
  const data = lines.slice(1).map((line, index) => {
    const values = line.split(',').map(v => v.trim());
    const row = { _rowIndex: index + 1 };
    
    headers.forEach((header, idx) => {
      row[header] = values[idx] || '';
    });
    
    return row;
  });
  
  return { headers, data, totalRows: data.length };
};

// Provider component
export const FileUploadProvider = ({ children }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [processedData, setProcessedData] = useState(null);

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
    setProcessedData(null);
  };

  // Process CSV file content
  const processCSVFile = async (file) => {
    try {
      const content = await file.text();
      const parsed = parseCSVContent(content);
      
      const processedFile = {
        ...file,
        parsed,
        processedAt: new Date().toISOString(),
        dataPreview: parsed.data.slice(0, 5) // First 5 rows for preview
      };
      
      setProcessedData(parsed);
      return processedFile;
    } catch (error) {
      console.error('Error processing CSV file:', error);
      throw new Error('Failed to process CSV file. Please check the file format.');
    }
  };

  const value = {
    uploadedFiles,
    processedData,
    addFile,
    updateFile,
    removeFile,
    getSuccessfulFiles,
    clearAllFiles,
    processCSVFile,
    setUploadedFiles
  };

  return (
    <FileUploadContext.Provider value={value}>
      {children}
    </FileUploadContext.Provider>
  );
};

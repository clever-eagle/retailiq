// File upload utilities for RetailIQ
export const validateFile = (file) => {
  const errors = [];
  
  // Check file type
  const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
  const allowedExtensions = ['.csv', '.xls', '.xlsx'];
  
  const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
  
  if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
    errors.push('Please upload a CSV or Excel file (.csv, .xls, .xlsx)');
  }
  
  // Check file size (max 10MB)
  const maxSize = 10 * 1024 * 1024; // 10MB in bytes
  if (file.size > maxSize) {
    errors.push('File size must be less than 10MB');
  }
  
  // Check if file is empty
  if (file.size === 0) {
    errors.push('File cannot be empty');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const getFileIcon = (fileName) => {
  const extension = fileName.toLowerCase().substring(fileName.lastIndexOf('.'));
  
  switch (extension) {
    case '.csv':
      return '📊';
    case '.xls':
    case '.xlsx':
      return '📗';
    default:
      return '📄';
  }
};

export const generateFileId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// File status constants
export const FILE_STATUS = {
  PENDING: 'pending',
  UPLOADING: 'uploading',
  SUCCESS: 'success',
  ERROR: 'error'
};

// Simulate file upload (replace with actual API call later)
export const simulateFileUpload = (file, onProgress) => {
  return new Promise((resolve, reject) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30;
      if (progress > 100) {
        progress = 100;
      }
      
      onProgress(Math.round(progress));
      
      if (progress >= 100) {
        clearInterval(interval);
        
        // Simulate random success/failure (90% success rate)
        if (Math.random() > 0.1) {
          setTimeout(() => resolve({
            success: true,
            message: 'File uploaded successfully',
            fileId: generateFileId()
          }), 500);
        } else {
          setTimeout(() => reject(new Error('Upload failed. Please try again.')), 500);
        }
      }
    }, 100);
  });
};

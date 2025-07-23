import React, { useState, useRef } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, X, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { validateFile, formatFileSize, getFileIcon, simulateFileUpload, FILE_STATUS } from '@/utils/fileUpload';

const UploadDialog = ({ trigger, onUploadComplete }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(Array.from(e.target.files));
    }
  };

  const handleFiles = (files) => {
    files.forEach(file => {
      const validation = validateFile(file);
      const fileId = Date.now().toString() + Math.random().toString(36).substr(2);
      
      const fileObj = {
        id: fileId,
        file,
        name: file.name,
        size: file.size,
        status: validation.isValid ? FILE_STATUS.PENDING : FILE_STATUS.ERROR,
        progress: 0,
        errors: validation.errors,
        uploadedAt: new Date()
      };
      
      setUploadedFiles(prev => [...prev, fileObj]);
      
      if (validation.isValid) {
        uploadFile(fileObj);
      }
    });
  };

  const uploadFile = async (fileObj) => {
    setUploadedFiles(prev => 
      prev.map(f => f.id === fileObj.id ? { ...f, status: FILE_STATUS.UPLOADING } : f)
    );

    try {
      await simulateFileUpload(fileObj.file, (progress) => {
        setUploadedFiles(prev => 
          prev.map(f => f.id === fileObj.id ? { ...f, progress } : f)
        );
      });

      setUploadedFiles(prev => 
        prev.map(f => f.id === fileObj.id ? { ...f, status: FILE_STATUS.SUCCESS, progress: 100 } : f)
      );

      if (onUploadComplete) {
        onUploadComplete(fileObj);
      }
    } catch (error) {
      setUploadedFiles(prev => 
        prev.map(f => f.id === fileObj.id ? { 
          ...f, 
          status: FILE_STATUS.ERROR, 
          errors: [error.message] 
        } : f)
      );
    }
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case FILE_STATUS.SUCCESS:
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case FILE_STATUS.ERROR:
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      case FILE_STATUS.UPLOADING:
        return <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />;
      default:
        return <FileText className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case FILE_STATUS.SUCCESS:
        return <Badge variant="default" className="bg-green-100 text-green-800 border-green-300">Success</Badge>;
      case FILE_STATUS.ERROR:
        return <Badge variant="destructive">Error</Badge>;
      case FILE_STATUS.UPLOADING:
        return <Badge variant="secondary" className="bg-blue-100 text-blue-800 border-blue-300">Uploading</Badge>;
      default:
        return <Badge variant="outline">Pending</Badge>;
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        {trigger}
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Upload Data File</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* Upload Area */}
          <div
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xls,.xlsx"
              onChange={handleChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="space-y-4">
              <div className="mx-auto w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                <Upload className="w-6 h-6 text-gray-600" />
              </div>
              
              <div>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  Drop your file here, or click to browse
                </p>
                <p className="text-sm text-gray-500">
                  Supports CSV and Excel files (max 10MB)
                </p>
              </div>
              
              <Button 
                type="button" 
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
              >
                Choose File
              </Button>
            </div>
          </div>

          {/* File List */}
          {uploadedFiles.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-medium text-gray-900">Uploaded Files</h4>
              <div className="space-y-3">
                {uploadedFiles.map((fileObj) => (
                  <div key={fileObj.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-3 flex-1 min-w-0">
                        <span className="text-lg">{getFileIcon(fileObj.name)}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {fileObj.name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatFileSize(fileObj.size)} • {fileObj.uploadedAt.toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(fileObj.status)}
                        {getStatusBadge(fileObj.status)}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFile(fileObj.id)}
                          className="h-6 w-6 p-0"
                        >
                          <X className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                    
                    {fileObj.status === FILE_STATUS.UPLOADING && (
                      <Progress value={fileObj.progress} className="mt-2" />
                    )}
                    
                    {fileObj.errors && fileObj.errors.length > 0 && (
                      <Alert variant="destructive" className="mt-2">
                        <AlertDescription>
                          {fileObj.errors.join(', ')}
                        </AlertDescription>
                      </Alert>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h5 className="font-medium text-blue-900 mb-2">Expected Data Format</h5>
            <div className="text-sm text-blue-800 space-y-1">
              <p>Your CSV should include these columns:</p>
              <ul className="list-disc list-inside space-y-1 ml-2">
                <li><strong>TransactionID:</strong> Unique transaction identifier</li>
                <li><strong>ProductID:</strong> Product identifier</li>
                <li><strong>ProductName:</strong> Name of the product</li>
                <li><strong>Category:</strong> Product category</li>
                <li><strong>Price:</strong> Unit price</li>
                <li><strong>Quantity:</strong> Quantity sold</li>
                <li><strong>Date:</strong> Transaction date (YYYY-MM-DD)</li>
                <li><strong>CustomerID:</strong> Customer identifier</li>
              </ul>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default UploadDialog;

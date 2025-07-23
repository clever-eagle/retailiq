import React, { useState, useRef, useEffect } from "react";
import { useFileUpload } from "@/contexts/FileUploadContext";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Upload,
  Download,
  FileText,
  CheckCircle,
  AlertCircle,
  Plus,
} from "lucide-react";
import UploadDialog from "@/components/UploadDialog";
import FileManager from "@/components/FileManager";
import AnalysisTypeSelector from "@/components/AnalysisTypeSelector";
import { downloadSampleCSV } from "@/utils/sampleData";
import {
  validateFile,
  formatFileSize,
  getFileIcon,
  FILE_STATUS,
} from "@/utils/fileUpload";
import { toast } from "sonner";
import apiService from "@/services/api";

function DataUpload() {
  const { uploadedFiles, addFile, updateFile, removeFile } = useFileUpload();
  const [dragActive, setDragActive] = useState(false);
  const [showAnalysisSelection, setShowAnalysisSelection] = useState(false);
  const fileInputRef = useRef(null);

  // Update analysis selection visibility when uploaded files change
  useEffect(() => {
    const successfulUploads = uploadedFiles.filter(
      (file) => file.status === FILE_STATUS.SUCCESS
    );
    setShowAnalysisSelection(successfulUploads.length > 0);
  }, [uploadedFiles]);

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
    files.forEach((file) => {
      const validation = validateFile(file);
      const fileId =
        Date.now().toString() + Math.random().toString(36).substr(2);

      const fileObj = {
        id: fileId,
        file,
        name: file.name,
        size: file.size,
        status: validation.isValid ? FILE_STATUS.PENDING : FILE_STATUS.ERROR,
        progress: 0,
        errors: validation.errors,
        uploadedAt: new Date(),
      };

      addFile(fileObj);

      if (validation.isValid) {
        uploadFile(fileObj);
      }
    });
  };

  const uploadFile = async (fileObj) => {
    updateFile(fileObj.id, { status: FILE_STATUS.UPLOADING });

    try {
      // Start progress at 10%
      updateFile(fileObj.id, { progress: 10 });

      // Upload to backend API
      const uploadResult = await apiService.uploadData(fileObj.file);

      // Update progress to 90%
      updateFile(fileObj.id, { progress: 90 });

      // Complete upload
      updateFile(fileObj.id, {
        status: FILE_STATUS.SUCCESS,
        progress: 100,
        backendResponse: uploadResult,
      });

      // Show success toast
      toast.success(`${fileObj.name} uploaded successfully!`, {
        description: "File is ready for analysis",
      });

      // Show analysis selection if we have successful uploads
      const hasSuccessfulUploads =
        uploadedFiles.some((f) => f.status === FILE_STATUS.SUCCESS) ||
        fileObj.status === FILE_STATUS.SUCCESS;
      if (hasSuccessfulUploads) {
        setShowAnalysisSelection(true);
      }
    } catch (error) {
      updateFile(fileObj.id, {
        status: FILE_STATUS.ERROR,
        errors: [error.message],
      });

      // Show error toast
      toast.error(`Failed to upload ${fileObj.name}`, {
        description: error.message,
      });
    }
  };

  const handleUploadComplete = (fileObj) => {
    setShowAnalysisSelection(true);
  };

  const handleRemoveFile = (fileId) => {
    removeFile(fileId);

    // Hide analysis selection if no successful uploads remain
    const remainingFiles = uploadedFiles.filter((f) => f.id !== fileId);
    const hasSuccessfulUploads = remainingFiles.some(
      (f) => f.status === FILE_STATUS.SUCCESS
    );
    if (!hasSuccessfulUploads) {
      setShowAnalysisSelection(false);
    }
  };

  const handleAnalysisSelect = (analysisType) => {
    console.log("Selected analysis:", analysisType);
    // Navigate to the appropriate analysis page
    // This will be implemented when we build the analysis pages
  };

  const successfulUploads = uploadedFiles.filter(
    (file) => file.status === FILE_STATUS.SUCCESS
  );

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Data Upload</h1>
          <p className="text-gray-600">
            Upload your retail sales data for AI-powered analysis
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Upload Dataset
            </h3>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  downloadSampleCSV();
                  toast.success("Sample CSV downloaded!", {
                    description: "Use this as a template for your data",
                  });
                }}
                className="flex items-center space-x-2"
              >
                <Download className="w-4 h-4" />
                <span>Download Sample</span>
              </Button>
              <UploadDialog
                trigger={
                  <Button variant="outline" size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    Quick Upload
                  </Button>
                }
                onUploadComplete={handleUploadComplete}
              />
            </div>
          </div>

          {/* Main Upload Area */}
          <div
            className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              dragActive
                ? "border-blue-500 bg-blue-50"
                : "border-gray-300 hover:border-gray-400"
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
              multiple
            />

            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
                <Upload className="w-8 h-8 text-gray-600" />
              </div>

              <div>
                <p className="text-xl font-medium text-gray-900 mb-2">
                  Drop your files here, or click to browse
                </p>
                <p className="text-gray-500 mb-4">
                  Supports CSV and Excel files (max 10MB each)
                </p>
              </div>

              <Button
                onClick={() => fileInputRef.current?.click()}
                className="mx-auto"
              >
                Choose Files
              </Button>
            </div>
          </div>
        </div>

        {/* File Management */}
        {uploadedFiles.length > 0 && (
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <FileManager
              files={uploadedFiles}
              onRemoveFile={handleRemoveFile}
              onViewFile={(file) => console.log("View file:", file)}
              onDownloadFile={(file) => console.log("Download file:", file)}
            />
          </div>
        )}

        {/* Analysis Type Selection */}
        {showAnalysisSelection && successfulUploads.length > 0 && (
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <AnalysisTypeSelector
              uploadedFiles={uploadedFiles}
              onAnalysisSelect={handleAnalysisSelect}
            />
          </div>
        )}

        {/* Data Format Guide */}
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h4 className="text-lg font-semibold text-blue-900 mb-3">
            Expected Data Format
          </h4>
          <div className="text-sm text-blue-800">
            <p className="mb-3">
              Your CSV file should include the following columns for optimal
              analysis:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h5 className="font-medium mb-2">Required Columns:</h5>
                <ul className="space-y-1">
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>TransactionID:</strong> Unique transaction
                    identifier
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>ProductID:</strong> Product identifier
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>ProductName:</strong> Name of the product
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>Date:</strong> Transaction date (YYYY-MM-DD)
                  </li>
                </ul>
              </div>
              <div>
                <h5 className="font-medium mb-2">Additional Columns:</h5>
                <ul className="space-y-1">
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>Category:</strong> Product category
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>Price:</strong> Unit price
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>Quantity:</strong> Quantity sold
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-3 h-3 mr-2 text-blue-600" />
                    <strong>CustomerID:</strong> Customer identifier
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataUpload;

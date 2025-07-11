import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { FileText, CheckCircle, AlertCircle, Trash2, Download, Eye } from 'lucide-react';
import { formatFileSize, getFileIcon, FILE_STATUS } from '@/utils/fileUpload';

const FileManager = ({ files, onRemoveFile, onViewFile, onDownloadFile }) => {
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
        return <Badge variant="default" className="bg-green-100 text-green-800 border-green-300">Ready</Badge>;
      case FILE_STATUS.ERROR:
        return <Badge variant="destructive">Error</Badge>;
      case FILE_STATUS.UPLOADING:
        return <Badge variant="secondary" className="bg-blue-100 text-blue-800 border-blue-300">Processing</Badge>;
      default:
        return <Badge variant="outline">Pending</Badge>;
    }
  };

  if (files.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
          <FileText className="w-6 h-6 text-gray-400" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No files uploaded</h3>
        <p className="text-gray-500 mb-4">Upload your first dataset to get started with analysis</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Uploaded Files</h3>
        <Badge variant="outline" className="text-xs">
          {files.length} file{files.length !== 1 ? 's' : ''}
        </Badge>
      </div>

      <div className="space-y-3">
        {files.map((fileObj) => (
          <div key={fileObj.id} className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <span className="text-2xl">{getFileIcon(fileObj.name)}</span>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-900 truncate">
                    {fileObj.name}
                  </h4>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-500">
                      {formatFileSize(fileObj.size)}
                    </span>
                    <span className="text-xs text-gray-500">
                      Uploaded {fileObj.uploadedAt.toLocaleDateString()} at {fileObj.uploadedAt.toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {getStatusIcon(fileObj.status)}
                {getStatusBadge(fileObj.status)}
              </div>
            </div>

            {fileObj.status === FILE_STATUS.UPLOADING && (
              <div className="mb-3">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                  <span>Uploading...</span>
                  <span>{fileObj.progress}%</span>
                </div>
                <Progress value={fileObj.progress} className="h-2" />
              </div>
            )}

            {fileObj.errors && fileObj.errors.length > 0 && (
              <Alert variant="destructive" className="mb-3">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {fileObj.errors.join(', ')}
                </AlertDescription>
              </Alert>
            )}

            {fileObj.status === FILE_STATUS.SUCCESS && (
              <div className="bg-green-50 border border-green-200 rounded-md p-3 mb-3">
                <div className="flex items-center text-sm text-green-800">
                  <CheckCircle className="w-4 h-4 mr-2" />
                  File uploaded successfully and ready for analysis
                </div>
              </div>
            )}

            {/* File Actions */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-100">
              <div className="flex items-center space-x-2">
                {fileObj.status === FILE_STATUS.SUCCESS && (
                  <>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onViewFile?.(fileObj)}
                      className="h-8"
                    >
                      <Eye className="w-3 h-3 mr-1" />
                      Preview
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onDownloadFile?.(fileObj)}
                      className="h-8"
                    >
                      <Download className="w-3 h-3 mr-1" />
                      Download
                    </Button>
                  </>
                )}
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemoveFile?.(fileObj.id)}
                className="h-8 text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="w-3 h-3 mr-1" />
                Remove
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileManager;

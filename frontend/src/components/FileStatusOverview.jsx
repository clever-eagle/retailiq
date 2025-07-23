import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FileText, Upload, CheckCircle, AlertCircle, Clock, Plus } from 'lucide-react';
import { formatFileSize, getFileIcon, FILE_STATUS } from '@/utils/fileUpload';
import UploadDialog from './UploadDialog';

const FileStatusOverview = ({ uploadedFiles, onUploadComplete }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case FILE_STATUS.SUCCESS:
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case FILE_STATUS.ERROR:
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      case FILE_STATUS.UPLOADING:
        return <Clock className="w-4 h-4 text-blue-600" />;
      default:
        return <FileText className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case FILE_STATUS.SUCCESS:
        return <Badge className="bg-green-100 text-green-800 border-green-300">Ready</Badge>;
      case FILE_STATUS.ERROR:
        return <Badge variant="destructive">Error</Badge>;
      case FILE_STATUS.UPLOADING:
        return <Badge className="bg-blue-100 text-blue-800 border-blue-300">Processing</Badge>;
      default:
        return <Badge variant="outline">Pending</Badge>;
    }
  };

  const successfulUploads = uploadedFiles.filter(file => file.status === FILE_STATUS.SUCCESS);
  const processingUploads = uploadedFiles.filter(file => file.status === FILE_STATUS.UPLOADING);
  const errorUploads = uploadedFiles.filter(file => file.status === FILE_STATUS.ERROR);

  const recentFiles = uploadedFiles
    .sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt))
    .slice(0, 5);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle className="text-lg font-semibold">Data Files</CardTitle>
        <UploadDialog
          trigger={
            <Button variant="outline" size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Upload
            </Button>
          }
          onUploadComplete={onUploadComplete}
        />
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* File Statistics */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 bg-green-50 rounded-lg border border-green-200">
              <div className="text-2xl font-bold text-green-700">{successfulUploads.length}</div>
              <div className="text-xs text-green-600">Ready</div>
            </div>
            <div className="text-center p-3 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-2xl font-bold text-blue-700">{processingUploads.length}</div>
              <div className="text-xs text-blue-600">Processing</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded-lg border border-red-200">
              <div className="text-2xl font-bold text-red-700">{errorUploads.length}</div>
              <div className="text-xs text-red-600">Errors</div>
            </div>
          </div>

          {/* Recent Files */}
          {recentFiles.length > 0 ? (
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Recent Uploads</h4>
              <div className="space-y-2">
                {recentFiles.map((file) => (
                  <div key={file.id} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3 flex-1 min-w-0">
                      <span className="text-lg">{getFileIcon(file.name)}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {file.name}
                        </p>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <span>{formatFileSize(file.size)}</span>
                          <span>•</span>
                          <span>{new Date(file.uploadedAt).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(file.status)}
                      {getStatusBadge(file.status)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="mx-auto w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-gray-400" />
              </div>
              <h3 className="text-sm font-medium text-gray-900 mb-2">No files uploaded yet</h3>
              <p className="text-xs text-gray-500 mb-4">Upload your retail data to get started</p>
              <UploadDialog
                trigger={
                  <Button size="sm">
                    <Upload className="w-4 h-4 mr-2" />
                    Upload First File
                  </Button>
                }
                onUploadComplete={onUploadComplete}
              />
            </div>
          )}

          {/* Quick Actions */}
          {successfulUploads.length > 0 && (
            <div className="pt-4 border-t border-gray-200">
              <h4 className="font-medium text-gray-900 mb-2">Quick Actions</h4>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm" className="flex-1">
                  Run Forecast
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  Market Analysis
                </Button>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FileStatusOverview;

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Upload, 
  TrendingUp, 
  ShoppingCart, 
  Download, 
  FileText, 
  BarChart3,
  ArrowRight,
  Zap
} from 'lucide-react';
import UploadDialog from './UploadDialog';

const QuickActionsCard = ({ uploadedFiles, onUploadComplete, onNavigate }) => {
  const successfulUploads = uploadedFiles.filter(file => file.status === 'success');
  const hasData = successfulUploads.length > 0;

  const quickActions = [
    {
      id: 'upload',
      title: 'Upload Data',
      description: 'Add new retail sales data',
      icon: Upload,
      variant: 'default',
      action: 'upload',
      available: true
    },
    {
      id: 'forecast',
      title: 'Sales Forecasting',
      description: 'Predict future sales trends',
      icon: TrendingUp,
      variant: hasData ? 'default' : 'outline',
      action: 'navigate',
      page: 'sales-forecasting',
      available: hasData
    },
    {
      id: 'basket',
      title: 'Market Basket Analysis',
      description: 'Find product associations',
      icon: ShoppingCart,
      variant: hasData ? 'default' : 'outline',
      action: 'navigate',
      page: 'market-basket-analysis',
      available: hasData
    },
    {
      id: 'reports',
      title: 'Export Reports',
      description: 'Download analysis results',
      icon: Download,
      variant: 'outline',
      action: 'export',
      available: hasData
    }
  ];

  const handleAction = (action) => {
    switch (action.action) {
      case 'navigate':
        if (onNavigate) {
          onNavigate(action.page);
        }
        break;
      case 'export':
        console.log('Export functionality will be implemented');
        break;
      default:
        break;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center">
          <Zap className="w-5 h-5 mr-2" />
          Quick Actions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {!hasData && (
            <Alert>
              <FileText className="h-4 w-4" />
              <AlertDescription>
                Upload your retail data to unlock analysis features.
              </AlertDescription>
            </Alert>
          )}

          <div className="grid grid-cols-1 gap-3">
            {quickActions.map((action) => {
              const Icon = action.icon;
              
              if (action.action === 'upload') {
                return (
                  <UploadDialog
                    key={action.id}
                    trigger={
                      <Button 
                        variant={action.variant} 
                        className="w-full justify-start h-auto p-4"
                        size="lg"
                      >
                        <div className="flex items-center space-x-3">
                          <Icon className="w-5 h-5" />
                          <div className="text-left">
                            <div className="font-medium">{action.title}</div>
                            <div className="text-xs opacity-80">{action.description}</div>
                          </div>
                        </div>
                        <ArrowRight className="w-4 h-4 ml-auto" />
                      </Button>
                    }
                    onUploadComplete={onUploadComplete}
                  />
                );
              }

              return (
                <Button
                  key={action.id}
                  variant={action.variant}
                  className="w-full justify-start h-auto p-4"
                  size="lg"
                  disabled={!action.available}
                  onClick={() => handleAction(action)}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className="w-5 h-5" />
                    <div className="text-left">
                      <div className="font-medium">{action.title}</div>
                      <div className="text-xs opacity-80">{action.description}</div>
                    </div>
                  </div>
                  {action.available && <ArrowRight className="w-4 h-4 ml-auto" />}
                </Button>
              );
            })}
          </div>

          {/* Data Summary */}
          {hasData && (
            <div className="pt-4 border-t border-gray-200">
              <h4 className="font-medium text-gray-900 mb-2">Available Data</h4>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {successfulUploads.length} file{successfulUploads.length !== 1 ? 's' : ''} ready for analysis
                </span>
                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                  <BarChart3 className="w-3 h-3 mr-1" />
                  Ready
                </Badge>
              </div>
            </div>
          )}

          {/* Analysis Tips */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <h5 className="font-medium text-blue-900 mb-1">Analysis Tips</h5>
            <ul className="text-xs text-blue-800 space-y-1">
              <li>• Sales Forecasting works best with 3+ months of data</li>
              <li>• Market Basket Analysis requires transaction IDs</li>
              <li>• Upload multiple files to compare periods</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default QuickActionsCard;

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card } from '@/components/ui/card';
import { TrendingUp, ShoppingCart, ArrowRight, Info } from 'lucide-react';

const AnalysisTypeSelector = ({ uploadedFiles, onAnalysisSelect }) => {
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);

  const analysisTypes = [
    {
      id: 'sales-forecasting',
      title: 'Sales Forecasting',
      description: 'Predict future sales trends using historical data',
      icon: TrendingUp,
      features: [
        'Time-series forecasting using Prophet',
        'Product-specific predictions',
        'Seasonal trend analysis',
        'Confidence intervals'
      ],
      requirements: ['Product', 'Date', 'Quantity', 'Price'],
      color: 'blue'
    },
    {
      id: 'market-basket-analysis',
      title: 'Market Basket Analysis',
      description: 'Discover product associations and buying patterns',
      icon: ShoppingCart,
      features: [
        'Association rule mining',
        'Product bundling recommendations',
        'Cross-selling insights',
        'Customer behavior patterns'
      ],
      requirements: ['TransactionID', 'Product', 'Category'],
      color: 'green'
    }
  ];

  const handleAnalysisSelect = (analysisType) => {
    setSelectedAnalysis(analysisType);
  };

  const handleProceed = () => {
    if (selectedAnalysis && onAnalysisSelect) {
      onAnalysisSelect(selectedAnalysis);
    }
  };

  const successfulUploads = uploadedFiles.filter(file => file.status === 'success');

  if (successfulUploads.length === 0) {
    return (
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          Please upload at least one data file before selecting an analysis type.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Choose Analysis Type
        </h3>
        <p className="text-gray-600">
          Select the type of analysis you want to perform on your uploaded data.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {analysisTypes.map((analysis) => {
          const Icon = analysis.icon;
          const isSelected = selectedAnalysis?.id === analysis.id;
          
          return (
            <Card 
              key={analysis.id}
              className={`p-6 cursor-pointer transition-all border-2 ${
                isSelected 
                  ? analysis.color === 'blue' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-green-500 bg-green-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => handleAnalysisSelect(analysis)}
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className={`p-3 rounded-lg ${
                    analysis.color === 'blue' ? 'bg-blue-100' : 'bg-green-100'
                  }`}>
                    <Icon className={`w-6 h-6 ${
                      analysis.color === 'blue' ? 'text-blue-600' : 'text-green-600'
                    }`} />
                  </div>
                  {isSelected && (
                    <Badge className={
                      analysis.color === 'blue' 
                        ? 'bg-blue-500 hover:bg-blue-600' 
                        : 'bg-green-500 hover:bg-green-600'
                    }>
                      Selected
                    </Badge>
                  )}
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    {analysis.title}
                  </h4>
                  <p className="text-gray-600 text-sm mb-4">
                    {analysis.description}
                  </p>
                </div>

                <div className="space-y-3">
                  <div>
                    <h5 className="text-sm font-medium text-gray-900 mb-2">Features:</h5>
                    <ul className="space-y-1">
                      {analysis.features.map((feature, index) => (
                        <li key={index} className="text-xs text-gray-600 flex items-center">
                          <div className={`w-1.5 h-1.5 rounded-full mr-2 ${
                            analysis.color === 'blue' ? 'bg-blue-400' : 'bg-green-400'
                          }`} />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h5 className="text-sm font-medium text-gray-900 mb-2">Required columns:</h5>
                    <div className="flex flex-wrap gap-1">
                      {analysis.requirements.map((req, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {req}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {selectedAnalysis && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">
                Ready to proceed with {selectedAnalysis.title}
              </h4>
              <p className="text-sm text-gray-600 mt-1">
                Using {successfulUploads.length} uploaded file{successfulUploads.length !== 1 ? 's' : ''}
              </p>
            </div>
            <Button onClick={handleProceed} className="flex items-center space-x-2">
              <span>Start Analysis</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Data Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">Uploaded Data Summary</h4>
        <div className="space-y-2">
          {successfulUploads.map((file, index) => (
            <div key={file.id} className="flex items-center justify-between text-sm">
              <span className="text-blue-800">{file.name}</span>
              <Badge variant="outline" className="bg-white">
                Ready for analysis
              </Badge>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisTypeSelector;

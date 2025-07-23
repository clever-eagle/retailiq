import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown } from 'lucide-react';

const SimpleLineChart = ({ data, title, color = 'blue' }) => {
  if (!data || data.length === 0) return null;

  const maxValue = Math.max(...data);
  const minValue = Math.min(...data);
  const range = maxValue - minValue;

  // Create SVG path for the line
  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * 100;
    const y = 100 - ((value - minValue) / range) * 100;
    return `${x},${y}`;
  }).join(' ');

  const trend = data[data.length - 1] > data[0];
  const trendPercentage = ((data[data.length - 1] - data[0]) / data[0] * 100).toFixed(1);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900">{title}</h4>
        <div className="flex items-center space-x-1">
          {trend ? (
            <TrendingUp className="w-3 h-3 text-green-600" />
          ) : (
            <TrendingDown className="w-3 h-3 text-red-600" />
          )}
          <span className={`text-xs ${trend ? 'text-green-600' : 'text-red-600'}`}>
            {Math.abs(trendPercentage)}%
          </span>
        </div>
      </div>
      
      <div className="relative">
        <svg
          viewBox="0 0 100 40"
          className="w-full h-16"
          preserveAspectRatio="none"
        >
          <polyline
            fill="none"
            stroke={color === 'blue' ? '#3b82f6' : '#10b981'}
            strokeWidth="2"
            points={points}
          />
          {/* Fill area under the line */}
          <polygon
            fill={color === 'blue' ? '#3b82f6' : '#10b981'}
            fillOpacity="0.1"
            points={`0,100 ${points} 100,100`}
          />
        </svg>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500">
        <span>{data[0]?.toLocaleString()}</span>
        <span>{data[data.length - 1]?.toLocaleString()}</span>
      </div>
    </div>
  );
};

const ForecastChart = ({ forecastData }) => {
  if (!forecastData) return null;

  const { dates, actual, predicted } = forecastData;
  const combinedData = [...actual, ...predicted];
  const maxValue = Math.max(...combinedData);
  const minValue = Math.min(...combinedData);
  const range = maxValue - minValue;

  // Split point between actual and predicted
  const splitIndex = actual.length;

  const createPoints = (data, startIndex = 0) => {
    return data.map((value, index) => {
      const x = ((startIndex + index) / (combinedData.length - 1)) * 100;
      const y = 100 - ((value - minValue) / range) * 100;
      return `${x},${y}`;
    }).join(' ');
  };

  const actualPoints = createPoints(actual);
  const predictedPoints = createPoints(predicted, splitIndex);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center justify-between">
          Sales Forecast Trend
          <Badge variant="outline" className="bg-blue-50 text-blue-700">
            14-day prediction
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="relative">
            <svg
              viewBox="0 0 100 40"
              className="w-full h-24"
              preserveAspectRatio="none"
            >
              {/* Actual data line */}
              <polyline
                fill="none"
                stroke="#3b82f6"
                strokeWidth="2"
                points={actualPoints}
              />
              
              {/* Predicted data line */}
              <polyline
                fill="none"
                stroke="#10b981"
                strokeWidth="2"
                strokeDasharray="4,2"
                points={predictedPoints}
              />
              
              {/* Fill area under actual line */}
              <polygon
                fill="#3b82f6"
                fillOpacity="0.1"
                points={`0,100 ${actualPoints} ${(splitIndex / (combinedData.length - 1)) * 100},100`}
              />
              
              {/* Fill area under predicted line */}
              <polygon
                fill="#10b981"
                fillOpacity="0.1"
                points={`${(splitIndex / (combinedData.length - 1)) * 100},100 ${predictedPoints} 100,100`}
              />
            </svg>
          </div>
          
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-0.5 bg-blue-500"></div>
                <span className="text-gray-600">Actual</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-0.5 bg-green-500 border-dashed border border-green-500"></div>
                <span className="text-gray-600">Predicted</span>
              </div>
            </div>
            <div className="text-gray-500">
              Last 30 days + Next 14 days
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-2 border-t border-gray-200">
            <div className="text-center">
              <p className="text-lg font-bold text-gray-900">
                {actual[actual.length - 1]?.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Current</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-green-600">
                {predicted[predicted.length - 1]?.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">14-day forecast</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-blue-600">
                {(((predicted[predicted.length - 1] - actual[actual.length - 1]) / actual[actual.length - 1]) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-gray-500">Expected growth</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export { SimpleLineChart, ForecastChart };

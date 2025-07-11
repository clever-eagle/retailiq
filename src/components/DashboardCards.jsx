import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Users, Package } from 'lucide-react';

const MetricCard = ({ title, value, change, changeType, icon: Icon, subtitle }) => {
  const isPositive = changeType === 'positive' || change > 0;
  const TrendIcon = isPositive ? TrendingUp : TrendingDown;
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">
          {title}
        </CardTitle>
        <Icon className="h-4 w-4 text-gray-400" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-gray-900">{value}</div>
        {change !== undefined && (
          <div className="flex items-center mt-1">
            <TrendIcon className={`h-3 w-3 mr-1 ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`} />
            <span className={`text-xs ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}>
              {Math.abs(change)}%
            </span>
            <span className="text-xs text-gray-500 ml-1">from last month</span>
          </div>
        )}
        {subtitle && (
          <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
        )}
      </CardContent>
    </Card>
  );
};

const SalesOverviewCard = ({ salesData }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Sales Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-2xl font-bold text-gray-900">
                ${salesData.totalRevenue.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500">Total Revenue</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {salesData.totalTransactions.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500">Transactions</p>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Top Performing Products</h4>
            <div className="space-y-2">
              {salesData.topProducts?.slice(0, 3).map((product, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className="text-xs">
                      #{index + 1}
                    </Badge>
                    <span className="text-sm text-gray-700">{product.name}</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      ${product.revenue.toLocaleString()}
                    </p>
                    <p className="text-xs text-green-600">+{product.growth}%</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const AnalysisResultsCard = ({ recentAnalyses }) => {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-800 border-green-300">Completed</Badge>;
      case 'running':
        return <Badge className="bg-blue-100 text-blue-800 border-blue-300">Running</Badge>;
      case 'failed':
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Recent Analysis Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {recentAnalyses.slice(0, 3).map((analysis) => (
            <div key={analysis.id} className="border border-gray-200 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900">{analysis.type}</h4>
                {getStatusBadge(analysis.status)}
              </div>
              <p className="text-sm text-gray-600 mb-2">{analysis.results.summary}</p>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Confidence: {analysis.results.confidence}%</span>
                <span>{new Date(analysis.date).toLocaleDateString()}</span>
              </div>
              {analysis.results.keyInsight && (
                <div className="mt-2 p-2 bg-blue-50 rounded border border-blue-200">
                  <p className="text-xs text-blue-800">
                    <strong>Key Insight:</strong> {analysis.results.keyInsight}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

const MarketBasketCard = ({ basketData }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Market Basket Insights</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Top Product Associations</h4>
            <div className="space-y-2">
              {basketData.associations.slice(0, 3).map((rule, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-1">
                    <div className="text-sm">
                      <span className="font-medium text-gray-900">
                        {rule.antecedent.join(' + ')}
                      </span>
                      <span className="text-gray-500 mx-2">→</span>
                      <span className="font-medium text-blue-600">
                        {rule.consequent.join(', ')}
                      </span>
                    </div>
                    <Badge variant="outline" className="text-xs">
                      {(rule.confidence * 100).toFixed(0)}%
                    </Badge>
                  </div>
                  <div className="flex space-x-4 text-xs text-gray-500">
                    <span>Support: {(rule.support * 100).toFixed(1)}%</span>
                    <span>Lift: {rule.lift.toFixed(1)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Frequent Itemsets</h4>
            <div className="flex flex-wrap gap-2">
              {basketData.frequentItemsets.slice(0, 4).map((itemset, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {itemset.items.join(' + ')} ({itemset.frequency})
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export {
  MetricCard,
  SalesOverviewCard,
  AnalysisResultsCard,
  MarketBasketCard
};

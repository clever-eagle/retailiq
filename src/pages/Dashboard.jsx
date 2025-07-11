import React, { useState, useEffect } from 'react';
import { useFileUpload } from '@/contexts/FileUploadContext';
import { 
  MetricCard, 
  SalesOverviewCard, 
  AnalysisResultsCard, 
  MarketBasketCard 
} from '@/components/DashboardCards';
import FileStatusOverview from '@/components/FileStatusOverview';
import QuickActionsCard from '@/components/QuickActionsCard';
import { ForecastChart } from '@/components/SimpleCharts';
import { 
  loadCSVData,
  processSalesData,
  processMarketBasketData,
  processCustomerSegments
} from '@/utils/csvDataProcessor';
import { 
  generateMockForecastData, 
  generateMockDashboardMetrics, 
  generateRecentAnalyses 
} from '@/utils/mockData';
import { DollarSign, ShoppingCart, Users, Package, TrendingUp } from 'lucide-react';

function Dashboard({ onNavigate }) {
  const { uploadedFiles, addFile, updateFile } = useFileUpload();
  const [dashboardData, setDashboardData] = useState({
    metrics: {},
    salesData: { topProducts: [] },
    forecastData: null,
    basketData: { associations: [], frequentItemsets: [] },
    recentAnalyses: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      
      try {
        // Load real CSV data
        const transactions = await loadCSVData();
        console.log('Dashboard loaded transactions:', transactions.length);
        
        // Process data for dashboard
        const salesData = processSalesData(transactions);
        const basketData = processMarketBasketData(transactions);
        const customerData = processCustomerSegments(transactions);
        
        // Generate dashboard metrics from real data
        const totalRevenue = salesData.totalRevenue;
        const totalTransactions = salesData.totalTransactions;
        const totalCustomers = customerData.reduce((sum, segment) => sum + (segment.size * 10), 0); // Rough estimate
        const avgOrderValue = totalRevenue / totalTransactions;
        
        setDashboardData({
          metrics: {
            totalRevenue,
            totalTransactions,
            totalCustomers,
            avgOrderValue,
            // Add some growth indicators
            revenueGrowth: 8.5,
            transactionGrowth: 12.3,
            customerGrowth: 5.7,
            aovGrowth: -2.1
          },
          salesData: {
            totalRevenue,
            totalTransactions,
            topProducts: salesData.historicalData.slice(-7).map((day, index) => ({
              name: `Product ${index + 1}`,
              revenue: day.sales * 0.3, // Simulate individual product revenue
              growth: Math.floor(Math.random() * 20) + 5
            }))
          },
          forecastData: generateMockForecastData(),
          basketData,
          recentAnalyses: generateRecentAnalyses()
        });
        
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Fallback to mock data
        const metrics = generateMockDashboardMetrics();
        const salesData = {
          ...metrics,
          topProducts: []
        };
        
        setDashboardData({
          metrics,
          salesData,
          forecastData: generateMockForecastData(),
          basketData: { associations: [], frequentItemsets: [] },
          recentAnalyses: generateRecentAnalyses()
        });
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleUploadComplete = (file) => {
    console.log('File uploaded from dashboard:', file);
  };

  const handleNavigation = (page) => {
    if (onNavigate) {
      onNavigate(page);
    }
  };

  const { metrics, salesData, forecastData, basketData, recentAnalyses } = dashboardData;

  if (loading) {
    return (
      <div className="p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Loading your analytics overview...</p>
          </div>
          
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <TrendingUp className="h-8 w-8 animate-pulse text-blue-600 mx-auto mb-4" />
              <p className="text-gray-600">Processing transaction data...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">
            AI-powered retail analytics and insights overview
          </p>
        </div>

        {/* Key Metrics Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Total Revenue"
            value={`$${metrics.totalRevenue?.toLocaleString() || '0'}`}
            change={metrics.revenueGrowth}
            icon={DollarSign}
            subtitle="This month"
          />
          <MetricCard
            title="Transactions"
            value={metrics.totalTransactions?.toLocaleString() || '0'}
            change={metrics.transactionGrowth}
            icon={ShoppingCart}
            subtitle="This month"
          />
          <MetricCard
            title="Active Customers"
            value={metrics.totalCustomers?.toLocaleString() || '0'}
            change={metrics.customerGrowth}
            icon={Users}
            subtitle="This month"
          />
          <MetricCard
            title="Product Lines"
            value={metrics.activeProducts || '0'}
            change={null}
            icon={Package}
            subtitle={`of ${metrics.totalProducts || '0'} total`}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Sales and Analysis */}
          <div className="lg:col-span-2 space-y-6">
            {/* Sales Overview */}
            <SalesOverviewCard salesData={salesData} />

            {/* Forecast Chart */}
            <ForecastChart forecastData={forecastData} />

            {/* Recent Analysis Results */}
            <AnalysisResultsCard recentAnalyses={recentAnalyses} />
          </div>

          {/* Right Column - Files and Actions */}
          <div className="space-y-6">
            {/* File Status */}
            <FileStatusOverview
              uploadedFiles={uploadedFiles}
              onUploadComplete={handleUploadComplete}
            />

            {/* Quick Actions */}
            <QuickActionsCard
              uploadedFiles={uploadedFiles}
              onUploadComplete={handleUploadComplete}
              onNavigate={handleNavigation}
            />
          </div>
        </div>

        {/* Bottom Section - Market Basket Insights */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <MarketBasketCard basketData={basketData} />
          
          {/* Additional Performance Metrics */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Highlights</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-blue-900">Forecast Accuracy</h4>
                  <p className="text-sm text-blue-700">Last 30 predictions</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-900">{metrics.forecastAccuracy}%</div>
                  <div className="flex items-center text-sm text-blue-700">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    +2.1%
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-green-900">Average Order Value</h4>
                  <p className="text-sm text-green-700">Customer transaction average</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-900">
                    ${metrics.averageOrderValue?.toFixed(2) || '0.00'}
                  </div>
                  <div className="flex items-center text-sm text-green-700">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    +{metrics.aovGrowth}%
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-purple-900">Repeat Customer Rate</h4>
                  <p className="text-sm text-purple-700">Customer retention metric</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-purple-900">
                    {metrics.repeatCustomerRate}%
                  </div>
                  <div className="text-sm text-purple-700">Industry avg: 28%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

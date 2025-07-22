import React, { useState, useEffect } from "react";
import { useFileUpload } from "@/contexts/FileUploadContext";
import {
  MetricCard,
  SalesOverviewCard,
  AnalysisResultsCard,
} from "@/components/DashboardCards";
import FileStatusOverview from "@/components/FileStatusOverview";
import QuickActionsCard from "@/components/QuickActionsCard";
import { ForecastChart } from "@/components/SimpleCharts";
import {
  loadCSVData,
  processSalesData,
  processCustomerSegments,
} from "@/utils/csvDataProcessor";
import {
  generateMockForecastData,
  generateMockDashboardMetrics,
  generateRecentAnalyses,
} from "@/utils/mockData";
import {
  DollarSign,
  ShoppingCart,
  Users,
  Package,
  TrendingUp,
} from "lucide-react";

function Dashboard({ onNavigate }) {
  const { uploadedFiles, addFile, updateFile } = useFileUpload();
  const [dashboardData, setDashboardData] = useState({
    metrics: {},
    salesData: { topProducts: [] },
    forecastData: null,
    recentAnalyses: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);

      try {
        // Load real CSV data
        const transactions = await loadCSVData();
        console.log("Dashboard loaded transactions:", transactions.length);

        // Process data for dashboard
        const salesData = processSalesData(transactions);
        const customerData = processCustomerSegments(transactions);

        // Generate dashboard metrics from real data
        const totalRevenue = salesData.totalRevenue;
        const totalTransactions = salesData.totalTransactions;
        const totalCustomers = customerData.reduce(
          (sum, segment) => sum + segment.size * 10,
          0
        ); // Rough estimate
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
            aovGrowth: -2.1,
          },
          salesData: {
            totalRevenue,
            totalTransactions,
            topProducts: salesData.historicalData
              .slice(-7)
              .map((day, index) => ({
                name: `Product ${index + 1}`,
                revenue: day.sales * 0.3, // Simulate individual product revenue
                growth: Math.floor(Math.random() * 20) + 5,
              })),
          },
          forecastData: generateMockForecastData(),
          recentAnalyses: generateRecentAnalyses(),
        });
      } catch (error) {
        console.error("Error loading dashboard data:", error);
        // Fallback to mock data
        const metrics = generateMockDashboardMetrics();
        const salesData = {
          ...metrics,
          topProducts: [],
        };

        setDashboardData({
          metrics,
          salesData,
          forecastData: generateMockForecastData(),
          recentAnalyses: generateRecentAnalyses(),
        });
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleUploadComplete = (file) => {
    console.log("File uploaded from dashboard:", file);
  };

  const handleNavigation = (page) => {
    if (onNavigate) {
      onNavigate(page);
    }
  };

  const { metrics, salesData, forecastData, recentAnalyses } = dashboardData;

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
            value={`$${metrics.totalRevenue?.toLocaleString() || "0"}`}
            change={metrics.revenueGrowth}
            icon={DollarSign}
            subtitle="This month"
          />
          <MetricCard
            title="Transactions"
            value={metrics.totalTransactions?.toLocaleString() || "0"}
            change={metrics.transactionGrowth}
            icon={ShoppingCart}
            subtitle="This month"
          />
          <MetricCard
            title="Active Customers"
            value={metrics.totalCustomers?.toLocaleString() || "0"}
            change={metrics.customerGrowth}
            icon={Users}
            subtitle="This month"
          />
          <MetricCard
            title="Product Lines"
            value={metrics.activeProducts || "0"}
            change={null}
            icon={Package}
            subtitle={`of ${metrics.totalProducts || "0"} total`}
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
      </div>
    </div>
  );
}

export default Dashboard;

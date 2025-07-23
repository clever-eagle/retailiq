import React, { useState, useEffect } from "react";
import { useFileUpload } from "@/contexts/FileUploadContext";
import apiService from "@/services/api";
import {
  MetricCard,
  SalesOverviewCard,
  AnalysisResultsCard,
} from "@/components/DashboardCards";
import FileStatusOverview from "@/components/FileStatusOverview";
import {
  DollarSign,
  ShoppingCart,
  Users,
  Package,
  TrendingUp,
  RefreshCw,
} from "lucide-react";

function Dashboard({ onNavigate }) {
  const { uploadedFiles, addFile, updateFile, clearAllFiles } = useFileUpload();
  const [dashboardData, setDashboardData] = useState({
    metrics: {},
    salesData: { topProducts: [] },
    forecastData: null,
    recentAnalyses: [],
  });
  const [loading, setLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);

  // Manual refresh function - resets all data to zero
  const refreshDashboard = async () => {
    // Confirm before resetting
    const confirmed = window.confirm(
      "Are you sure you want to reset all data? This will clear all uploaded files and analysis results. This action cannot be undone."
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);

    try {
      // Call backend to reset data
      await apiService.resetData();

      // Clear uploaded files from context
      clearAllFiles();

      // Reset frontend state to empty
      setDashboardData({
        metrics: {
          totalRevenue: 0,
          totalTransactions: 0,
          totalCustomers: 0,
          avgOrderValue: 0,
          revenueGrowth: 0,
          transactionGrowth: 0,
          customerGrowth: 0,
          aovGrowth: 0,
          activeProducts: 0,
          totalProducts: 0,
        },
        salesData: {
          totalRevenue: 0,
          totalTransactions: 0,
          topProducts: [],
          monthlyTrends: [],
          weeklyPatterns: {},
          categories: {},
        },
        forecastData: null,
        recentAnalyses: [],
        hasData: false,
      });

      console.log("✅ Dashboard data reset successfully");
    } catch (error) {
      console.error("❌ Failed to reset data:", error);
      alert("Failed to reset data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);

      try {
        // Load real data from backend - only data-summary is available in clean backend
        const dataSummary = await apiService.getDataSummary();

        console.log("Dashboard loaded data:", dataSummary);

        // Check if we have uploaded data
        if (!dataSummary.data?.has_data) {
          setDashboardData({
            metrics: {},
            salesData: { topProducts: [] },
            forecastData: null,
            recentAnalyses: [],
            hasData: false,
          });
          setLoading(false);
          return;
        }

        const analysis = dataSummary.data.analysis;

        // Extract metrics from API response
        const metrics = {
          totalRevenue: analysis.revenue?.total_revenue || 0,
          totalTransactions: analysis.transactions?.total_transactions || 0,
          totalCustomers: analysis.transactions?.total_customers || 0,
          avgOrderValue: analysis.transactions?.avg_transaction_value || 0,
          revenueGrowth: 0, // Not available in clean backend
          transactionGrowth: 0,
          customerGrowth: 0,
          aovGrowth: 0,
          activeProducts: Object.keys(analysis.products?.top_products || {})
            .length,
          totalProducts:
            analysis.products?.total_products ||
            Object.keys(analysis.products?.top_products || {}).length,
        };

        const salesData = {
          totalRevenue: metrics.totalRevenue,
          totalTransactions: metrics.totalTransactions,
          topProducts: Object.entries(analysis.products?.top_products || {})
            .slice(0, 7)
            .map(([name, count]) => ({
              name,
              revenue: count * (metrics.avgOrderValue || 100), // Estimate from average
              growth: 0, // Not available
              sales: count,
            })),
          monthlyTrends: [], // Not available in clean backend
          weeklyPatterns: {},
          categories: analysis.products?.top_categories || {},
        };

        setDashboardData({
          metrics,
          salesData,
          forecastData: null,
          recentAnalyses: [
            {
              type: "CSV Analysis",
              timestamp: dataSummary.data.file_info?.upload_timestamp,
              filename: dataSummary.data.file_info?.filename,
              records: dataSummary.data.file_info?.records,
              result: "Analysis Complete",
              format: dataSummary.data.file_info?.format_detected,
            },
          ],
          hasData: true,
          trendsData: analysis,
        });
      } catch (error) {
        console.error("Error loading dashboard data:", error);
        // Fallback to empty state
        setDashboardData({
          metrics: {
            totalRevenue: 0,
            totalTransactions: 0,
            totalCustomers: 0,
            avgOrderValue: 0,
            revenueGrowth: 0,
            transactionGrowth: 0,
            customerGrowth: 0,
            aovGrowth: 0,
          },
          salesData: {
            totalRevenue: 0,
            totalTransactions: 0,
            topProducts: [],
            monthlyTrends: [],
            weeklyPatterns: {},
          },
          forecastData: null,
          recentAnalyses: [],
        });
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [uploadedFiles, refreshKey]); // Reload when files change or manual refresh

  const handleUploadComplete = (file) => {
    console.log("File uploaded from dashboard:", file);
    // Trigger refresh after upload
    setTimeout(() => refreshDashboard(), 1000);
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

  // Show empty state if no data uploaded
  if (!dashboardData.hasData) {
    return (
      <div className="p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">
              Upload a CSV file to see your analytics
            </p>
          </div>

          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No Data Available
              </h3>
              <p className="text-gray-600 mb-4">
                Upload a CSV file to start analyzing your retail data
              </p>
              <button
                onClick={() => handleNavigation("upload")}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
              >
                Upload CSV File
              </button>
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
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">
              AI-powered retail analytics and insights overview
            </p>
          </div>
          <button
            onClick={refreshDashboard}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
            Reset Data
          </button>
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
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

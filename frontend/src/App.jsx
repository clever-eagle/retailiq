import { useState } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import DataUpload from "./pages/DataUpload";
import SalesForecasting from "./pages/SalesForecasting";
import MarketBasketAnalysis from "./pages/MarketBasketAnalysis";
import ProductRecommendations from "./pages/ProductRecommendations";
import Settings from "./pages/Settings";
import { FileUploadProvider } from "./contexts/FileUploadContext";
import { Toaster } from "@/components/ui/sonner";

function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard onNavigate={setCurrentPage} />;
      case "data-upload":
        return <DataUpload />;
      case "sales-forecasting":
        return <SalesForecasting />;
      case "market-basket-analysis":
        return <MarketBasketAnalysis />;
      case "product-recommendations":
        return <ProductRecommendations />;
      case "settings":
        return <Settings />;
      default:
        return <Dashboard onNavigate={setCurrentPage} />;
    }
  };

  return (
    <FileUploadProvider>
      <div className="flex h-screen bg-gray-50">
        <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
        <main className="flex-1 overflow-auto md:ml-0">{renderPage()}</main>
      </div>
      <Toaster />
    </FileUploadProvider>
  );
}

export default App;

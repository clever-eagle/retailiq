import { cn } from "@/lib/utils";
import {
  Home,
  Upload,
  TrendingUp,
  ShoppingCart,
  Lightbulb,
  Settings,
  Menu,
  X,
  Plus,
} from "lucide-react";
import { useState } from "react";
import UploadDialog from "./UploadDialog";
import { Button } from "@/components/ui/button";

const navigationItems = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: Home,
  },
  {
    id: "data-upload",
    label: "Data Upload",
    icon: Upload,
  },
  {
    id: "sales-forecasting",
    label: "Sales Forecasting",
    icon: TrendingUp,
  },
  {
    id: "market-basket-analysis",
    label: "Market Basket Analysis",
    icon: ShoppingCart,
  },
  {
    id: "product-recommendations",
    label: "Product Recommendations",
    icon: Lightbulb,
  },
  {
    id: "settings",
    label: "Settings",
    icon: Settings,
  },
];

function Sidebar({ currentPage, setCurrentPage }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleNavigation = (pageId) => {
    setCurrentPage(pageId);
    setIsMobileMenuOpen(false); // Close mobile menu on navigation
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="fixed top-4 left-4 z-50 md:hidden bg-black text-white p-2 rounded-lg shadow-lg"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {isMobileMenuOpen ? (
          <X className="h-6 w-6" />
        ) : (
          <Menu className="h-6 w-6" />
        )}
      </button>

      {/* Backdrop for mobile */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          "fixed md:relative w-64 bg-white border-r border-gray-200 flex flex-col h-full z-50 transition-transform duration-300 ease-in-out",
          "md:translate-x-0",
          isMobileMenuOpen
            ? "translate-x-0"
            : "-translate-x-full md:translate-x-0"
        )}
      >
        {/* Logo */}
        <div className="bg-black text-white p-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">RetailIQ</h1>
          {/* Close button for mobile - only show when menu is open */}
          <button
            className="md:hidden text-white"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;

            return (
              <button
                key={item.id}
                onClick={() => handleNavigation(item.id)}
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200",
                  isActive
                    ? "bg-blue-50 text-blue-700 border border-blue-200"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                )}
              >
                <Icon
                  className={cn(
                    "h-5 w-5 flex-shrink-0",
                    isActive ? "text-blue-700" : "text-gray-500"
                  )}
                />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}

          {/* Quick Upload Button */}
          <div className="pt-4 border-t border-gray-200">
            <UploadDialog
              trigger={
                <Button
                  variant="outline"
                  className="w-full justify-start gap-3"
                  size="sm"
                >
                  <Plus className="h-4 w-4" />
                  <span>Quick Upload</span>
                </Button>
              }
              onUploadComplete={(file) => {
                console.log("File uploaded from sidebar:", file);
                // Optionally navigate to data upload page
                setCurrentPage("data-upload");
              }}
            />
          </div>
        </nav>

        {/* Footer */}
      </div>
    </>
  );
}

export default Sidebar;

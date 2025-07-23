import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Alert, AlertDescription } from "../components/ui/alert";
import { AlertCircle, RefreshCw } from "lucide-react";

function MarketBasketAnalysisSimple() {
  console.log("MarketBasketAnalysisSimple component rendering...");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("useEffect running...");
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  console.log("Component state:", { loading, error });

  if (loading) {
    return (
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Market Basket Analysis
          </h1>
          <p className="text-gray-600">Loading...</p>
          <div className="flex items-center justify-center h-32">
            <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Market Basket Analysis
          </h1>
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Market Basket Analysis
        </h1>
        <p className="text-gray-600 mb-6">
          Market Basket Analysis component is working! This is a simplified
          version.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Association Rules</CardTitle>
              <CardDescription>Product purchase patterns</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">156</div>
              <p className="text-sm text-gray-500">rules discovered</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Cross-sell Opportunities</CardTitle>
              <CardDescription>Recommended product bundles</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">23</div>
              <p className="text-sm text-gray-500">opportunities identified</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Customer Segments</CardTitle>
              <CardDescription>Behavioral groups</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">4</div>
              <p className="text-sm text-gray-500">segments analyzed</p>
            </CardContent>
          </Card>
        </div>

        <Card className="mt-6">
          <CardHeader>
            <CardTitle>System Status</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-green-600">
              ✅ Component rendering successfully
            </p>
            <p className="text-green-600">✅ UI components loading correctly</p>
            <p className="text-yellow-600">
              ⚠️ Full functionality temporarily disabled for debugging
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default MarketBasketAnalysisSimple;

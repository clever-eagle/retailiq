import React, { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Alert, AlertDescription } from "../components/ui/alert";
import apiService from "../services/api";
import { ShoppingCart, Plus, X, Lightbulb, TrendingUp } from "lucide-react";

function ProductRecommendations() {
  const [currentItems, setCurrentItems] = useState([]);
  const [newItem, setNewItem] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addItem = () => {
    if (newItem.trim() && !currentItems.includes(newItem.trim())) {
      setCurrentItems([...currentItems, newItem.trim()]);
      setNewItem("");
    }
  };

  const removeItem = (item) => {
    setCurrentItems(currentItems.filter((i) => i !== item));
  };

  const getRecommendations = async () => {
    if (currentItems.length === 0) {
      setError("Please add at least one item to get recommendations");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiService.getRecommendations(currentItems);
      // Fix: extract recommendations array from backend response
      setRecommendations(result.data?.recommendations || []);
    } catch (err) {
      console.error("Error getting recommendations:", err);
      setError(`Failed to get recommendations: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      addItem();
    }
  };

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Product Recommendations
          </h1>
          <p className="text-gray-600">
            Get AI-powered product recommendations based on market basket
            analysis
          </p>
        </div>

        <div className="grid gap-6">
          {/* Input Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="h-5 w-5" />
                Current Cart Items
              </CardTitle>
              <CardDescription>
                Add products to see what customers typically buy together
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  placeholder="Enter product name..."
                  value={newItem}
                  onChange={(e) => setNewItem(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <Button onClick={addItem} disabled={!newItem.trim()}>
                  <Plus className="h-4 w-4 mr-2" />
                  Add
                </Button>
              </div>

              {/* Current Items */}
              <div className="flex flex-wrap gap-2 mb-4">
                {currentItems.map((item, index) => (
                  <Badge key={index} variant="secondary" className="px-3 py-1">
                    {item}
                    <button
                      onClick={() => removeItem(item)}
                      className="ml-2 text-gray-500 hover:text-gray-700"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>

              <Button
                onClick={getRecommendations}
                disabled={currentItems.length === 0 || loading}
                className="w-full"
              >
                {loading ? (
                  "Getting Recommendations..."
                ) : (
                  <>
                    <Lightbulb className="h-4 w-4 mr-2" />
                    Get Recommendations
                  </>
                )}
              </Button>

              {error && (
                <Alert className="mt-4">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Recommendations Section */}
          {recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Recommended Products
                </CardTitle>
                <CardDescription>
                  Based on market basket analysis of customer purchase patterns
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-semibold text-lg">{rec.product}</h3>
                        <div className="flex gap-2">
                          <Badge variant="outline">
                            Confidence: {(rec.confidence * 100).toFixed(1)}%
                          </Badge>
                          {rec.lift > 0 && (
                            <Badge variant="secondary">
                              Lift: {rec.lift.toFixed(2)}
                            </Badge>
                          )}
                        </div>
                      </div>

                      {rec.based_on && rec.based_on.length > 0 && (
                        <p className="text-sm text-gray-600">
                          Often bought with: {rec.based_on.join(", ")}
                        </p>
                      )}

                      <div className="mt-3">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${rec.confidence * 100}%` }}
                          ></div>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          Recommendation strength based on purchase patterns
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Empty State */}
          {!loading &&
            recommendations.length === 0 &&
            currentItems.length > 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <Lightbulb className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-600 mb-2">
                    No Recommendations Found
                  </h3>
                  <p className="text-gray-500">
                    Try adding different products or check if the backend has
                    sufficient data for analysis.
                  </p>
                </CardContent>
              </Card>
            )}
        </div>
      </div>
    </div>
  );
}

export default ProductRecommendations;

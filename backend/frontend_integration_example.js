// Frontend Integration Examples for Retail Analytics Backend
// Add these functions to your React/JavaScript frontend

// Backend base URL
const BACKEND_URL = "http://localhost:5000";

/**
 * Upload CSV data file
 */
export const uploadData = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${BACKEND_URL}/upload-data`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Upload failed");
    }

    return result;
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
};

/**
 * Perform market basket analysis
 */
export const performMarketBasketAnalysis = async (parameters = {}) => {
  try {
    const payload = {
      min_support: parameters.minSupport || 0.01,
      min_confidence: parameters.minConfidence || 0.2,
      min_lift: parameters.minLift || 1.0,
    };

    const response = await fetch(`${BACKEND_URL}/market-basket-analysis`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Analysis failed");
    }

    return result.data;
  } catch (error) {
    console.error("Market basket analysis error:", error);
    throw error;
  }
};

/**
 * Get product recommendations based on current cart items
 */
export const getRecommendations = async (currentItems) => {
  try {
    const payload = {
      items: currentItems,
    };

    const response = await fetch(`${BACKEND_URL}/get-recommendations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Recommendations failed");
    }

    return result.data.recommendations;
  } catch (error) {
    console.error("Recommendations error:", error);
    throw error;
  }
};

/**
 * Generate sales forecast
 */
export const generateSalesForecast = async (options = {}) => {
  try {
    const payload = {
      forecast_days: options.forecastDays || 30,
      product: options.product || null,
      category: options.category || null,
    };

    const response = await fetch(`${BACKEND_URL}/sales-forecast`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Forecast failed");
    }

    return result.data;
  } catch (error) {
    console.error("Sales forecast error:", error);
    throw error;
  }
};

/**
 * Get sales trends analysis
 */
export const getSalesTrends = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/sales-trends`);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Trends analysis failed");
    }

    return result.data;
  } catch (error) {
    console.error("Sales trends error:", error);
    throw error;
  }
};

/**
 * Get data summary
 */
export const getDataSummary = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/data-summary`);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Data summary failed");
    }

    return result.data;
  } catch (error) {
    console.error("Data summary error:", error);
    throw error;
  }
};

/**
 * Get frequent itemsets
 */
export const getFrequentItemsets = async (minSupport = 0.01) => {
  try {
    const payload = {
      min_support: minSupport,
    };

    const response = await fetch(`${BACKEND_URL}/frequent-itemsets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Frequent itemsets analysis failed");
    }

    return result.data;
  } catch (error) {
    console.error("Frequent itemsets error:", error);
    throw error;
  }
};

// React Component Example Usage:

/*
import React, { useState, useEffect } from 'react';
import { 
  uploadData, 
  performMarketBasketAnalysis, 
  getRecommendations,
  generateSalesForecast,
  getSalesTrends,
  getDataSummary 
} from './api/backend';

const AnalyticsComponent = () => {
  const [data, setData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  // Upload data
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      try {
        await uploadData(file);
        alert('Data uploaded successfully!');
        // Refresh data summary
        const summary = await getDataSummary();
        setData(summary);
      } catch (error) {
        alert('Upload failed: ' + error.message);
      } finally {
        setLoading(false);
      }
    }
  };

  // Get recommendations for current cart
  const handleGetRecommendations = async () => {
    const currentItems = ['Laptop', 'Mouse']; // Replace with actual cart items
    setLoading(true);
    try {
      const recs = await getRecommendations(currentItems);
      setRecommendations(recs);
    } catch (error) {
      alert('Failed to get recommendations: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Generate sales forecast
  const handleGenerateForecast = async () => {
    setLoading(true);
    try {
      const forecastData = await generateSalesForecast({ forecastDays: 30 });
      setForecast(forecastData);
    } catch (error) {
      alert('Failed to generate forecast: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Retail Analytics</h2>
      
      <div>
        <h3>Upload Data</h3>
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleFileUpload} 
          disabled={loading}
        />
      </div>

      <div>
        <h3>Product Recommendations</h3>
        <button onClick={handleGetRecommendations} disabled={loading}>
          Get Recommendations
        </button>
        {recommendations.length > 0 && (
          <ul>
            {recommendations.map((rec, index) => (
              <li key={index}>
                {rec.product} - Confidence: {rec.confidence.toFixed(3)}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h3>Sales Forecast</h3>
        <button onClick={handleGenerateForecast} disabled={loading}>
          Generate Forecast
        </button>
        {forecast && (
          <div>
            <p>Forecast generated for {forecast.metadata.forecast_days} days</p>
            {forecast.forecasts.ensemble && (
              <div>
                <h4>Ensemble Forecast</h4>
                {forecast.forecasts.ensemble.slice(0, 7).map((day, index) => (
                  <div key={index}>
                    {day.date}: ${day.predicted_revenue.toFixed(2)}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {loading && <div>Loading...</div>}
    </div>
  );
};

export default AnalyticsComponent;
*/

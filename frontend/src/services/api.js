// API service for connecting frontend with backend
const API_BASE_URL = "http://localhost:5000";

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || `HTTP error! status: ${response.status}`
        );
      }

      return data;
    } catch (error) {
      console.error(`API Error for ${endpoint}:`, error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.makeRequest("/health");
  }

  // Upload CSV data
  async uploadData(file) {
    const formData = new FormData();
    formData.append("file", file);

    return this.makeRequest("/upload-data", {
      method: "POST",
      body: formData,
      headers: {}, // Let browser set content-type for FormData
    });
  }

  // Get data summary
  async getDataSummary() {
    return this.makeRequest("/data-summary");
  }

  // Perform market basket analysis
  async performMarketBasketAnalysis(parameters = {}) {
    const payload = {
      min_support: parameters.minSupport || 0.01,
      min_confidence: parameters.minConfidence || 0.2,
      min_lift: parameters.minLift || 1.0,
    };

    return this.makeRequest("/market-basket-analysis", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  // Get product recommendations
  async getRecommendations(currentItems) {
    const payload = {
      items: currentItems,
    };

    return this.makeRequest("/get-recommendations", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  // Generate sales forecast
  async generateSalesForecast(options = {}) {
    const payload = {
      forecast_days: options.forecastDays || 30,
      product: options.product || null,
      category: options.category || null,
    };

    return this.makeRequest("/sales-forecast", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  // Get sales trends
  async getSalesTrends() {
    return this.makeRequest("/sales-trends");
  }

  // Get frequent itemsets
  async getFrequentItemsets(minSupport = 0.01) {
    const payload = {
      min_support: minSupport,
    };

    return this.makeRequest("/frequent-itemsets", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

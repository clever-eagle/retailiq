// Detailed mock data for analysis pages
export const generateDetailedForecastData = () => {
  // Generate more comprehensive historical data (90 days)
  const historicalData = [];
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 90);
  
  for (let i = 0; i < 90; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    
    // Simulate seasonal patterns and trends
    const baseValue = 4500;
    const weeklyPattern = Math.sin((i % 7) * Math.PI / 3.5) * 500; // Weekly pattern
    const monthlyTrend = Math.sin(i * Math.PI / 30) * 800; // Monthly seasonality
    const growthTrend = i * 2; // Linear growth
    const randomNoise = (Math.random() - 0.5) * 600;
    
    const sales = Math.max(0, baseValue + weeklyPattern + monthlyTrend + growthTrend + randomNoise);
    
    historicalData.push({
      date: date.toISOString().split('T')[0],
      sales: Math.round(sales),
      actualDate: new Date(date)
    });
  }
  
  // Generate future predictions (30 days)
  const predictions = [];
  for (let i = 1; i <= 30; i++) {
    const date = new Date();
    date.setDate(date.getDate() + i);
    
    const lastHistorical = historicalData[historicalData.length - 1].sales;
    const trendFactor = 1 + (i * 0.001); // Small positive trend
    const seasonalFactor = 1 + Math.sin((90 + i) * Math.PI / 30) * 0.15;
    const confidenceFactor = Math.max(0.8, 1 - (i * 0.01)); // Decreasing confidence
    
    const predicted = lastHistorical * trendFactor * seasonalFactor;
    const confidenceInterval = predicted * (1 - confidenceFactor) * 0.2;
    
    predictions.push({
      date: date.toISOString().split('T')[0],
      predicted: Math.round(predicted),
      lowerBound: Math.round(predicted - confidenceInterval),
      upperBound: Math.round(predicted + confidenceInterval),
      confidence: Math.round(confidenceFactor * 100),
      actualDate: new Date(date)
    });
  }
  
  return { historicalData, predictions };
};

export const generateProductLevelForecasts = () => {
  const products = [
    'Wireless Headphones', 'Coffee Maker', 'Bluetooth Speaker', 'Yoga Mat',
    'Office Chair', 'Smartphone Case', 'Water Bottle', 'Desk Lamp',
    'Running Shoes', 'Kitchen Scale'
  ];
  
  return products.map(product => {
    const currentSales = Math.floor(Math.random() * 1000) + 200;
    const growth = (Math.random() - 0.3) * 30; // -30% to +20% growth
    const forecastedSales = Math.round(currentSales * (1 + growth / 100));
    const accuracy = Math.floor(Math.random() * 15) + 80; // 80-95% accuracy
    
    return {
      product,
      currentSales,
      forecastedSales,
      growth: growth.toFixed(1),
      accuracy,
      confidence: Math.floor(Math.random() * 20) + 75, // 75-95% confidence
      trend: growth > 0 ? 'up' : 'down',
      category: ['Electronics', 'Appliances', 'Fitness', 'Furniture', 'Accessories'][Math.floor(Math.random() * 5)]
    };
  });
};

export const generateSeasonalInsights = () => {
  return [
    {
      period: 'Q4 2025',
      trend: 'Strong Growth Expected',
      factor: 'Holiday Season',
      impact: '+25%',
      confidence: 89,
      description: 'Holiday shopping typically drives significant sales increase'
    },
    {
      period: 'January 2026',
      trend: 'Post-Holiday Decline',
      factor: 'Seasonal Adjustment',
      impact: '-15%',
      confidence: 82,
      description: 'Expected decline following holiday season peak'
    },
    {
      period: 'Spring 2026',
      trend: 'Gradual Recovery',
      factor: 'New Product Launches',
      impact: '+8%',
      confidence: 75,
      description: 'Recovery driven by new product introductions'
    }
  ];
};

export const generateDetailedAssociationRules = () => {
  const rules = [
    {
      id: 1,
      antecedent: ['Wireless Headphones'],
      consequent: ['Smartphone Case'],
      support: 0.12,
      confidence: 0.68,
      lift: 2.1,
      conviction: 2.8,
      transactions: 124,
      expectedRevenue: 2480,
      strength: 'Strong'
    },
    {
      id: 2,
      antecedent: ['Coffee Maker'],
      consequent: ['Coffee Beans', 'Coffee Filters'],
      support: 0.15,
      confidence: 0.72,
      lift: 2.4,
      conviction: 3.1,
      transactions: 156,
      expectedRevenue: 3120,
      strength: 'Very Strong'
    },
    {
      id: 3,
      antecedent: ['Yoga Mat'],
      consequent: ['Water Bottle'],
      support: 0.08,
      confidence: 0.58,
      lift: 1.9,
      conviction: 2.2,
      transactions: 83,
      expectedRevenue: 1245,
      strength: 'Moderate'
    },
    {
      id: 4,
      antecedent: ['Office Chair', 'Desk Lamp'],
      consequent: ['Monitor Stand'],
      support: 0.06,
      confidence: 0.75,
      lift: 2.8,
      conviction: 3.5,
      transactions: 62,
      expectedRevenue: 1860,
      strength: 'Strong'
    },
    {
      id: 5,
      antecedent: ['Running Shoes'],
      consequent: ['Athletic Socks', 'Water Bottle'],
      support: 0.10,
      confidence: 0.62,
      lift: 1.8,
      conviction: 2.4,
      transactions: 104,
      expectedRevenue: 1560,
      strength: 'Moderate'
    },
    {
      id: 6,
      antecedent: ['Bluetooth Speaker'],
      consequent: ['Phone Charger'],
      support: 0.09,
      confidence: 0.55,
      lift: 1.7,
      conviction: 2.0,
      transactions: 93,
      expectedRevenue: 1395,
      strength: 'Moderate'
    }
  ];

  return rules.sort((a, b) => b.lift - a.lift);
};

export const generateCrossSellOpportunities = () => {
  return [
    {
      product: 'Wireless Headphones',
      recommendations: ['Smartphone Case', 'Phone Charger', 'Bluetooth Adapter'],
      potentialRevenue: 2480,
      successRate: 68,
      bundle: 'Audio Accessories Bundle',
      discount: 15
    },
    {
      product: 'Coffee Maker',
      recommendations: ['Coffee Beans', 'Coffee Filters', 'Milk Frother'],
      potentialRevenue: 3120,
      successRate: 72,
      bundle: 'Complete Coffee Experience',
      discount: 20
    },
    {
      product: 'Office Chair',
      recommendations: ['Desk Lamp', 'Monitor Stand', 'Desk Organizer'],
      potentialRevenue: 1860,
      successRate: 75,
      bundle: 'Workspace Essentials',
      discount: 18
    },
    {
      product: 'Yoga Mat',
      recommendations: ['Water Bottle', 'Resistance Bands', 'Yoga Blocks'],
      potentialRevenue: 1245,
      successRate: 58,
      bundle: 'Fitness Starter Kit',
      discount: 12
    }
  ];
};

export const generateCustomerSegments = () => {
  return [
    {
      segment: 'Tech Enthusiasts',
      size: 24,
      avgOrderValue: 185.50,
      topProducts: ['Wireless Headphones', 'Bluetooth Speaker', 'Smartphone Case'],
      behaviorPattern: 'Frequently buys electronics accessories together',
      recommendation: 'Bundle electronics with premium accessories'
    },
    {
      segment: 'Home & Office',
      size: 31,
      avgOrderValue: 245.20,
      topProducts: ['Office Chair', 'Desk Lamp', 'Coffee Maker'],
      behaviorPattern: 'Purchases workspace and home improvement items',
      recommendation: 'Create workspace productivity bundles'
    },
    {
      segment: 'Fitness Focused',
      size: 18,
      avgOrderValue: 95.75,
      topProducts: ['Yoga Mat', 'Water Bottle', 'Running Shoes'],
      behaviorPattern: 'Health and fitness product combinations',
      recommendation: 'Develop fitness lifestyle packages'
    },
    {
      segment: 'Occasional Buyers',
      size: 27,
      avgOrderValue: 67.30,
      topProducts: ['Water Bottle', 'Phone Charger', 'Desk Organizer'],
      behaviorPattern: 'Lower value, utility-focused purchases',
      recommendation: 'Offer value packs and starter bundles'
    }
  ];
};

export const generateForecastMetrics = () => {
  return {
    overall: {
      accuracy: 87.3,
      mape: 12.7, // Mean Absolute Percentage Error
      rmse: 245.8, // Root Mean Square Error
      r2: 0.91, // R-squared
      lastUpdated: new Date().toISOString().split('T')[0]
    },
    byProduct: {
      accuracy: 84.1,
      bestPerforming: 'Wireless Headphones',
      worstPerforming: 'Seasonal Items',
      avgConfidence: 82.5
    },
    trends: {
      shortTerm: 'Positive (+2.3%)',
      longTerm: 'Steady Growth (+8.1%)',
      volatility: 'Low',
      seasonality: 'Moderate'
    }
  };
};

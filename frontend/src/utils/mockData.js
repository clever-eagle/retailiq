// Mock data generators for RetailIQ Dashboard
export const generateMockSalesData = () => {
  const products = [
    { name: 'Wireless Headphones', category: 'Electronics', sales: 2400, revenue: 239760, growth: 12.5 },
    { name: 'Coffee Maker', category: 'Appliances', sales: 1800, revenue: 143820, growth: 8.3 },
    { name: 'Bluetooth Speaker', category: 'Electronics', sales: 3200, revenue: 159680, growth: 15.7 },
    { name: 'Yoga Mat', category: 'Fitness', sales: 1500, revenue: 44985, growth: -2.1 },
    { name: 'Office Chair', category: 'Furniture', sales: 850, revenue: 169915, growth: 6.8 },
    { name: 'Smartphone Case', category: 'Accessories', sales: 4500, revenue: 89955, growth: 22.3 },
    { name: 'Water Bottle', category: 'Sports', sales: 2100, revenue: 52479, growth: 9.4 },
    { name: 'Desk Lamp', category: 'Furniture', sales: 1200, revenue: 47988, growth: 4.2 }
  ];

  return products;
};

export const generateMockForecastData = () => {
  const dates = [];
  const actual = [];
  const predicted = [];
  
  // Generate last 30 days of actual data
  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(date.toISOString().split('T')[0]);
    
    // Simulate seasonal sales with some randomness
    const baseValue = 5000 + Math.sin(i * 0.1) * 1000;
    const randomVariation = (Math.random() - 0.5) * 800;
    actual.push(Math.round(baseValue + randomVariation));
  }
  
  // Generate next 14 days of predictions
  for (let i = 1; i <= 14; i++) {
    const date = new Date();
    date.setDate(date.getDate() + i);
    dates.push(date.toISOString().split('T')[0]);
    
    const trend = 1 + (i * 0.02); // 2% growth trend
    const baseValue = 5200 * trend + Math.sin((29 + i) * 0.1) * 1000;
    const confidence = Math.random() * 300; // Confidence interval
    predicted.push(Math.round(baseValue + confidence));
  }
  
  return { dates, actual, predicted };
};

export const generateMockBasketData = () => {
  const associations = [
    {
      antecedent: ['Coffee Maker'],
      consequent: ['Coffee Beans'],
      support: 0.15,
      confidence: 0.68,
      lift: 2.1,
      conviction: 2.8
    },
    {
      antecedent: ['Wireless Headphones'],
      consequent: ['Smartphone Case'],
      support: 0.12,
      confidence: 0.58,
      lift: 1.9,
      conviction: 2.2
    },
    {
      antecedent: ['Yoga Mat'],
      consequent: ['Water Bottle'],
      support: 0.08,
      confidence: 0.72,
      lift: 2.4,
      conviction: 3.1
    },
    {
      antecedent: ['Office Chair', 'Desk Lamp'],
      consequent: ['Monitor Stand'],
      support: 0.06,
      confidence: 0.75,
      lift: 2.8,
      conviction: 3.5
    },
    {
      antecedent: ['Bluetooth Speaker'],
      consequent: ['Phone Charger'],
      support: 0.10,
      confidence: 0.62,
      lift: 1.8,
      conviction: 2.4
    }
  ];

  const frequentItemsets = [
    { items: ['Coffee Maker', 'Coffee Beans'], support: 0.15, frequency: 156 },
    { items: ['Wireless Headphones', 'Smartphone Case'], support: 0.12, frequency: 124 },
    { items: ['Yoga Mat', 'Water Bottle'], support: 0.08, frequency: 83 },
    { items: ['Office Chair', 'Desk Lamp', 'Monitor Stand'], support: 0.06, frequency: 62 },
    { items: ['Bluetooth Speaker', 'Phone Charger'], support: 0.10, frequency: 104 }
  ];

  return { associations, frequentItemsets };
};

export const generateMockDashboardMetrics = () => {
  const currentDate = new Date();
  const lastMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
  
  return {
    totalRevenue: 847560,
    revenueGrowth: 12.8,
    totalTransactions: 3247,
    transactionGrowth: 8.4,
    averageOrderValue: 261.23,
    aovGrowth: 4.1,
    totalProducts: 156,
    activeProducts: 143,
    topCategory: 'Electronics',
    categoryGrowth: 18.6,
    forecastAccuracy: 87.3,
    lastAnalysisDate: currentDate.toISOString().split('T')[0],
    totalCustomers: 1256,
    customerGrowth: 6.7,
    repeatCustomerRate: 34.2
  };
};

export const generateRecentAnalyses = () => {
  const analyses = [
    {
      id: 'forecast_001',
      type: 'Sales Forecasting',
      date: '2025-07-10',
      status: 'completed',
      results: {
        summary: 'Sales expected to grow 15% next month',
        confidence: 89,
        keyInsight: 'Electronics category showing strongest growth potential'
      }
    },
    {
      id: 'basket_001',
      type: 'Market Basket Analysis',
      date: '2025-07-09',
      status: 'completed',
      results: {
        summary: '12 strong product associations found',
        confidence: 94,
        keyInsight: 'Coffee products have highest cross-sell potential'
      }
    },
    {
      id: 'forecast_002',
      type: 'Sales Forecasting',
      date: '2025-07-08',
      status: 'completed',
      results: {
        summary: 'Seasonal trends identified for Q3',
        confidence: 78,
        keyInsight: 'Prepare inventory for back-to-school season'
      }
    }
  ];

  return analyses;
};

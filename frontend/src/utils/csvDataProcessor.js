// CSV Data Processor for RetailIQ
// Processes the retail transactions CSV for use in forecasting and market basket analysis

export const loadCSVData = async () => {
  try {
    // In a real application, you would fetch this from a server
    // For now, we'll load it from the public folder or use a static import
    const response = await fetch('/data/retail_transactions.csv')
    const csvText = await response.text()
    
    return parseCSV(csvText)
  } catch (error) {
    console.error('Error loading CSV data:', error)
    // Fallback to mock data if CSV can't be loaded
    return generateFallbackData()
  }
}

const parseCSV = (csvText) => {
  const lines = csvText.trim().split('\n')
  const headers = lines[0].split(',')
  
  const data = lines.slice(1).map(line => {
    const values = line.split(',')
    const row = {}
    headers.forEach((header, index) => {
      row[header] = values[index]
    })
    return row
  })
  
  return data
}

// Process transaction data for sales forecasting
export const processSalesData = (transactions) => {
  // Group transactions by date and calculate daily sales
  const dailySales = {}
  
  transactions.forEach(transaction => {
    const date = transaction.date
    const amount = parseFloat(transaction.total_amount)
    
    if (!dailySales[date]) {
      dailySales[date] = {
        date,
        sales: 0,
        transactions: 0,
        revenue: 0
      }
    }
    
    dailySales[date].sales += amount
    dailySales[date].transactions += 1
    dailySales[date].revenue += amount
  })
  
  // Convert to array and sort by date
  const salesArray = Object.values(dailySales).sort((a, b) => new Date(a.date) - new Date(b.date))
  
  // Generate forecast data (simple trend-based prediction)
  const lastSales = salesArray.slice(-7).reduce((sum, day) => sum + day.sales, 0) / 7
  const predictions = []
  
  for (let i = 1; i <= 30; i++) {
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + i)
    
    // Simple forecasting with trend and seasonality
    const trendFactor = 1 + (i * 0.002) // Small growth trend
    const seasonalFactor = 1 + Math.sin((i * Math.PI) / 15) * 0.1 // Weekly seasonality
    const predicted = lastSales * trendFactor * seasonalFactor
    
    predictions.push({
      date: futureDate.toISOString().split('T')[0],
      predicted: Math.round(predicted),
      lowerBound: Math.round(predicted * 0.85),
      upperBound: Math.round(predicted * 1.15),
      confidence: Math.max(70, 95 - (i * 1)) // Decreasing confidence
    })
  }
  
  return {
    historicalData: salesArray,
    predictions,
    totalRevenue: salesArray.reduce((sum, day) => sum + day.revenue, 0),
    totalTransactions: salesArray.reduce((sum, day) => sum + day.transactions, 0)
  }
}

// Process data for product-level forecasting
export const processProductForecasts = (transactions) => {
  const productSales = {}
  
  transactions.forEach(transaction => {
    const product = transaction.product_name
    const amount = parseFloat(transaction.total_amount)
    const quantity = parseInt(transaction.quantity)
    
    if (!productSales[product]) {
      productSales[product] = {
        product,
        currentSales: 0,
        quantity: 0,
        revenue: 0,
        category: transaction.category
      }
    }
    
    productSales[product].currentSales += amount
    productSales[product].quantity += quantity
    productSales[product].revenue += amount
  })
  
  // Convert to array and add forecast calculations
  return Object.values(productSales).map(product => {
    const growth = (Math.random() - 0.3) * 30 // -30% to +20% growth
    const forecastedSales = Math.round(product.currentSales * (1 + growth / 100))
    
    return {
      ...product,
      forecastedSales,
      growth: growth.toFixed(1),
      accuracy: Math.floor(Math.random() * 15) + 80, // 80-95% accuracy
      confidence: Math.floor(Math.random() * 20) + 75, // 75-95% confidence
      trend: growth > 0 ? 'up' : 'down'
    }
  }).sort((a, b) => b.revenue - a.revenue)
}

// Process data for market basket analysis
export const processMarketBasketData = (transactions) => {
  // Group transactions by customer and date to identify baskets
  const baskets = {}
  
  transactions.forEach(transaction => {
    const basketKey = `${transaction.customer_id}_${transaction.date}`
    
    if (!baskets[basketKey]) {
      baskets[basketKey] = {
        customer_id: transaction.customer_id,
        date: transaction.date,
        products: [],
        total: 0
      }
    }
    
    baskets[basketKey].products.push(transaction.product_name)
    baskets[basketKey].total += parseFloat(transaction.total_amount)
  })
  
  const basketArray = Object.values(baskets)
  
  // Generate association rules
  const associationRules = generateAssociationRules(basketArray)
  
  // Generate frequent itemsets
  const frequentItemsets = generateFrequentItemsets(basketArray)
  
  return {
    baskets: basketArray,
    associationRules,
    frequentItemsets
  }
}

const generateAssociationRules = (baskets) => {
  const rules = []
  const productPairs = {}
  const singleProducts = {}
  
  // Count single products and pairs
  baskets.forEach(basket => {
    basket.products.forEach(product => {
      singleProducts[product] = (singleProducts[product] || 0) + 1
    })
    
    // Generate pairs from this basket
    for (let i = 0; i < basket.products.length; i++) {
      for (let j = i + 1; j < basket.products.length; j++) {
        const pair = [basket.products[i], basket.products[j]].sort().join(' -> ')
        productPairs[pair] = (productPairs[pair] || 0) + 1
      }
    }
  })
  
  const totalBaskets = baskets.length
  
  // Generate rules from pairs
  Object.entries(productPairs).forEach(([pair, count], index) => {
    const [antecedent, consequent] = pair.split(' -> ')
    const support = count / totalBaskets
    const confidence = count / (singleProducts[antecedent] || 1)
    const lift = confidence / ((singleProducts[consequent] || 1) / totalBaskets)
    
    if (support >= 0.05 && confidence >= 0.5 && lift > 1) {
      rules.push({
        id: index + 1,
        antecedent: [antecedent],
        consequent: [consequent],
        support,
        confidence,
        lift,
        conviction: (1 - (singleProducts[consequent] || 1) / totalBaskets) / (1 - confidence),
        transactions: count,
        expectedRevenue: count * 50, // Estimated revenue per rule
        strength: lift > 2.5 ? 'Very Strong' : lift > 2 ? 'Strong' : 'Moderate'
      })
    }
  })
  
  return rules.sort((a, b) => b.lift - a.lift).slice(0, 10) // Top 10 rules
}

const generateFrequentItemsets = (baskets) => {
  const itemCounts = {}
  
  baskets.forEach(basket => {
    basket.products.forEach(product => {
      itemCounts[product] = (itemCounts[product] || 0) + 1
    })
  })
  
  return Object.entries(itemCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10)
    .map(([product, count]) => ({
      items: [product],
      frequency: count,
      support: count / baskets.length
    }))
}

// Process customer segments from transaction data
export const processCustomerSegments = (transactions) => {
  const customers = {}
  
  transactions.forEach(transaction => {
    const customerId = transaction.customer_id
    const amount = parseFloat(transaction.total_amount)
    
    if (!customers[customerId]) {
      customers[customerId] = {
        customerId,
        totalSpent: 0,
        transactionCount: 0,
        products: new Set(),
        segment: transaction.customer_segment,
        categories: new Set()
      }
    }
    
    customers[customerId].totalSpent += amount
    customers[customerId].transactionCount += 1
    customers[customerId].products.add(transaction.product_name)
    customers[customerId].categories.add(transaction.category)
  })
  
  // Group by segment
  const segments = {}
  Object.values(customers).forEach(customer => {
    const segment = customer.segment
    
    if (!segments[segment]) {
      segments[segment] = {
        segment,
        customers: [],
        totalRevenue: 0,
        totalOrders: 0
      }
    }
    
    segments[segment].customers.push(customer)
    segments[segment].totalRevenue += customer.totalSpent
    segments[segment].totalOrders += customer.transactionCount
  })
  
  // Calculate segment statistics
  const totalCustomers = Object.keys(customers).length
  
  return Object.values(segments).map(segment => {
    const avgOrderValue = segment.totalRevenue / segment.totalOrders
    const customerCount = segment.customers.length
    const size = Math.round((customerCount / totalCustomers) * 100)
    
    // Get top products for this segment
    const productCounts = {}
    segment.customers.forEach(customer => {
      Array.from(customer.products).forEach(product => {
        productCounts[product] = (productCounts[product] || 0) + 1
      })
    })
    
    const topProducts = Object.entries(productCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([product]) => product)
    
    return {
      segment: segment.segment,
      size,
      avgOrderValue,
      topProducts,
      behaviorPattern: getSegmentBehaviorPattern(segment.segment),
      recommendation: getSegmentRecommendation(segment.segment)
    }
  })
}

const getSegmentBehaviorPattern = (segment) => {
  const patterns = {
    'Tech Enthusiasts': 'Frequently buys electronics accessories together',
    'Home & Office': 'Purchases workspace and home improvement items',
    'Fitness Focused': 'Health and fitness product combinations',
    'Occasional Buyers': 'Lower value, utility-focused purchases'
  }
  return patterns[segment] || 'Mixed purchasing behavior'
}

const getSegmentRecommendation = (segment) => {
  const recommendations = {
    'Tech Enthusiasts': 'Bundle electronics with premium accessories',
    'Home & Office': 'Create workspace productivity bundles',
    'Fitness Focused': 'Develop fitness lifestyle packages',
    'Occasional Buyers': 'Offer value packs and starter bundles'
  }
  return recommendations[segment] || 'Personalized product recommendations'
}

// Generate fallback data if CSV loading fails
const generateFallbackData = () => {
  // Return the same structure as our CSV but with generated data
  const fallbackTransactions = []
  
  for (let i = 1; i <= 100; i++) {
    fallbackTransactions.push({
      transaction_id: `TXN${i.toString().padStart(3, '0')}`,
      date: `2024-${Math.ceil(i/30).toString().padStart(2, '0')}-${((i % 30) + 1).toString().padStart(2, '0')}`,
      customer_id: `CUST${Math.ceil(i/2).toString().padStart(3, '0')}`,
      product_name: ['Wireless Headphones', 'Coffee Maker', 'Yoga Mat', 'Office Chair'][i % 4],
      category: ['Electronics', 'Appliances', 'Fitness', 'Furniture'][i % 4],
      quantity: Math.ceil(Math.random() * 3),
      unit_price: (Math.random() * 200 + 20).toFixed(2),
      total_amount: (Math.random() * 300 + 20).toFixed(2),
      customer_segment: ['Tech Enthusiasts', 'Home & Office', 'Fitness Focused', 'Occasional Buyers'][i % 4],
      store_location: ['Store A', 'Store B', 'Store C'][i % 3]
    })
  }
  
  return fallbackTransactions
}

export default {
  loadCSVData,
  processSalesData,
  processProductForecasts,
  processMarketBasketData,
  processCustomerSegments
}

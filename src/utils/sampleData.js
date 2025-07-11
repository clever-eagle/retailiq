// Sample retail data generator for RetailIQ
export const generateSampleCSV = () => {
  const products = [
    { id: 'P001', name: 'Wireless Headphones', category: 'Electronics', price: 99.99 },
    { id: 'P002', name: 'Coffee Maker', category: 'Appliances', price: 79.99 },
    { id: 'P003', name: 'Bluetooth Speaker', category: 'Electronics', price: 49.99 },
    { id: 'P004', name: 'Yoga Mat', category: 'Fitness', price: 29.99 },
    { id: 'P005', name: 'Office Chair', category: 'Furniture', price: 199.99 },
    { id: 'P006', name: 'Smartphone Case', category: 'Accessories', price: 19.99 },
    { id: 'P007', name: 'Water Bottle', category: 'Sports', price: 24.99 },
    { id: 'P008', name: 'Desk Lamp', category: 'Furniture', price: 39.99 },
    { id: 'P009', name: 'Running Shoes', category: 'Footwear', price: 129.99 },
    { id: 'P010', name: 'Kitchen Scale', category: 'Appliances', price: 34.99 },
    { id: 'P011', name: 'Tablet Stand', category: 'Accessories', price: 15.99 },
    { id: 'P012', name: 'Protein Powder', category: 'Supplements', price: 59.99 },
    { id: 'P013', name: 'Gaming Mouse', category: 'Electronics', price: 69.99 },
    { id: 'P014', name: 'Backpack', category: 'Bags', price: 89.99 },
    { id: 'P015', name: 'Air Freshener', category: 'Home', price: 12.99 }
  ];

  const customers = ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010'];
  
  // Generate dates for the last 6 months
  const startDate = new Date();
  startDate.setMonth(startDate.getMonth() - 6);
  
  const data = [];
  let transactionId = 1000;
  
  // Generate 200 transactions with realistic patterns
  for (let i = 0; i < 200; i++) {
    const currentTransactionId = `T${transactionId++}`;
    const customerId = customers[Math.floor(Math.random() * customers.length)];
    
    // Random date within the last 6 months
    const randomDate = new Date(startDate.getTime() + Math.random() * (Date.now() - startDate.getTime()));
    const dateStr = randomDate.toISOString().split('T')[0];
    
    // Each transaction can have 1-4 items
    const itemsInTransaction = Math.floor(Math.random() * 4) + 1;
    const usedProducts = new Set();
    
    for (let j = 0; j < itemsInTransaction; j++) {
      let product;
      // Ensure no duplicate products in the same transaction
      do {
        product = products[Math.floor(Math.random() * products.length)];
      } while (usedProducts.has(product.id));
      
      usedProducts.add(product.id);
      
      // Realistic quantity (1-5 items, weighted towards 1-2)
      const quantity = Math.random() < 0.7 ? 1 : Math.random() < 0.9 ? 2 : Math.floor(Math.random() * 4) + 3;
      
      // Some price variation (±10%)
      const priceVariation = 0.9 + Math.random() * 0.2;
      const actualPrice = Math.round(product.price * priceVariation * 100) / 100;
      
      data.push({
        TransactionID: currentTransactionId,
        ProductID: product.id,
        ProductName: product.name,
        Category: product.category,
        Price: actualPrice,
        Quantity: quantity,
        Date: dateStr,
        CustomerID: customerId
      });
    }
  }
  
  // Sort by date
  data.sort((a, b) => new Date(a.Date) - new Date(b.Date));
  
  return data;
};

export const convertToCSV = (data) => {
  if (!data || data.length === 0) return '';
  
  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => 
      headers.map(header => {
        const value = row[header];
        // Escape commas and quotes in values
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      }).join(',')
    )
  ].join('\n');
  
  return csvContent;
};

export const downloadSampleCSV = () => {
  const sampleData = generateSampleCSV();
  const csvContent = convertToCSV(sampleData);
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'retailiq_sample_data.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

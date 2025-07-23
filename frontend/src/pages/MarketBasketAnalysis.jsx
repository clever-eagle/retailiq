import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Progress } from '../components/ui/progress'
import { Alert, AlertDescription } from '../components/ui/alert'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, ScatterChart, Scatter
} from 'recharts'
import { 
  ShoppingCart, TrendingUp, Users, Package, Download, 
  RefreshCw, ArrowRight, Target, DollarSign, Lightbulb, AlertCircle
} from 'lucide-react'
import { 
  loadCSVData,
  processMarketBasketData,
  processCustomerSegments
} from '../utils/csvDataProcessor'
import { generateCrossSellOpportunities } from '../utils/detailedMockData'

function MarketBasketAnalysis() {
  const [associationRules, setAssociationRules] = useState([])
  const [crossSellOpportunities, setCrossSellOpportunities] = useState([])
  const [customerSegments, setCustomerSegments] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedMetric, setSelectedMetric] = useState('lift')
  const [minSupport, setMinSupport] = useState(0.05)
  const [minConfidence, setMinConfidence] = useState(0.5)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Load and process real CSV data for market basket analysis
    const loadData = async () => {
      setLoading(true)
      setError(null)
      
      try {
        // Simulate loading time for better UX
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Load CSV data
        const transactions = await loadCSVData()
        console.log('Loaded transactions for basket analysis:', transactions.length)
        
        // Process the data for market basket analysis
        const basketData = processMarketBasketData(transactions)
        const customerData = processCustomerSegments(transactions)
        
        setAssociationRules(basketData.associationRules)
        setCustomerSegments(customerData)
        
        // Generate cross-sell opportunities (can be enhanced with real data later)
        setCrossSellOpportunities(generateCrossSellOpportunities())
        
      } catch (err) {
        console.error('Error loading market basket data:', err)
        setError('Failed to load transaction data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [minSupport, minConfidence])

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
  }

  const getStrengthColor = (strength) => {
    switch (strength.toLowerCase()) {
      case 'very strong': return 'bg-green-100 text-green-800'
      case 'strong': return 'bg-blue-100 text-blue-800'
      case 'moderate': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const prepareSegmentData = () => {
    return customerSegments.map(segment => ({
      name: segment.segment,
      size: segment.size,
      value: segment.avgOrderValue
    }))
  }

  const COLORS = ['#2563eb', '#dc2626', '#16a34a', '#ca8a04', '#9333ea']

  if (loading) {
    return (
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Market Basket Analysis</h1>
            <p className="text-gray-600">Discover product associations and purchasing patterns</p>
          </div>
          
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <RefreshCw className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
              <p className="text-gray-600">Analyzing purchase patterns and generating association rules...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Market Basket Analysis</h1>
            <p className="text-gray-600">Discover product associations and purchasing patterns</p>
          </div>
          
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error}
            </AlertDescription>
          </Alert>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Market Basket Analysis</h1>
              <p className="text-gray-600">Discover product associations and purchasing patterns</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export Rules
              </Button>
              <Button size="sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh Analysis
              </Button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Association Rules</p>
                    <p className="text-2xl font-bold text-blue-600">{associationRules.length}</p>
                  </div>
                  <ShoppingCart className="h-8 w-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Cross-sell Revenue</p>
                    <p className="text-2xl font-bold text-green-600">
                      {formatCurrency(crossSellOpportunities.reduce((sum, opp) => sum + opp.potentialRevenue, 0))}
                    </p>
                  </div>
                  <DollarSign className="h-8 w-8 text-green-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Customer Segments</p>
                    <p className="text-2xl font-bold text-purple-600">{customerSegments.length}</p>
                  </div>
                  <Users className="h-8 w-8 text-purple-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Strong Rules</p>
                    <p className="text-2xl font-bold text-orange-600">
                      {associationRules.filter(rule => rule.strength === 'Strong' || rule.strength === 'Very Strong').length}
                    </p>
                  </div>
                  <Target className="h-8 w-8 text-orange-600" />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Analysis Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Analysis Parameters</CardTitle>
            <CardDescription>Adjust thresholds to refine association rules</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Support: {minSupport.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.01"
                  max="0.2"
                  step="0.01"
                  value={minSupport}
                  onChange={(e) => setMinSupport(parseFloat(e.target.value))}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Minimum frequency of item combinations
                </p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Confidence: {minConfidence.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="0.9"
                  step="0.05"
                  value={minConfidence}
                  onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Reliability of the association rule
                </p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort by Metric
                </label>
                <div className="flex gap-2">
                  <Button 
                    variant={selectedMetric === 'lift' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedMetric('lift')}
                  >
                    Lift
                  </Button>
                  <Button 
                    variant={selectedMetric === 'confidence' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedMetric('confidence')}
                  >
                    Confidence
                  </Button>
                  <Button 
                    variant={selectedMetric === 'support' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedMetric('support')}
                  >
                    Support
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Association Rules Table */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Association Rules</CardTitle>
            <CardDescription>
              Product combinations with statistical significance (sorted by {selectedMetric})
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium">Rule</th>
                    <th className="text-left py-3 px-4 font-medium">Support</th>
                    <th className="text-left py-3 px-4 font-medium">Confidence</th>
                    <th className="text-left py-3 px-4 font-medium">Lift</th>
                    <th className="text-left py-3 px-4 font-medium">Strength</th>
                    <th className="text-left py-3 px-4 font-medium">Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {associationRules
                    .sort((a, b) => b[selectedMetric] - a[selectedMetric])
                    .map((rule, index) => (
                    <tr key={rule.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="text-sm">
                            <div className="font-medium text-gray-900">
                              {rule.antecedent.join(', ')}
                            </div>
                            <div className="flex items-center text-gray-600 mt-1">
                              <ArrowRight className="h-3 w-3 mr-1" />
                              {rule.consequent.join(', ')}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm font-medium">{(rule.support * 100).toFixed(1)}%</div>
                        <div className="text-xs text-gray-500">{rule.transactions} txns</div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm font-medium">{(rule.confidence * 100).toFixed(1)}%</div>
                        <Progress value={rule.confidence * 100} className="h-1 mt-1" />
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm font-medium">{rule.lift.toFixed(2)}</div>
                        <div className="text-xs text-gray-500">
                          {rule.lift > 1 ? 'Positive' : 'Negative'}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <Badge variant="outline" className={getStrengthColor(rule.strength)}>
                          {rule.strength}
                        </Badge>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-sm font-medium text-green-600">
                          {formatCurrency(rule.expectedRevenue)}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Cross-sell Opportunities & Customer Segments */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Card>
            <CardHeader>
              <CardTitle>Cross-sell Opportunities</CardTitle>
              <CardDescription>Recommended product bundles for increased revenue</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {crossSellOpportunities.map((opportunity, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="font-medium text-gray-900">{opportunity.product}</h4>
                        <p className="text-sm text-gray-600">Base Product</p>
                      </div>
                      <Badge variant="outline" className="bg-green-100 text-green-800">
                        {opportunity.successRate}% Success Rate
                      </Badge>
                    </div>
                    
                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-700 mb-1">Recommended Bundle:</p>
                      <div className="flex flex-wrap gap-1">
                        {opportunity.recommendations.map((rec, idx) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            {rec}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex justify-between items-center text-sm">
                      <div>
                        <span className="font-medium text-green-600">
                          {formatCurrency(opportunity.potentialRevenue)}
                        </span>
                        <span className="text-gray-600"> potential revenue</span>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{opportunity.bundle}</div>
                        <div className="text-gray-600">{opportunity.discount}% bundle discount</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Customer Segments</CardTitle>
              <CardDescription>Distinct purchasing behavior patterns</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={prepareSegmentData()}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="size"
                      label={({ name, size }) => `${name}: ${size}%`}
                    >
                      {prepareSegmentData().map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value}%`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <div className="space-y-3">
                {customerSegments.map((segment, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-900">{segment.segment}</h4>
                      <div className="text-right">
                        <div className="text-sm font-bold">{segment.size}%</div>
                        <div className="text-xs text-gray-600">of customers</div>
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-2">
                      Avg Order: <span className="font-medium">{formatCurrency(segment.avgOrderValue)}</span>
                    </div>
                    
                    <div className="mb-2">
                      <p className="text-xs text-gray-500 mb-1">Top Products:</p>
                      <div className="flex flex-wrap gap-1">
                        {segment.topProducts.map((product, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs">
                            {product}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-700">
                      <strong>Pattern:</strong> {segment.behaviorPattern}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Insights and Recommendations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Key Insights</CardTitle>
              <CardDescription>Important findings from the analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Alert>
                  <Lightbulb className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Strongest Association:</strong> {associationRules[0]?.antecedent.join(', ')} → {associationRules[0]?.consequent.join(', ')} with {associationRules[0]?.lift.toFixed(2)}x lift
                  </AlertDescription>
                </Alert>
                
                <Alert>
                  <TrendingUp className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Revenue Opportunity:</strong> Cross-selling could generate {formatCurrency(crossSellOpportunities.reduce((sum, opp) => sum + opp.potentialRevenue, 0))} additional revenue
                  </AlertDescription>
                </Alert>
                
                <Alert>
                  <Users className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Customer Segmentation:</strong> {customerSegments[0]?.segment} segment shows highest value with {formatCurrency(customerSegments[0]?.avgOrderValue)} average order
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Actionable Recommendations</CardTitle>
              <CardDescription>Strategic actions based on analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-medium text-blue-900">Product Placement</h4>
                  <p className="text-sm text-blue-800 mt-1">
                    Place {associationRules[0]?.antecedent.join(', ')} near {associationRules[0]?.consequent.join(', ')} to increase cross-sells.
                  </p>
                </div>
                
                <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                  <h4 className="font-medium text-green-900">Bundle Creation</h4>
                  <p className="text-sm text-green-800 mt-1">
                    Create "{crossSellOpportunities[0]?.bundle}" bundle with {crossSellOpportunities[0]?.discount}% discount to drive sales.
                  </p>
                </div>
                
                <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                  <h4 className="font-medium text-purple-900">Targeted Marketing</h4>
                  <p className="text-sm text-purple-800 mt-1">
                    Focus campaigns on {customerSegments[0]?.segment} segment for maximum ROI.
                  </p>
                </div>
                
                <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                  <h4 className="font-medium text-yellow-900">Inventory Optimization</h4>
                  <p className="text-sm text-yellow-800 mt-1">
                    Stock complementary products together based on association rules.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Educational Section */}
        <div className="mt-6 bg-green-50 p-6 rounded-lg border border-green-200">
          <h4 className="text-lg font-semibold text-green-900 mb-3">
            Understanding Market Basket Analysis
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-green-800">
            <div>
              <h5 className="font-medium mb-2">Support</h5>
              <p>How frequently items appear together relative to all transactions. Higher support indicates more common associations.</p>
            </div>
            <div>
              <h5 className="font-medium mb-2">Confidence</h5>
              <p>The likelihood that consequent items are purchased when antecedent items are bought. Measures rule reliability.</p>
            </div>
            <div>
              <h5 className="font-medium mb-2">Lift</h5>
              <p>How much more likely the consequent is to be bought when the antecedent is purchased. Lift {'>'}  1 indicates positive association.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MarketBasketAnalysis

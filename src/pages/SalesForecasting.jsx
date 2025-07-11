function SalesForecasting() {
  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Sales Forecasting</h1>
          <p className="text-gray-600">
            AI-powered sales predictions based on historical data
          </p>
        </div>

        {/* Placeholder content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Configuration Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Forecast Settings
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                Parameter configuration will be implemented in later stages.
              </p>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Forecast Period
                  </label>
                  <div className="text-sm text-gray-500">Coming soon...</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Product Selection
                  </label>
                  <div className="text-sm text-gray-500">Coming soon...</div>
                </div>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Forecast Results
              </h3>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
                <p className="text-gray-600 mb-2">
                  Interactive charts and forecast visualization will be displayed here.
                </p>
                <p className="text-sm text-gray-500">
                  Using Prophet algorithm for time series forecasting
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SalesForecasting

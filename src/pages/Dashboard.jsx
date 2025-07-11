function Dashboard() {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">
            Welcome to RetailIQ - Your AI-powered retail analytics platform
          </p>
        </div>

        {/* Placeholder content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Quick Stats
            </h3>
            <p className="text-gray-600">
              Dashboard overview content will be implemented in later stages.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Recent Analysis
            </h3>
            <p className="text-gray-600">
              Recent analysis results will be displayed here.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Data Status
            </h3>
            <p className="text-gray-600">
              Current data upload and processing status.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

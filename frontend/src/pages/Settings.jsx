function Settings() {
  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
          <p className="text-gray-600">
            Configure your RetailIQ preferences and account settings
          </p>
        </div>

        {/* Placeholder content */}
        <div className="space-y-6">
          {/* Account Settings */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Account Settings
            </h3>
            <p className="text-gray-600 text-sm">
              User account management features will be implemented in later stages.
            </p>
          </div>

          {/* Data Settings */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Data Preferences
            </h3>
            <p className="text-gray-600 text-sm">
              Configure default data processing and analysis settings.
            </p>
          </div>

          {/* Application Settings */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Application Settings
            </h3>
            <p className="text-gray-600 text-sm">
              Theme, notifications, and other application preferences.
            </p>
          </div>

          {/* About */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              About RetailIQ
            </h3>
            <div className="text-sm text-gray-600 space-y-2">
              <p>
                <strong>Version:</strong> 1.0.0
              </p>
              <p>
                <strong>Description:</strong> AI-Driven Sales Forecasting and Market Basket Analysis System
              </p>
              <p>
                <strong>Purpose:</strong> Helping retail businesses make smarter, faster, and more informed decisions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings

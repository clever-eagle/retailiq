function DataUpload() {
  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Data Upload</h1>
          <p className="text-gray-600">
            Upload your retail sales data for analysis
          </p>
        </div>

        {/* Placeholder content */}
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Upload Dataset
          </h3>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <p className="text-gray-600 mb-2">
              File upload functionality will be implemented in later stages.
            </p>
            <p className="text-sm text-gray-500">
              Supported formats: CSV, Excel (.xlsx, .xls)
            </p>
          </div>
        </div>

        {/* Expected data format info */}
        <div className="mt-6 bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h4 className="text-lg font-semibold text-blue-900 mb-3">
            Expected Data Format
          </h4>
          <div className="text-sm text-blue-800">
            <p className="mb-2">Your data should include the following columns:</p>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>Product:</strong> Name or ID of the product</li>
              <li><strong>Date:</strong> Date of the sale/transaction</li>
              <li><strong>Units Sold:</strong> Quantity sold</li>
              <li><strong>Price:</strong> Unit price</li>
              <li><strong>Category:</strong> Product category</li>
              <li><strong>TransactionID:</strong> Unique transaction identifier (required for Market Basket Analysis)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DataUpload

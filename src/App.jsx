import { useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import DataUpload from './pages/DataUpload'
import SalesForecasting from './pages/SalesForecasting'
import MarketBasketAnalysis from './pages/MarketBasketAnalysis'
import Settings from './pages/Settings'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'data-upload':
        return <DataUpload />
      case 'sales-forecasting':
        return <SalesForecasting />
      case 'market-basket-analysis':
        return <MarketBasketAnalysis />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="flex-1 overflow-auto md:ml-0">
        {renderPage()}
      </main>
    </div>
  )
}

export default App

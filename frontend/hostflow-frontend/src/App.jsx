import { useState } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import ClientBooking from './components/ClientBooking'
import Chatbot from './components/Chatbot'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [viewMode, setViewMode] = useState('client') // 'client', 'login', 'register', or 'admin'
  const [currentPage, setCurrentPage] = useState('client') // Para controlar a navegação

  const handleLogin = (userData) => {
    setIsLoggedIn(true)
    setViewMode('admin')
    setCurrentPage('admin')
  }

  const handleRegister = (userData) => {
    setIsLoggedIn(true)
    setViewMode('admin')
    setCurrentPage('admin')
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setViewMode('client')
    setCurrentPage('client')
  }

  const switchToClientView = () => {
    setViewMode('client')
    setCurrentPage('client')
    setIsLoggedIn(false)
  }

  const switchToLogin = () => {
    setViewMode('login')
    setCurrentPage('login')
  }

  const switchToRegister = () => {
    setViewMode('register')
    setCurrentPage('register')
  }

  const switchToAdmin = () => {
    if (isLoggedIn) {
      setViewMode('admin')
      setCurrentPage('admin')
    } else {
      switchToLogin()
    }
  }

  // Renderização baseada no estado atual
  if (currentPage === 'login' || (viewMode === 'admin' && !isLoggedIn)) {
    return <Login onLogin={handleLogin} onSwitchToClient={switchToClientView} onSwitchToRegister={switchToRegister} />
  }

  if (currentPage === 'register') {
    return <Register onRegister={handleRegister} onSwitchToClient={switchToClientView} onSwitchToLogin={switchToLogin} />
  }

  if (currentPage === 'admin' && isLoggedIn) {
    return <Dashboard onLogout={handleLogout} onSwitchToClient={switchToClientView} />
  }

  // Página padrão - área do cliente
  return (
    <>
      <ClientBooking onSwitchToAdmin={switchToLogin} onSwitchToRegister={switchToRegister} />
      <Chatbot />
    </>
  )
}

export default App


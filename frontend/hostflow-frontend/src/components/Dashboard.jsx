import { useState } from 'react'
import { Home, Building, Bed, Users, Calendar, Bot, BarChart3, DollarSign, TrendingUp, Clock } from 'lucide-react'
import AIAgent from './AIAgent'
import Properties from './Properties'
import Accommodations from './Accommodations'
import Guests from './Guests'
import Bookings from './Bookings'

const Dashboard = ({ onLogout }) => {
  const [activeSection, setActiveSection] = useState('dashboard')
  const [stats, setStats] = useState({
    monthly_revenue: 45230,
    occupancy_rate: 78,
    active_guests: 142,
    today_checkins: 12
  })

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'properties', label: 'Pousadas', icon: Building },
    { id: 'accommodations', label: 'Acomodações', icon: Bed },
    { id: 'guests', label: 'Hóspedes', icon: Users },
    { id: 'bookings', label: 'Reservas', icon: Calendar },
    { id: 'ai-agent', label: 'Agente de IA', icon: Bot }
  ]

  const renderContent = () => {
    switch (activeSection) {
      case 'properties':
        return <Properties />
      case 'accommodations':
        return <Accommodations />
      case 'guests':
        return <Guests />
      case 'bookings':
        return <Bookings />
      case 'ai-agent':
        return <AIAgent />
      default:
        return (
          <div className="space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Visão geral do seu negócio</p>
            </div>

            {/* Métricas principais */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Receita Mensal</p>
                    <p className="text-2xl font-bold text-gray-900">R$ {stats.monthly_revenue.toLocaleString()}</p>
                  </div>
                  <div className="p-3 bg-green-100 rounded-full">
                    <DollarSign className="h-6 w-6 text-green-600" />
                  </div>
                </div>
                <div className="mt-4 flex items-center">
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+12% vs mês anterior</span>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Taxa de Ocupação</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.occupancy_rate}%</p>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-full">
                    <BarChart3 className="h-6 w-6 text-blue-600" />
                  </div>
                </div>
                <div className="mt-4 flex items-center">
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+5% vs mês anterior</span>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Hóspedes Ativos</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.active_guests}</p>
                  </div>
                  <div className="p-3 bg-purple-100 rounded-full">
                    <Users className="h-6 w-6 text-purple-600" />
                  </div>
                </div>
                <div className="mt-4 flex items-center">
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+8% vs mês anterior</span>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Check-ins Hoje</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.today_checkins}</p>
                  </div>
                  <div className="p-3 bg-orange-100 rounded-full">
                    <Clock className="h-6 w-6 text-orange-600" />
                  </div>
                </div>
                <div className="mt-4 flex items-center">
                  <span className="text-sm text-gray-600">3 check-outs programados</span>
                </div>
              </div>
            </div>

            {/* Gráficos e informações adicionais */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Reservas Recentes</h3>
                <div className="space-y-4">
                  {[
                    { guest: 'Maria Silva', accommodation: 'Quarto Vista Mar', checkin: '2024-01-15', status: 'confirmed' },
                    { guest: 'João Santos', accommodation: 'Chalé Romântico', checkin: '2024-01-16', status: 'checked_in' },
                    { guest: 'Ana Costa', accommodation: 'Suíte Master', checkin: '2024-01-18', status: 'pending' }
                  ].map((booking, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900">{booking.guest}</p>
                        <p className="text-sm text-gray-600">{booking.accommodation}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-900">{booking.checkin}</p>
                        <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                          booking.status === 'confirmed' ? 'bg-blue-100 text-blue-800' :
                          booking.status === 'checked_in' ? 'bg-green-100 text-green-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {booking.status === 'confirmed' ? 'Confirmada' :
                           booking.status === 'checked_in' ? 'Check-in' : 'Pendente'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights do Agente de IA</h3>
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                    <h4 className="font-medium text-blue-900">Oportunidade de Receita</h4>
                    <p className="text-sm text-blue-700 mt-1">
                      Aumente os preços em 15% para finais de semana de janeiro. Demanda alta detectada.
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-400">
                    <h4 className="font-medium text-green-900">Performance Excelente</h4>
                    <p className="text-sm text-green-700 mt-1">
                      Taxa de ocupação 23% acima da média regional. Continue com a estratégia atual.
                    </p>
                  </div>
                  <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                    <h4 className="font-medium text-yellow-900">Atenção Necessária</h4>
                    <p className="text-sm text-yellow-700 mt-1">
                      3 hóspedes com check-in atrasado. Considere enviar lembretes automáticos.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">H</span>
                </div>
                <span className="text-xl font-bold text-gray-900">HostFlow</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Bem-vindo, Demo User</span>
              <button
                onClick={onLogout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-sm min-h-screen">
          <nav className="p-4">
            <ul className="space-y-2">
              {menuItems.map((item) => {
                const Icon = item.icon
                return (
                  <li key={item.id}>
                    <button
                      onClick={() => setActiveSection(item.id)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                        activeSection === item.id
                          ? 'bg-red-50 text-red-700 border-r-2 border-red-500'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      <span className="font-medium">{item.label}</span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  )
}

export default Dashboard


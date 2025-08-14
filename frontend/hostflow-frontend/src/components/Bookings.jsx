import { useState, useEffect } from 'react'
import { Plus, Edit, Calendar, User, MapPin, DollarSign, Clock, CheckCircle, XCircle, AlertCircle, Filter } from 'lucide-react'

const Bookings = () => {
  const [bookings, setBookings] = useState([])
  const [properties, setProperties] = useState([])
  const [accommodations, setAccommodations] = useState([])
  const [guests, setGuests] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingBooking, setEditingBooking] = useState(null)
  const [filters, setFilters] = useState({
    status: '',
    property_id: '',
    date_from: '',
    date_to: ''
  })
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [formData, setFormData] = useState({
    property_id: '',
    accommodation_id: '',
    guest_id: '',
    check_in_date: '',
    check_out_date: '',
    adults: 1,
    children: 0,
    special_requests: '',
    source: 'direct'
  })

  const statusOptions = [
    { value: '', label: 'Todos os Status' },
    { value: 'pending', label: 'Pendente' },
    { value: 'confirmed', label: 'Confirmada' },
    { value: 'checked_in', label: 'Check-in' },
    { value: 'checked_out', label: 'Check-out' },
    { value: 'cancelled', label: 'Cancelada' },
    { value: 'no_show', label: 'No-show' }
  ]

  const sourceOptions = [
    { value: 'direct', label: 'Direto' },
    { value: 'booking.com', label: 'Booking.com' },
    { value: 'airbnb', label: 'Airbnb' },
    { value: 'expedia', label: 'Expedia' },
    { value: 'phone', label: 'Telefone' },
    { value: 'email', label: 'Email' }
  ]

  useEffect(() => {
    fetchBookings()
    fetchProperties()
    fetchGuests()
  }, [currentPage, filters])

  useEffect(() => {
    if (formData.property_id) {
      fetchAccommodations(formData.property_id)
    }
  }, [formData.property_id])

  const fetchBookings = async () => {
    try {
      const params = new URLSearchParams({
        page: currentPage,
        per_page: 10,
        ...Object.fromEntries(Object.entries(filters).filter(([_, v]) => v))
      })
      
      const response = await fetch(`/api/bookings?${params}`)
      const data = await response.json()
      setBookings(data.bookings || [])
      setTotalPages(data.pages || 1)
    } catch (error) {
      console.error('Erro ao carregar reservas:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchProperties = async () => {
    try {
      const response = await fetch('/api/properties')
      const data = await response.json()
      setProperties(data)
    } catch (error) {
      console.error('Erro ao carregar pousadas:', error)
    }
  }

  const fetchAccommodations = async (propertyId) => {
    try {
      const response = await fetch(`/api/accommodations?property_id=${propertyId}`)
      const data = await response.json()
      setAccommodations(data)
    } catch (error) {
      console.error('Erro ao carregar acomodações:', error)
    }
  }

  const fetchGuests = async () => {
    try {
      const response = await fetch('/api/guests?per_page=100')
      const data = await response.json()
      setGuests(data.guests || [])
    } catch (error) {
      console.error('Erro ao carregar hóspedes:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const url = editingBooking ? `/api/bookings/${editingBooking.id}` : '/api/bookings'
      const method = editingBooking ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          adults: parseInt(formData.adults),
          children: parseInt(formData.children)
        })
      })

      if (response.ok) {
        fetchBookings()
        resetForm()
      } else {
        const error = await response.json()
        alert(error.error || 'Erro ao salvar reserva')
      }
    } catch (error) {
      console.error('Erro ao salvar reserva:', error)
      alert('Erro ao salvar reserva')
    }
  }

  const handleStatusChange = async (bookingId, action) => {
    try {
      const response = await fetch(`/api/bookings/${bookingId}/${action}`, {
        method: 'POST'
      })
      
      if (response.ok) {
        fetchBookings()
      } else {
        const error = await response.json()
        alert(error.error || `Erro ao ${action} reserva`)
      }
    } catch (error) {
      console.error(`Erro ao ${action} reserva:`, error)
    }
  }

  const handleCancel = async (bookingId) => {
    const reason = prompt('Motivo do cancelamento (opcional):')
    if (reason !== null) {
      try {
        const response = await fetch(`/api/bookings/${bookingId}/cancel`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ reason })
        })
        
        if (response.ok) {
          fetchBookings()
        } else {
          const error = await response.json()
          alert(error.error || 'Erro ao cancelar reserva')
        }
      } catch (error) {
        console.error('Erro ao cancelar reserva:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      property_id: '',
      accommodation_id: '',
      guest_id: '',
      check_in_date: '',
      check_out_date: '',
      adults: 1,
      children: 0,
      special_requests: '',
      source: 'direct'
    })
    setEditingBooking(null)
    setShowForm(false)
    setAccommodations([])
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock, label: 'Pendente' },
      confirmed: { color: 'bg-blue-100 text-blue-800', icon: CheckCircle, label: 'Confirmada' },
      checked_in: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Check-in' },
      checked_out: { color: 'bg-gray-100 text-gray-800', icon: CheckCircle, label: 'Check-out' },
      cancelled: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'Cancelada' },
      no_show: { color: 'bg-red-100 text-red-800', icon: AlertCircle, label: 'No-show' }
    }
    
    const config = statusConfig[status] || statusConfig.pending
    const Icon = config.icon
    
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        <Icon className="h-3 w-3" />
        {config.label}
      </span>
    )
  }

  const getActionButtons = (booking) => {
    const buttons = []
    
    if (booking.can_check_in) {
      buttons.push(
        <button
          key="checkin"
          onClick={() => handleStatusChange(booking.id, 'check-in')}
          className="text-green-600 hover:text-green-800 text-sm"
        >
          Check-in
        </button>
      )
    }
    
    if (booking.can_check_out) {
      buttons.push(
        <button
          key="checkout"
          onClick={() => handleStatusChange(booking.id, 'check-out')}
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          Check-out
        </button>
      )
    }
    
    if (booking.status === 'pending') {
      buttons.push(
        <button
          key="confirm"
          onClick={() => handleStatusChange(booking.id, 'confirm')}
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          Confirmar
        </button>
      )
    }
    
    if (booking.can_cancel) {
      buttons.push(
        <button
          key="cancel"
          onClick={() => handleCancel(booking.id)}
          className="text-red-600 hover:text-red-800 text-sm"
        >
          Cancelar
        </button>
      )
    }
    
    return buttons
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reservas</h1>
          <p className="text-gray-600">Gerencie todas as reservas</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Nova Reserva
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              {statusOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Pousada</label>
            <select
              value={filters.property_id}
              onChange={(e) => setFilters(prev => ({ ...prev, property_id: e.target.value }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option value="">Todas as Pousadas</option>
              {properties.map(property => (
                <option key={property.id} value={property.id}>
                  {property.name}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Data Início</label>
            <input
              type="date"
              value={filters.date_from}
              onChange={(e) => setFilters(prev => ({ ...prev, date_from: e.target.value }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Data Fim</label>
            <input
              type="date"
              value={filters.date_to}
              onChange={(e) => setFilters(prev => ({ ...prev, date_to: e.target.value }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {editingBooking ? 'Editar Reserva' : 'Nova Reserva'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Pousada *
                  </label>
                  <select
                    required
                    value={formData.property_id}
                    onChange={(e) => setFormData(prev => ({ ...prev, property_id: e.target.value, accommodation_id: '' }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  >
                    <option value="">Selecione uma pousada</option>
                    {properties.map(property => (
                      <option key={property.id} value={property.id}>
                        {property.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Acomodação *
                  </label>
                  <select
                    required
                    value={formData.accommodation_id}
                    onChange={(e) => setFormData(prev => ({ ...prev, accommodation_id: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    disabled={!formData.property_id}
                  >
                    <option value="">Selecione uma acomodação</option>
                    {accommodations.map(accommodation => (
                      <option key={accommodation.id} value={accommodation.id}>
                        {accommodation.name} - R$ {accommodation.base_price}/noite
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hóspede *
                </label>
                <select
                  required
                  value={formData.guest_id}
                  onChange={(e) => setFormData(prev => ({ ...prev, guest_id: e.target.value }))}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                >
                  <option value="">Selecione um hóspede</option>
                  {guests.map(guest => (
                    <option key={guest.id} value={guest.id}>
                      {guest.full_name} - {guest.email}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Check-in *
                  </label>
                  <input
                    type="date"
                    required
                    value={formData.check_in_date}
                    onChange={(e) => setFormData(prev => ({ ...prev, check_in_date: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Check-out *
                  </label>
                  <input
                    type="date"
                    required
                    value={formData.check_out_date}
                    onChange={(e) => setFormData(prev => ({ ...prev, check_out_date: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Adultos *
                  </label>
                  <input
                    type="number"
                    required
                    min="1"
                    value={formData.adults}
                    onChange={(e) => setFormData(prev => ({ ...prev, adults: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Crianças
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={formData.children}
                    onChange={(e) => setFormData(prev => ({ ...prev, children: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Origem
                  </label>
                  <select
                    value={formData.source}
                    onChange={(e) => setFormData(prev => ({ ...prev, source: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  >
                    {sourceOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Solicitações Especiais
                </label>
                <textarea
                  value={formData.special_requests}
                  onChange={(e) => setFormData(prev => ({ ...prev, special_requests: e.target.value }))}
                  rows={3}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                >
                  {editingBooking ? 'Atualizar' : 'Criar'} Reserva
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Lista de Reservas */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reserva
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Hóspede
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acomodação
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Período
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {bookings.map(booking => (
                <tr key={booking.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {booking.booking_code}
                      </div>
                      <div className="text-sm text-gray-500">
                        {booking.source}
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-3">
                        <User className="h-4 w-4 text-red-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {booking.guest_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {booking.total_guests} hóspede(s)
                        </div>
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {booking.accommodation_name}
                      </div>
                      <div className="text-sm text-gray-500">
                        {booking.property_name}
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm text-gray-900">
                        {new Date(booking.check_in_date).toLocaleDateString('pt-BR')} -
                      </div>
                      <div className="text-sm text-gray-900">
                        {new Date(booking.check_out_date).toLocaleDateString('pt-BR')}
                      </div>
                      <div className="text-sm text-gray-500">
                        {booking.nights} noite(s)
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      R$ {booking.total_amount.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">
                      {booking.payment_status}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(booking.status)}
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <div className="flex flex-col space-y-1">
                      {getActionButtons(booking)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Paginação */}
      {totalPages > 1 && (
        <div className="flex justify-center space-x-2">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Anterior
          </button>
          
          <span className="px-3 py-2 text-sm text-gray-600">
            Página {currentPage} de {totalPages}
          </span>
          
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Próxima
          </button>
        </div>
      )}

      {bookings.length === 0 && !loading && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Calendar className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhuma reserva encontrada
          </h3>
          <p className="text-gray-600 mb-4">
            {Object.values(filters).some(v => v) ? 'Tente ajustar os filtros' : 'Comece criando sua primeira reserva'}
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
          >
            Criar Reserva
          </button>
        </div>
      )}
    </div>
  )
}

export default Bookings


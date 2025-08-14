import { useState, useEffect } from 'react'
import { Search, MapPin, Calendar, Users, Star, Wifi, Car, Coffee, Waves, Mountain, Heart, Filter } from 'lucide-react'

const ClientBooking = ({ onSwitchToAdmin, onSwitchToRegister }) => {
  const [searchParams, setSearchParams] = useState({
    destination: '',
    checkin: '',
    checkout: '',
    guests: 1
  })
  const [properties, setProperties] = useState([])
  const [accommodations, setAccommodations] = useState([])
  const [filteredAccommodations, setFilteredAccommodations] = useState([])
  const [selectedProperty, setSelectedProperty] = useState(null)
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({
    priceRange: [0, 1000],
    type: '',
    amenities: []
  })
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    fetchProperties()
    fetchAccommodations()
  }, [])

  useEffect(() => {
    filterAccommodations()
  }, [accommodations, searchParams, filters])

  const fetchProperties = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/properties')
      const data = await response.json()
      setProperties(data)
    } catch (error) {
      console.error('Erro ao buscar pousadas:', error)
    }
  }

  const fetchAccommodations = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/accommodations')
      const data = await response.json()
      setAccommodations(data)
    } catch (error) {
      console.error('Erro ao buscar acomodações:', error)
    }
  }

  const filterAccommodations = () => {
    let filtered = accommodations.filter(acc => acc.is_available)

    if (searchParams.destination) {
      const property = properties.find(p => p.id === parseInt(searchParams.destination))
      if (property) {
        filtered = filtered.filter(acc => acc.property_id === property.id)
      }
    }

    if (filters.type) {
      filtered = filtered.filter(acc => acc.type === filters.type)
    }

    if (filters.priceRange) {
      filtered = filtered.filter(acc => 
        acc.price_per_night >= filters.priceRange[0] && 
        acc.price_per_night <= filters.priceRange[1]
      )
    }

    setFilteredAccommodations(filtered)
  }

  const handleReservation = (accommodation) => {
    alert(`Reserva iniciada para ${accommodation.name}!\n\nEm um sistema real, isso abriria um formulário de reserva com:\n- Dados do hóspede\n- Datas de check-in/check-out\n- Forma de pagamento\n- Confirmação da reserva`)
  }

  const handleSearch = (e) => {
    e.preventDefault()
    filterAccommodations()
  }

  const toggleFavorite = (accommodationId) => {
    setFavorites(prev => 
      prev.includes(accommodationId) 
        ? prev.filter(id => id !== accommodationId)
        : [...prev, accommodationId]
    )
  }

  const getPropertyName = (propertyId) => {
    const property = properties.find(p => p.id === propertyId)
    return property ? property.name : 'Pousada'
  }

  const getPropertyLocation = (propertyId) => {
    const property = properties.find(p => p.id === propertyId)
    return property ? `${property.city}, ${property.state}` : 'Localização'
  }

  const getAmenityIcon = (amenity) => {
    const icons = {
      'wifi': Wifi,
      'estacionamento': Car,
      'cafe': Coffee,
      'piscina': Waves,
      'vista': Mountain
    }
    return icons[amenity.toLowerCase()] || Coffee
  }

  const accommodationTypes = [...new Set(accommodations.map(acc => acc.type))]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">H</span>
              </div>
              <span className="text-xl font-bold text-gray-900">HostFlow</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-700 hover:text-red-600">Hospedagens</a>
              <a href="#" className="text-gray-700 hover:text-red-600">Experiências</a>
              <a href="#" className="text-gray-700 hover:text-red-600">Contato</a>
            </nav>
            <div className="flex items-center space-x-4">
              <button 
                onClick={onSwitchToAdmin}
                className="text-gray-700 hover:text-red-600"
              >
                Entrar
              </button>
              <button 
                onClick={onSwitchToRegister}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
              >
                Cadastrar
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section with Search */}
      <section className="bg-gradient-to-r from-red-500 to-pink-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Encontre sua hospedagem perfeita
            </h1>
            <p className="text-xl md:text-2xl opacity-90">
              Descubra pousadas únicas e acomodações especiais
            </p>
          </div>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Destino
                </label>
                <select
                  value={searchParams.destination}
                  onChange={(e) => setSearchParams({...searchParams, destination: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent text-gray-900"
                >
                  <option value="">Todas as pousadas</option>
                  {properties.map(property => (
                    <option key={property.id} value={property.id}>
                      {property.name} - {property.city}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Check-in
                </label>
                <input
                  type="date"
                  value={searchParams.checkin}
                  onChange={(e) => setSearchParams({...searchParams, checkin: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent text-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Check-out
                </label>
                <input
                  type="date"
                  value={searchParams.checkout}
                  onChange={(e) => setSearchParams({...searchParams, checkout: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent text-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Hóspedes
                </label>
                <select
                  value={searchParams.guests}
                  onChange={(e) => setSearchParams({...searchParams, guests: parseInt(e.target.value)})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent text-gray-900"
                >
                  {[1,2,3,4,5,6,7,8].map(num => (
                    <option key={num} value={num}>{num} {num === 1 ? 'hóspede' : 'hóspedes'}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex justify-between items-center mt-6">
              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
              >
                <Filter className="h-5 w-5" />
                <span>Filtros</span>
              </button>

              <button
                type="submit"
                className="bg-red-500 text-white px-8 py-3 rounded-lg hover:bg-red-600 flex items-center space-x-2"
              >
                <Search className="h-5 w-5" />
                <span>Buscar</span>
              </button>
            </div>

            {/* Filters */}
            {showFilters && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tipo de Acomodação
                    </label>
                    <select
                      value={filters.type}
                      onChange={(e) => setFilters({...filters, type: e.target.value})}
                      className="w-full p-2 border border-gray-300 rounded-lg text-gray-900"
                    >
                      <option value="">Todos os tipos</option>
                      {accommodationTypes.map(type => (
                        <option key={type} value={type}>{type}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Preço por noite (R$)
                    </label>
                    <div className="flex space-x-2">
                      <input
                        type="number"
                        placeholder="Mín"
                        value={filters.priceRange[0]}
                        onChange={(e) => setFilters({
                          ...filters, 
                          priceRange: [parseInt(e.target.value) || 0, filters.priceRange[1]]
                        })}
                        className="w-full p-2 border border-gray-300 rounded-lg text-gray-900"
                      />
                      <input
                        type="number"
                        placeholder="Máx"
                        value={filters.priceRange[1]}
                        onChange={(e) => setFilters({
                          ...filters, 
                          priceRange: [filters.priceRange[0], parseInt(e.target.value) || 1000]
                        })}
                        className="w-full p-2 border border-gray-300 rounded-lg text-gray-900"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </form>
        </div>
      </section>

      {/* Results */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900">
            {filteredAccommodations.length} acomodações encontradas
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredAccommodations.map(accommodation => (
            <div key={accommodation.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
              {/* Image */}
              <div className="relative h-48 bg-gradient-to-r from-gray-200 to-gray-300">
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-gray-500 text-lg">Foto da Acomodação</span>
                </div>
                <button
                  onClick={() => toggleFavorite(accommodation.id)}
                  className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:shadow-lg"
                >
                  <Heart 
                    className={`h-5 w-5 ${
                      favorites.includes(accommodation.id) 
                        ? 'text-red-500 fill-current' 
                        : 'text-gray-400'
                    }`} 
                  />
                </button>
              </div>

              {/* Content */}
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {accommodation.name}
                  </h3>
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-400 fill-current" />
                    <span className="text-sm text-gray-600">4.8</span>
                  </div>
                </div>

                <div className="flex items-center text-gray-600 mb-2">
                  <MapPin className="h-4 w-4 mr-1" />
                  <span className="text-sm">{getPropertyLocation(accommodation.property_id)}</span>
                </div>

                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {accommodation.description || 'Acomodação confortável e bem localizada.'}
                </p>

                <div className="flex items-center space-x-2 mb-3">
                  <Users className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    Até {accommodation.capacity} hóspedes
                  </span>
                </div>

                {/* Amenities */}
                <div className="flex items-center space-x-2 mb-4">
                  {['wifi', 'estacionamento', 'cafe'].map(amenity => {
                    const Icon = getAmenityIcon(amenity)
                    return (
                      <div key={amenity} className="p-1 bg-gray-100 rounded">
                        <Icon className="h-3 w-3 text-gray-600" />
                      </div>
                    )
                  })}
                </div>

                <div className="flex justify-between items-center">
                  <div>
                    <span className="text-lg font-bold text-gray-900">
                      R$ {accommodation.price_per_night}
                    </span>
                    <span className="text-gray-600 text-sm"> / noite</span>
                  </div>
                  <button 
                    onClick={() => handleReservation(accommodation)}
                    className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
                  >
                    Reservar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredAccommodations.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <Search className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma acomodação encontrada
            </h3>
            <p className="text-gray-600">
              Tente ajustar seus filtros de busca para encontrar mais opções.
            </p>
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">H</span>
                </div>
                <span className="text-xl font-bold">HostFlow</span>
              </div>
              <p className="text-gray-400">
                Conectando viajantes a experiências únicas em pousadas especiais.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Hospedagem</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Pousadas</a></li>
                <li><a href="#" className="hover:text-white">Chalés</a></li>
                <li><a href="#" className="hover:text-white">Suítes</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Suporte</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Central de Ajuda</a></li>
                <li><a href="#" className="hover:text-white">Contato</a></li>
                <li><a href="#" className="hover:text-white">Cancelamento</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Sobre</a></li>
                <li><a href="#" className="hover:text-white">Carreiras</a></li>
                <li><a href="#" className="hover:text-white">Imprensa</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 HostFlow. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default ClientBooking


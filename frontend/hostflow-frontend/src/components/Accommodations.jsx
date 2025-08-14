import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Bed, Users, DollarSign, Calendar, Eye } from 'lucide-react'

const Accommodations = () => {
  const [accommodations, setAccommodations] = useState([])
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingAccommodation, setEditingAccommodation] = useState(null)
  const [selectedProperty, setSelectedProperty] = useState('')
  const [formData, setFormData] = useState({
    property_id: '',
    name: '',
    type: 'quarto',
    description: '',
    max_guests: 2,
    bedrooms: 1,
    bathrooms: 1,
    beds: 1,
    area_sqm: '',
    floor: '',
    base_price: '',
    weekend_price: '',
    holiday_price: '',
    cleaning_fee: '',
    amenities: [],
    main_image: '',
    images: [],
    min_stay_nights: 1,
    max_stay_nights: ''
  })

  const accommodationTypes = [
    { value: 'quarto', label: 'Quarto' },
    { value: 'suite', label: 'Suíte' },
    { value: 'chale', label: 'Chalé' },
    { value: 'apartamento', label: 'Apartamento' },
    { value: 'casa', label: 'Casa' },
    { value: 'loft', label: 'Loft' }
  ]

  const amenitiesList = [
    'Ar condicionado', 'TV a cabo', 'Frigobar', 'Wi-Fi',
    'Varanda', 'Vista para o mar', 'Vista da montanha', 'Lareira',
    'Cozinha equipada', 'Hidromassagem', 'Sala de estar', 'Cofre',
    'Área externa privativa', 'Jardim privativo', 'Estacionamento'
  ]

  useEffect(() => {
    fetchAccommodations()
    fetchProperties()
  }, [])

  const fetchAccommodations = async () => {
    try {
      const response = await fetch('/api/accommodations')
      const data = await response.json()
      setAccommodations(data)
    } catch (error) {
      console.error('Erro ao carregar acomodações:', error)
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const url = editingAccommodation ? `/api/accommodations/${editingAccommodation.id}` : '/api/accommodations'
      const method = editingAccommodation ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          base_price: parseFloat(formData.base_price),
          weekend_price: formData.weekend_price ? parseFloat(formData.weekend_price) : null,
          holiday_price: formData.holiday_price ? parseFloat(formData.holiday_price) : null,
          cleaning_fee: formData.cleaning_fee ? parseFloat(formData.cleaning_fee) : 0,
          area_sqm: formData.area_sqm ? parseFloat(formData.area_sqm) : null,
          max_stay_nights: formData.max_stay_nights ? parseInt(formData.max_stay_nights) : null
        })
      })

      if (response.ok) {
        fetchAccommodations()
        resetForm()
      } else {
        const error = await response.json()
        alert(error.error || 'Erro ao salvar acomodação')
      }
    } catch (error) {
      console.error('Erro ao salvar acomodação:', error)
      alert('Erro ao salvar acomodação')
    }
  }

  const handleEdit = (accommodation) => {
    setEditingAccommodation(accommodation)
    setFormData({
      ...accommodation,
      amenities: accommodation.amenities ? JSON.parse(accommodation.amenities) : [],
      images: accommodation.images ? JSON.parse(accommodation.images) : [],
      base_price: accommodation.base_price.toString(),
      weekend_price: accommodation.weekend_price ? accommodation.weekend_price.toString() : '',
      holiday_price: accommodation.holiday_price ? accommodation.holiday_price.toString() : '',
      cleaning_fee: accommodation.cleaning_fee ? accommodation.cleaning_fee.toString() : '',
      area_sqm: accommodation.area_sqm ? accommodation.area_sqm.toString() : '',
      max_stay_nights: accommodation.max_stay_nights ? accommodation.max_stay_nights.toString() : ''
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Tem certeza que deseja excluir esta acomodação?')) {
      try {
        const response = await fetch(`/api/accommodations/${id}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          fetchAccommodations()
        }
      } catch (error) {
        console.error('Erro ao excluir acomodação:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      property_id: '',
      name: '',
      type: 'quarto',
      description: '',
      max_guests: 2,
      bedrooms: 1,
      bathrooms: 1,
      beds: 1,
      area_sqm: '',
      floor: '',
      base_price: '',
      weekend_price: '',
      holiday_price: '',
      cleaning_fee: '',
      amenities: [],
      main_image: '',
      images: [],
      min_stay_nights: 1,
      max_stay_nights: ''
    })
    setEditingAccommodation(null)
    setShowForm(false)
  }

  const handleAmenityToggle = (amenity) => {
    setFormData(prev => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter(a => a !== amenity)
        : [...prev.amenities, amenity]
    }))
  }

  const filteredAccommodations = selectedProperty 
    ? accommodations.filter(acc => acc.property_id.toString() === selectedProperty)
    : accommodations

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
          <h1 className="text-2xl font-bold text-gray-900">Acomodações</h1>
          <p className="text-gray-600">Gerencie quartos, suítes e chalés</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Nova Acomodação
        </button>
      </div>

      {/* Filtro por Pousada */}
      <div className="bg-white p-4 rounded-lg shadow-sm">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Filtrar por Pousada:</label>
          <select
            value={selectedProperty}
            onChange={(e) => setSelectedProperty(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
          >
            <option value="">Todas as Pousadas</option>
            {properties.map(property => (
              <option key={property.id} value={property.id}>
                {property.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {editingAccommodation ? 'Editar Acomodação' : 'Nova Acomodação'}
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
                    onChange={(e) => setFormData(prev => ({ ...prev, property_id: e.target.value }))}
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
                    Nome da Acomodação *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tipo *
                  </label>
                  <select
                    required
                    value={formData.type}
                    onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  >
                    {accommodationTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Máximo de Hóspedes *
                  </label>
                  <input
                    type="number"
                    required
                    min="1"
                    value={formData.max_guests}
                    onChange={(e) => setFormData(prev => ({ ...prev, max_guests: parseInt(e.target.value) }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrição
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  rows={3}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Quartos
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={formData.bedrooms}
                    onChange={(e) => setFormData(prev => ({ ...prev, bedrooms: parseInt(e.target.value) }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Banheiros
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={formData.bathrooms}
                    onChange={(e) => setFormData(prev => ({ ...prev, bathrooms: parseInt(e.target.value) }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Camas
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={formData.beds}
                    onChange={(e) => setFormData(prev => ({ ...prev, beds: parseInt(e.target.value) }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Área (m²)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.area_sqm}
                    onChange={(e) => setFormData(prev => ({ ...prev, area_sqm: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Andar
                  </label>
                  <input
                    type="text"
                    value={formData.floor}
                    onChange={(e) => setFormData(prev => ({ ...prev, floor: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Preço Base (R$) *
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={formData.base_price}
                    onChange={(e) => setFormData(prev => ({ ...prev, base_price: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Preço Final de Semana (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.weekend_price}
                    onChange={(e) => setFormData(prev => ({ ...prev, weekend_price: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Preço Feriado (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.holiday_price}
                    onChange={(e) => setFormData(prev => ({ ...prev, holiday_price: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Taxa de Limpeza (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.cleaning_fee}
                    onChange={(e) => setFormData(prev => ({ ...prev, cleaning_fee: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Estadia Mínima (noites)
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={formData.min_stay_nights}
                    onChange={(e) => setFormData(prev => ({ ...prev, min_stay_nights: parseInt(e.target.value) }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Estadia Máxima (noites)
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={formData.max_stay_nights}
                    onChange={(e) => setFormData(prev => ({ ...prev, max_stay_nights: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Comodidades
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                  {amenitiesList.map(amenity => (
                    <label key={amenity} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.amenities.includes(amenity)}
                        onChange={() => handleAmenityToggle(amenity)}
                        className="rounded border-gray-300 text-red-500 focus:ring-red-500"
                      />
                      <span className="text-sm">{amenity}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Imagem Principal (URL)
                </label>
                <input
                  type="url"
                  value={formData.main_image}
                  onChange={(e) => setFormData(prev => ({ ...prev, main_image: e.target.value }))}
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
                  {editingAccommodation ? 'Atualizar' : 'Criar'} Acomodação
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAccommodations.map(accommodation => (
          <div key={accommodation.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            {accommodation.main_image && (
              <img
                src={accommodation.main_image}
                alt={accommodation.name}
                className="w-full h-48 object-cover"
              />
            )}
            
            <div className="p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{accommodation.name}</h3>
                  <p className="text-sm text-gray-600">{accommodation.property_name}</p>
                </div>
                <div className="flex space-x-1">
                  <button
                    onClick={() => handleEdit(accommodation)}
                    className="p-1 text-gray-400 hover:text-blue-500"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(accommodation.id)}
                    className="p-1 text-gray-400 hover:text-red-500"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center justify-between">
                  <span className="capitalize">{accommodation.type}</span>
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    accommodation.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {accommodation.is_available ? 'Disponível' : 'Indisponível'}
                  </span>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1">
                    <Users className="h-4 w-4" />
                    <span>{accommodation.max_guests}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Bed className="h-4 w-4" />
                    <span>{accommodation.beds}</span>
                  </div>
                  {accommodation.area_sqm && (
                    <span>{accommodation.area_sqm}m²</span>
                  )}
                </div>
                
                <div className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4" />
                  <span className="font-medium">R$ {accommodation.base_price}/noite</span>
                </div>
                
                {accommodation.weekend_price && (
                  <div className="text-xs text-gray-500">
                    Final de semana: R$ {accommodation.weekend_price}
                  </div>
                )}
              </div>
              
              {accommodation.amenities && (
                <div className="mt-3">
                  <div className="flex flex-wrap gap-1">
                    {JSON.parse(accommodation.amenities).slice(0, 3).map(amenity => (
                      <span key={amenity} className="px-2 py-1 bg-gray-100 text-xs rounded-full">
                        {amenity}
                      </span>
                    ))}
                    {JSON.parse(accommodation.amenities).length > 3 && (
                      <span className="px-2 py-1 bg-gray-100 text-xs rounded-full">
                        +{JSON.parse(accommodation.amenities).length - 3}
                      </span>
                    )}
                  </div>
                </div>
              )}
              
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Estadia mín:</span>
                  <span className="font-medium">{accommodation.min_stay_nights} noite(s)</span>
                </div>
                {accommodation.floor && (
                  <div className="flex justify-between text-sm mt-1">
                    <span className="text-gray-600">Andar:</span>
                    <span className="font-medium">{accommodation.floor}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredAccommodations.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Bed className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {selectedProperty ? 'Nenhuma acomodação encontrada' : 'Nenhuma acomodação cadastrada'}
          </h3>
          <p className="text-gray-600 mb-4">
            {selectedProperty ? 'Esta pousada ainda não possui acomodações' : 'Comece criando sua primeira acomodação'}
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
          >
            Criar Acomodação
          </button>
        </div>
      )}
    </div>
  )
}

export default Accommodations


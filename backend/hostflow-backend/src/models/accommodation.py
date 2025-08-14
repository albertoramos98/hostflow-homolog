from datetime import datetime
from src.models.user import db

class Accommodation(db.Model):
    """Modelo para Acomodações (Quartos, Suítes, Chalés)"""
    __tablename__ = 'accommodations'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    
    # Informações básicas
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # quarto, suite, chale, etc.
    description = db.Column(db.Text)
    
    # Capacidade
    max_guests = db.Column(db.Integer, nullable=False, default=2)
    bedrooms = db.Column(db.Integer, default=1)
    bathrooms = db.Column(db.Integer, default=1)
    beds = db.Column(db.Integer, default=1)
    
    # Área e características
    area_sqm = db.Column(db.Float)  # Área em metros quadrados
    floor = db.Column(db.String(20))  # Andar
    
    # Preços
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    weekend_price = db.Column(db.Numeric(10, 2))
    holiday_price = db.Column(db.Numeric(10, 2))
    cleaning_fee = db.Column(db.Numeric(10, 2), default=0)
    
    # Comodidades específicas
    amenities = db.Column(db.Text)  # JSON string com lista de comodidades
    
    # Imagens
    main_image = db.Column(db.String(500))
    images = db.Column(db.Text)  # JSON string com lista de URLs
    
    # Disponibilidade
    is_available = db.Column(db.Boolean, default=True)
    min_stay_nights = db.Column(db.Integer, default=1)
    max_stay_nights = db.Column(db.Integer)
    
    # Status e datas
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    bookings = db.relationship('Booking', backref='accommodation', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'max_guests': self.max_guests,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'beds': self.beds,
            'area_sqm': float(self.area_sqm) if self.area_sqm else None,
            'floor': self.floor,
            'base_price': float(self.base_price) if self.base_price else 0,
            'weekend_price': float(self.weekend_price) if self.weekend_price else None,
            'holiday_price': float(self.holiday_price) if self.holiday_price else None,
            'cleaning_fee': float(self.cleaning_fee) if self.cleaning_fee else 0,
            'amenities': self.amenities,
            'main_image': self.main_image,
            'images': self.images,
            'is_available': self.is_available,
            'min_stay_nights': self.min_stay_nights,
            'max_stay_nights': self.max_stay_nights,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'property_name': self.property.name if self.property else None
        }
    
    def get_price_for_date(self, date):
        """Retorna o preço para uma data específica"""
        # Lógica simples: weekend = sábado/domingo
        if date.weekday() >= 5:  # 5=sábado, 6=domingo
            return float(self.weekend_price) if self.weekend_price else float(self.base_price)
        return float(self.base_price)
    
    def is_available_for_period(self, check_in, check_out):
        """Verifica se está disponível para um período"""
        if not self.is_available or not self.is_active:
            return False
        
        # Verificar se há reservas conflitantes
        from .booking import Booking
        conflicting_bookings = Booking.query.filter(
            Booking.accommodation_id == self.id,
            Booking.status.in_(['confirmed', 'checked_in']),
            db.or_(
                db.and_(Booking.check_in_date <= check_in, Booking.check_out_date > check_in),
                db.and_(Booking.check_in_date < check_out, Booking.check_out_date >= check_out),
                db.and_(Booking.check_in_date >= check_in, Booking.check_out_date <= check_out)
            )
        ).first()
        
        return conflicting_bookings is None
    
    def __repr__(self):
        return f'<Accommodation {self.name}>'


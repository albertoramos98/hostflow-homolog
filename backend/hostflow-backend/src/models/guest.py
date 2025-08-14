from datetime import datetime, date
from src.models.user import db

class Guest(db.Model):
    """Modelo para Hóspedes"""
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Informações pessoais
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    
    # Documentos
    document_type = db.Column(db.String(20))  # CPF, RG, Passaporte
    document_number = db.Column(db.String(50))
    
    # Endereço
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50), default='Brasil')
    zip_code = db.Column(db.String(20))
    
    # Informações adicionais
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    
    # Preferências
    preferences = db.Column(db.Text)  # JSON string com preferências
    special_requests = db.Column(db.Text)
    
    # Marketing
    newsletter_consent = db.Column(db.Boolean, default=False)
    marketing_consent = db.Column(db.Boolean, default=False)
    
    # Status e estatísticas
    is_active = db.Column(db.Boolean, default=True)
    total_bookings = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Numeric(10, 2), default=0)
    last_stay_date = db.Column(db.Date)
    
    # Avaliação do hóspede
    rating = db.Column(db.Float, default=5.0)  # Avaliação média do hóspede
    notes = db.Column(db.Text)  # Notas internas sobre o hóspede
    
    # Datas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    bookings = db.relationship('Booking', backref='guest', lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.birth_date:
            today = datetime.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zip_code': self.zip_code,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'age': self.age,
            'gender': self.gender,
            'nationality': self.nationality,
            'occupation': self.occupation,
            'preferences': self.preferences,
            'special_requests': self.special_requests,
            'newsletter_consent': self.newsletter_consent,
            'marketing_consent': self.marketing_consent,
            'is_active': self.is_active,
            'total_bookings': self.total_bookings,
            'total_spent': float(self.total_spent) if self.total_spent else 0,
            'last_stay_date': self.last_stay_date.isoformat() if self.last_stay_date else None,
            'rating': self.rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_stats(self):
        """Atualiza estatísticas do hóspede"""
        from .booking import Booking
        
        # Contar reservas confirmadas
        confirmed_bookings = Booking.query.filter_by(
            guest_id=self.id,
            status='confirmed'
        ).all()
        
        self.total_bookings = len(confirmed_bookings)
        self.total_spent = sum(booking.total_amount for booking in confirmed_bookings if booking.total_amount)
        
        # Última estadia
        if confirmed_bookings:
            latest_booking = max(confirmed_bookings, key=lambda b: b.check_out_date)
            self.last_stay_date = latest_booking.check_out_date
    
    def __repr__(self):
        return f'<Guest {self.full_name}>'


from datetime import datetime, date
from src.models.user import db

class Booking(db.Model):
    """Modelo para Reservas"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamentos
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodations.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Datas da reserva
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    
    # Hóspedes
    adults = db.Column(db.Integer, nullable=False, default=1)
    children = db.Column(db.Integer, default=0)
    total_guests = db.Column(db.Integer, nullable=False)
    
    # Valores
    base_amount = db.Column(db.Numeric(10, 2), nullable=False)
    cleaning_fee = db.Column(db.Numeric(10, 2), default=0)
    service_fee = db.Column(db.Numeric(10, 2), default=0)
    taxes = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status da reserva
    status = db.Column(db.String(20), nullable=False, default='pending')
    # pending, confirmed, cancelled, checked_in, checked_out, no_show
    
    # Pagamento
    payment_status = db.Column(db.String(20), default='pending')
    # pending, paid, partial, refunded, failed
    payment_method = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime)
    
    # Check-in/Check-out
    actual_check_in = db.Column(db.DateTime)
    actual_check_out = db.Column(db.DateTime)
    
    # Informações adicionais
    special_requests = db.Column(db.Text)
    internal_notes = db.Column(db.Text)
    cancellation_reason = db.Column(db.Text)
    cancelled_at = db.Column(db.DateTime)
    
    # Origem da reserva
    source = db.Column(db.String(50), default='direct')  # direct, booking.com, airbnb, etc.
    
    # Avaliação
    guest_rating = db.Column(db.Integer)  # 1-5
    guest_review = db.Column(db.Text)
    host_rating = db.Column(db.Integer)  # 1-5
    host_review = db.Column(db.Text)
    
    # Datas do sistema
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.booking_code:
            self.booking_code = self.generate_booking_code()
        if self.check_in_date and self.check_out_date:
            self.nights = (self.check_out_date - self.check_in_date).days
        if self.adults and self.children is not None:
            self.total_guests = self.adults + self.children
    
    def generate_booking_code(self):
        """Gera código único para a reserva"""
        return f"HF{datetime.now().strftime('%Y%m')}{str(uuid.uuid4())[:6].upper()}"
    
    @property
    def is_past(self):
        """Verifica se a reserva é do passado"""
        return self.check_out_date < date.today()
    
    @property
    def is_current(self):
        """Verifica se a reserva está em andamento"""
        today = date.today()
        return self.check_in_date <= today <= self.check_out_date
    
    @property
    def is_future(self):
        """Verifica se a reserva é futura"""
        return self.check_in_date > date.today()
    
    @property
    def can_cancel(self):
        """Verifica se a reserva pode ser cancelada"""
        return self.status in ['pending', 'confirmed'] and self.is_future
    
    @property
    def can_check_in(self):
        """Verifica se pode fazer check-in"""
        return self.status == 'confirmed' and self.check_in_date <= date.today()
    
    @property
    def can_check_out(self):
        """Verifica se pode fazer check-out"""
        return self.status == 'checked_in'
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_code': self.booking_code,
            'property_id': self.property_id,
            'accommodation_id': self.accommodation_id,
            'guest_id': self.guest_id,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'nights': self.nights,
            'adults': self.adults,
            'children': self.children,
            'total_guests': self.total_guests,
            'base_amount': float(self.base_amount) if self.base_amount else 0,
            'cleaning_fee': float(self.cleaning_fee) if self.cleaning_fee else 0,
            'service_fee': float(self.service_fee) if self.service_fee else 0,
            'taxes': float(self.taxes) if self.taxes else 0,
            'discount': float(self.discount) if self.discount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'actual_check_in': self.actual_check_in.isoformat() if self.actual_check_in else None,
            'actual_check_out': self.actual_check_out.isoformat() if self.actual_check_out else None,
            'special_requests': self.special_requests,
            'internal_notes': self.internal_notes,
            'cancellation_reason': self.cancellation_reason,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'source': self.source,
            'guest_rating': self.guest_rating,
            'guest_review': self.guest_review,
            'host_rating': self.host_rating,
            'host_review': self.host_review,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Propriedades calculadas
            'is_past': self.is_past,
            'is_current': self.is_current,
            'is_future': self.is_future,
            'can_cancel': self.can_cancel,
            'can_check_in': self.can_check_in,
            'can_check_out': self.can_check_out,
            # Relacionamentos
            'property_name': self.property.name if self.property else None,
            'accommodation_name': self.accommodation.name if self.accommodation else None,
            'guest_name': self.guest.full_name if self.guest else None,
            'guest_email': self.guest.email if self.guest else None
        }
    
    def calculate_total(self):
        """Calcula o valor total da reserva"""
        total = float(self.base_amount or 0)
        total += float(self.cleaning_fee or 0)
        total += float(self.service_fee or 0)
        total += float(self.taxes or 0)
        total -= float(self.discount or 0)
        self.total_amount = total
        return total
    
    def cancel(self, reason=None):
        """Cancela a reserva"""
        if self.can_cancel:
            self.status = 'cancelled'
            self.cancellation_reason = reason
            self.cancelled_at = datetime.utcnow()
            return True
        return False
    
    def check_in(self):
        """Realiza check-in"""
        if self.can_check_in:
            self.status = 'checked_in'
            self.actual_check_in = datetime.utcnow()
            return True
        return False
    
    def check_out(self):
        """Realiza check-out"""
        if self.can_check_out:
            self.status = 'checked_out'
            self.actual_check_out = datetime.utcnow()
            return True
        return False
    
    def __repr__(self):
        return f'<Booking {self.booking_code}>'


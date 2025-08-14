from datetime import datetime
from src.models.user import db

class Property(db.Model):
    """Modelo para Pousadas"""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    
    # Informações de negócio
    check_in_time = db.Column(db.String(10), default='14:00')
    check_out_time = db.Column(db.String(10), default='12:00')
    cancellation_policy = db.Column(db.Text)
    house_rules = db.Column(db.Text)
    
    # Comodidades
    amenities = db.Column(db.Text)  # JSON string com lista de comodidades
    
    # Imagens
    main_image = db.Column(db.String(500))
    images = db.Column(db.Text)  # JSON string com lista de URLs
    
    # Status e datas
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'cancellation_policy': self.cancellation_policy,
            'house_rules': self.house_rules,
            'amenities': self.amenities,
            'main_image': self.main_image,
            'images': self.images,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'accommodations_count': 0  # Will be calculated in routes
        }
    
    def __repr__(self):
        return f'<Property {self.name}>'


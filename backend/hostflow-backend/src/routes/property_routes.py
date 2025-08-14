from flask import Blueprint, request, jsonify
from src.models.property import Property, db
import json

property_bp = Blueprint('properties', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    """Lista todas as pousadas"""
    try:
        properties = Property.query.filter_by(is_active=True).all()
        return jsonify([prop.to_dict() for prop in properties]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Obtém uma pousada específica"""
    try:
        property = Property.query.get_or_404(property_id)
        return jsonify(property.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties', methods=['POST'])
def create_property():
    """Cria uma nova pousada"""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['name', 'address', 'city', 'state']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Converter listas para JSON strings
        if 'amenities' in data and isinstance(data['amenities'], list):
            data['amenities'] = json.dumps(data['amenities'])
        if 'images' in data and isinstance(data['images'], list):
            data['images'] = json.dumps(data['images'])
        
        property = Property(**data)
        db.session.add(property)
        db.session.commit()
        
        return jsonify(property.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    """Atualiza uma pousada"""
    try:
        property = Property.query.get_or_404(property_id)
        data = request.get_json()
        
        # Converter listas para JSON strings
        if 'amenities' in data and isinstance(data['amenities'], list):
            data['amenities'] = json.dumps(data['amenities'])
        if 'images' in data and isinstance(data['images'], list):
            data['images'] = json.dumps(data['images'])
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(property, key):
                setattr(property, key, value)
        
        db.session.commit()
        return jsonify(property.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    """Desativa uma pousada (soft delete)"""
    try:
        property = Property.query.get_or_404(property_id)
        property.is_active = False
        db.session.commit()
        return jsonify({'message': 'Pousada desativada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties/<int:property_id>/accommodations', methods=['GET'])
def get_property_accommodations(property_id):
    """Lista acomodações de uma pousada"""
    try:
        property = Property.query.get_or_404(property_id)
        accommodations = [acc.to_dict() for acc in property.accommodations if acc.is_active]
        return jsonify(accommodations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@property_bp.route('/properties/<int:property_id>/stats', methods=['GET'])
def get_property_stats(property_id):
    """Obtém estatísticas de uma pousada"""
    try:
        from src.models.booking import Booking
        from src.models.accommodation import Accommodation
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        property = Property.query.get_or_404(property_id)
        
        # Estatísticas básicas
        total_accommodations = Accommodation.query.filter_by(
            property_id=property_id, 
            is_active=True
        ).count()
        
        # Reservas do último mês
        last_month = datetime.now() - timedelta(days=30)
        recent_bookings = Booking.query.join(Accommodation).filter(
            Accommodation.property_id == property_id,
            Booking.created_at >= last_month
        ).count()
        
        # Receita do último mês
        revenue_query = db.session.query(func.sum(Booking.total_amount)).join(Accommodation).filter(
            Accommodation.property_id == property_id,
            Booking.status.in_(['confirmed', 'checked_out']),
            Booking.created_at >= last_month
        ).scalar()
        
        monthly_revenue = float(revenue_query) if revenue_query else 0
        
        # Taxa de ocupação (simplificada)
        total_nights_available = total_accommodations * 30  # Aproximação
        nights_booked = db.session.query(func.sum(Booking.nights)).join(Accommodation).filter(
            Accommodation.property_id == property_id,
            Booking.status.in_(['confirmed', 'checked_in', 'checked_out']),
            Booking.check_in_date >= last_month.date()
        ).scalar()
        
        occupancy_rate = (nights_booked / total_nights_available * 100) if total_nights_available > 0 and nights_booked else 0
        
        stats = {
            'total_accommodations': total_accommodations,
            'recent_bookings': recent_bookings,
            'monthly_revenue': monthly_revenue,
            'occupancy_rate': round(occupancy_rate, 1),
            'property_name': property.name
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


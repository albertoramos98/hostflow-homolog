from flask import Blueprint, request, jsonify
from src.models.accommodation import Accommodation, db
from src.models.property import Property
from datetime import datetime, date
import json

accommodation_bp = Blueprint('accommodations', __name__)

@accommodation_bp.route('/accommodations', methods=['GET'])
def get_accommodations():
    """Lista todas as acomodações"""
    try:
        property_id = request.args.get('property_id')
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        
        query = Accommodation.query.filter_by(is_active=True)
        
        if property_id:
            query = query.filter_by(property_id=property_id)
        
        if available_only:
            query = query.filter_by(is_available=True)
        
        accommodations = query.all()
        return jsonify([acc.to_dict() for acc in accommodations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/<int:accommodation_id>', methods=['GET'])
def get_accommodation(accommodation_id):
    """Obtém uma acomodação específica"""
    try:
        accommodation = Accommodation.query.get_or_404(accommodation_id)
        return jsonify(accommodation.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations', methods=['POST'])
def create_accommodation():
    """Cria uma nova acomodação"""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['property_id', 'name', 'type', 'max_guests', 'base_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se a pousada existe
        property = Property.query.get(data['property_id'])
        if not property:
            return jsonify({'error': 'Pousada não encontrada'}), 404
        
        # Converter listas para JSON strings
        if 'amenities' in data and isinstance(data['amenities'], list):
            data['amenities'] = json.dumps(data['amenities'])
        if 'images' in data and isinstance(data['images'], list):
            data['images'] = json.dumps(data['images'])
        
        accommodation = Accommodation(**data)
        db.session.add(accommodation)
        db.session.commit()
        
        return jsonify(accommodation.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/<int:accommodation_id>', methods=['PUT'])
def update_accommodation(accommodation_id):
    """Atualiza uma acomodação"""
    try:
        accommodation = Accommodation.query.get_or_404(accommodation_id)
        data = request.get_json()
        
        # Converter listas para JSON strings
        if 'amenities' in data and isinstance(data['amenities'], list):
            data['amenities'] = json.dumps(data['amenities'])
        if 'images' in data and isinstance(data['images'], list):
            data['images'] = json.dumps(data['images'])
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(accommodation, key):
                setattr(accommodation, key, value)
        
        db.session.commit()
        return jsonify(accommodation.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/<int:accommodation_id>', methods=['DELETE'])
def delete_accommodation(accommodation_id):
    """Desativa uma acomodação (soft delete)"""
    try:
        accommodation = Accommodation.query.get_or_404(accommodation_id)
        accommodation.is_active = False
        db.session.commit()
        return jsonify({'message': 'Acomodação desativada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/<int:accommodation_id>/availability', methods=['GET'])
def check_availability(accommodation_id):
    """Verifica disponibilidade de uma acomodação"""
    try:
        accommodation = Accommodation.query.get_or_404(accommodation_id)
        
        check_in = request.args.get('check_in')
        check_out = request.args.get('check_out')
        
        if not check_in or not check_out:
            return jsonify({'error': 'Datas de check-in e check-out são obrigatórias'}), 400
        
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        if check_in_date >= check_out_date:
            return jsonify({'error': 'Data de check-out deve ser posterior ao check-in'}), 400
        
        is_available = accommodation.is_available_for_period(check_in_date, check_out_date)
        
        # Calcular preço total
        total_price = 0
        current_date = check_in_date
        while current_date < check_out_date:
            total_price += accommodation.get_price_for_date(current_date)
            current_date = current_date.replace(day=current_date.day + 1)
        
        nights = (check_out_date - check_in_date).days
        
        result = {
            'available': is_available,
            'accommodation_id': accommodation_id,
            'check_in': check_in,
            'check_out': check_out,
            'nights': nights,
            'base_price_per_night': float(accommodation.base_price),
            'total_base_price': total_price,
            'cleaning_fee': float(accommodation.cleaning_fee),
            'total_amount': total_price + float(accommodation.cleaning_fee)
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/search', methods=['GET'])
def search_accommodations():
    """Busca acomodações disponíveis"""
    try:
        # Parâmetros de busca
        check_in = request.args.get('check_in')
        check_out = request.args.get('check_out')
        guests = request.args.get('guests', 1, type=int)
        property_id = request.args.get('property_id')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        accommodation_type = request.args.get('type')
        
        query = Accommodation.query.filter_by(is_active=True, is_available=True)
        
        # Filtrar por pousada
        if property_id:
            query = query.filter_by(property_id=property_id)
        
        # Filtrar por capacidade
        query = query.filter(Accommodation.max_guests >= guests)
        
        # Filtrar por preço
        if min_price:
            query = query.filter(Accommodation.base_price >= min_price)
        if max_price:
            query = query.filter(Accommodation.base_price <= max_price)
        
        # Filtrar por tipo
        if accommodation_type:
            query = query.filter(Accommodation.type == accommodation_type)
        
        accommodations = query.all()
        
        # Se datas foram fornecidas, verificar disponibilidade
        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                available_accommodations = []
                for acc in accommodations:
                    if acc.is_available_for_period(check_in_date, check_out_date):
                        acc_dict = acc.to_dict()
                        
                        # Calcular preço para o período
                        total_price = 0
                        current_date = check_in_date
                        while current_date < check_out_date:
                            total_price += acc.get_price_for_date(current_date)
                            current_date = current_date.replace(day=current_date.day + 1)
                        
                        acc_dict['search_total_price'] = total_price + float(acc.cleaning_fee)
                        acc_dict['search_nights'] = (check_out_date - check_in_date).days
                        available_accommodations.append(acc_dict)
                
                return jsonify(available_accommodations), 200
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        return jsonify([acc.to_dict() for acc in accommodations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accommodation_bp.route('/accommodations/<int:accommodation_id>/calendar', methods=['GET'])
def get_accommodation_calendar(accommodation_id):
    """Obtém calendário de disponibilidade de uma acomodação"""
    try:
        from src.models.booking import Booking
        from datetime import timedelta
        
        accommodation = Accommodation.query.get_or_404(accommodation_id)
        
        # Período (padrão: próximos 3 meses)
        start_date = date.today()
        end_date = start_date + timedelta(days=90)
        
        # Buscar reservas no período
        bookings = Booking.query.filter(
            Booking.accommodation_id == accommodation_id,
            Booking.status.in_(['confirmed', 'checked_in']),
            Booking.check_out_date > start_date,
            Booking.check_in_date < end_date
        ).all()
        
        # Gerar calendário
        calendar = []
        current_date = start_date
        
        while current_date <= end_date:
            # Verificar se há reserva nesta data
            is_booked = any(
                booking.check_in_date <= current_date < booking.check_out_date
                for booking in bookings
            )
            
            calendar.append({
                'date': current_date.isoformat(),
                'available': not is_booked and accommodation.is_available,
                'price': accommodation.get_price_for_date(current_date),
                'is_weekend': current_date.weekday() >= 5
            })
            
            current_date += timedelta(days=1)
        
        return jsonify({
            'accommodation_id': accommodation_id,
            'accommodation_name': accommodation.name,
            'calendar': calendar
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


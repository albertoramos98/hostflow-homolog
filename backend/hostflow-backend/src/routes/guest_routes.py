from flask import Blueprint, request, jsonify
from src.models.guest import Guest, db
from datetime import datetime
import json

guest_bp = Blueprint('guests', __name__)

@guest_bp.route('/guests', methods=['GET'])
def get_guests():
    """Lista todos os hóspedes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        query = Guest.query.filter_by(is_active=True)
        
        # Busca por nome ou email
        if search:
            query = query.filter(
                db.or_(
                    Guest.first_name.ilike(f'%{search}%'),
                    Guest.last_name.ilike(f'%{search}%'),
                    Guest.email.ilike(f'%{search}%')
                )
            )
        
        # Ordenar por último update
        query = query.order_by(Guest.updated_at.desc())
        
        # Paginação
        guests = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'guests': [guest.to_dict() for guest in guests.items],
            'total': guests.total,
            'pages': guests.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>', methods=['GET'])
def get_guest(guest_id):
    """Obtém um hóspede específico"""
    try:
        guest = Guest.query.get_or_404(guest_id)
        guest_data = guest.to_dict()
        
        # Incluir histórico de reservas
        from src.models.booking import Booking
        bookings = Booking.query.filter_by(guest_id=guest_id).order_by(Booking.created_at.desc()).all()
        guest_data['bookings'] = [booking.to_dict() for booking in bookings]
        
        return jsonify(guest_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests', methods=['POST'])
def create_guest():
    """Cria um novo hóspede"""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se email já existe
        existing_guest = Guest.query.filter_by(email=data['email']).first()
        if existing_guest:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Converter data de nascimento
        if 'birth_date' in data and data['birth_date']:
            try:
                data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data de nascimento inválido. Use YYYY-MM-DD'}), 400
        
        # Converter preferências para JSON
        if 'preferences' in data and isinstance(data['preferences'], (dict, list)):
            data['preferences'] = json.dumps(data['preferences'])
        
        guest = Guest(**data)
        db.session.add(guest)
        db.session.commit()
        
        return jsonify(guest.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>', methods=['PUT'])
def update_guest(guest_id):
    """Atualiza um hóspede"""
    try:
        guest = Guest.query.get_or_404(guest_id)
        data = request.get_json()
        
        # Verificar se email já existe (exceto o próprio hóspede)
        if 'email' in data:
            existing_guest = Guest.query.filter(
                Guest.email == data['email'],
                Guest.id != guest_id
            ).first()
            if existing_guest:
                return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Converter data de nascimento
        if 'birth_date' in data and data['birth_date']:
            try:
                data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data de nascimento inválido. Use YYYY-MM-DD'}), 400
        
        # Converter preferências para JSON
        if 'preferences' in data and isinstance(data['preferences'], (dict, list)):
            data['preferences'] = json.dumps(data['preferences'])
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(guest, key):
                setattr(guest, key, value)
        
        db.session.commit()
        return jsonify(guest.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    """Desativa um hóspede (soft delete)"""
    try:
        guest = Guest.query.get_or_404(guest_id)
        guest.is_active = False
        db.session.commit()
        return jsonify({'message': 'Hóspede desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>/stats', methods=['GET'])
def get_guest_stats(guest_id):
    """Obtém estatísticas de um hóspede"""
    try:
        from src.models.booking import Booking
        from sqlalchemy import func
        
        guest = Guest.query.get_or_404(guest_id)
        
        # Atualizar estatísticas
        guest.update_stats()
        db.session.commit()
        
        # Estatísticas detalhadas
        bookings = Booking.query.filter_by(guest_id=guest_id).all()
        
        confirmed_bookings = [b for b in bookings if b.status == 'confirmed']
        completed_bookings = [b for b in bookings if b.status == 'checked_out']
        cancelled_bookings = [b for b in bookings if b.status == 'cancelled']
        
        # Valor médio por reserva
        avg_booking_value = 0
        if confirmed_bookings:
            total_value = sum(float(b.total_amount) for b in confirmed_bookings if b.total_amount)
            avg_booking_value = total_value / len(confirmed_bookings)
        
        # Noites totais
        total_nights = sum(b.nights for b in confirmed_bookings if b.nights)
        
        # Última reserva
        last_booking = None
        if bookings:
            last_booking = max(bookings, key=lambda b: b.created_at).to_dict()
        
        stats = {
            'guest_id': guest_id,
            'guest_name': guest.full_name,
            'total_bookings': len(bookings),
            'confirmed_bookings': len(confirmed_bookings),
            'completed_bookings': len(completed_bookings),
            'cancelled_bookings': len(cancelled_bookings),
            'total_spent': float(guest.total_spent),
            'avg_booking_value': round(avg_booking_value, 2),
            'total_nights': total_nights,
            'last_stay_date': guest.last_stay_date.isoformat() if guest.last_stay_date else None,
            'last_booking': last_booking,
            'rating': guest.rating,
            'member_since': guest.created_at.isoformat() if guest.created_at else None
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>/bookings', methods=['GET'])
def get_guest_bookings(guest_id):
    """Lista reservas de um hóspede"""
    try:
        from src.models.booking import Booking
        
        guest = Guest.query.get_or_404(guest_id)
        
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Booking.query.filter_by(guest_id=guest_id)
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Booking.created_at.desc())
        
        bookings = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'guest_id': guest_id,
            'guest_name': guest.full_name,
            'bookings': [booking.to_dict() for booking in bookings.items],
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/search', methods=['GET'])
def search_guests():
    """Busca hóspedes por diferentes critérios"""
    try:
        email = request.args.get('email')
        phone = request.args.get('phone')
        document = request.args.get('document')
        name = request.args.get('name')
        
        query = Guest.query.filter_by(is_active=True)
        
        if email:
            query = query.filter(Guest.email.ilike(f'%{email}%'))
        
        if phone:
            query = query.filter(Guest.phone.ilike(f'%{phone}%'))
        
        if document:
            query = query.filter(Guest.document_number.ilike(f'%{document}%'))
        
        if name:
            query = query.filter(
                db.or_(
                    Guest.first_name.ilike(f'%{name}%'),
                    Guest.last_name.ilike(f'%{name}%')
                )
            )
        
        guests = query.limit(20).all()
        return jsonify([guest.to_dict() for guest in guests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@guest_bp.route('/guests/<int:guest_id>/update-stats', methods=['POST'])
def update_guest_stats(guest_id):
    """Atualiza estatísticas de um hóspede"""
    try:
        guest = Guest.query.get_or_404(guest_id)
        guest.update_stats()
        db.session.commit()
        return jsonify(guest.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


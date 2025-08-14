from flask import Blueprint, request, jsonify
from src.models.booking import Booking, db
from src.models.accommodation import Accommodation
from src.models.guest import Guest
from src.models.property import Property
from datetime import datetime, date
import json

booking_bp = Blueprint('bookings', __name__)

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    """Lista todas as reservas"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        property_id = request.args.get('property_id')
        guest_id = request.args.get('guest_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        query = Booking.query
        
        # Filtros
        if status:
            query = query.filter_by(status=status)
        
        if guest_id:
            query = query.filter_by(guest_id=guest_id)
        
        if property_id:
            query = query.join(Accommodation).filter(Accommodation.property_id == property_id)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Booking.check_in_date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data_from inválido. Use YYYY-MM-DD'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Booking.check_out_date <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Formato de date_to inválido. Use YYYY-MM-DD'}), 400
        
        # Ordenar por data de criação (mais recentes primeiro)
        query = query.order_by(Booking.created_at.desc())
        
        # Paginação
        bookings = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings.items],
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Obtém uma reserva específica"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        return jsonify(booking.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    """Cria uma nova reserva"""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['accommodation_id', 'guest_id', 'check_in_date', 'check_out_date', 'adults']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se acomodação existe
        accommodation = Accommodation.query.get(data['accommodation_id'])
        if not accommodation:
            return jsonify({'error': 'Acomodação não encontrada'}), 404
        
        # Verificar se hóspede existe
        guest = Guest.query.get(data['guest_id'])
        if not guest:
            return jsonify({'error': 'Hóspede não encontrado'}), 404
        
        # Converter datas
        try:
            check_in_date = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Validações de negócio
        if check_in_date >= check_out_date:
            return jsonify({'error': 'Data de check-out deve ser posterior ao check-in'}), 400
        
        if check_in_date < date.today():
            return jsonify({'error': 'Data de check-in não pode ser no passado'}), 400
        
        # Verificar disponibilidade
        if not accommodation.is_available_for_period(check_in_date, check_out_date):
            return jsonify({'error': 'Acomodação não disponível para o período solicitado'}), 400
        
        # Verificar capacidade
        total_guests = data['adults'] + data.get('children', 0)
        if total_guests > accommodation.max_guests:
            return jsonify({'error': f'Número de hóspedes excede a capacidade máxima ({accommodation.max_guests})'}), 400
        
        # Calcular valores
        nights = (check_out_date - check_in_date).days
        base_amount = 0
        current_date = check_in_date
        
        while current_date < check_out_date:
            base_amount += accommodation.get_price_for_date(current_date)
            current_date = current_date.replace(day=current_date.day + 1)
        
        # Preparar dados da reserva
        booking_data = {
            'property_id': accommodation.property_id,
            'accommodation_id': data['accommodation_id'],
            'guest_id': data['guest_id'],
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'nights': nights,
            'adults': data['adults'],
            'children': data.get('children', 0),
            'total_guests': total_guests,
            'base_amount': base_amount,
            'cleaning_fee': accommodation.cleaning_fee or 0,
            'service_fee': data.get('service_fee', 0),
            'taxes': data.get('taxes', 0),
            'discount': data.get('discount', 0),
            'special_requests': data.get('special_requests'),
            'source': data.get('source', 'direct'),
            'status': data.get('status', 'pending')
        }
        
        booking = Booking(**booking_data)
        booking.calculate_total()
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify(booking.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """Atualiza uma reserva"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = [
            'special_requests', 'internal_notes', 'payment_status', 
            'payment_method', 'service_fee', 'taxes', 'discount'
        ]
        
        # Atualizar campos permitidos
        for key, value in data.items():
            if key in updatable_fields and hasattr(booking, key):
                setattr(booking, key, value)
        
        # Recalcular total se valores foram alterados
        if any(field in data for field in ['service_fee', 'taxes', 'discount']):
            booking.calculate_total()
        
        db.session.commit()
        return jsonify(booking.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancela uma reserva"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        data = request.get_json() or {}
        
        reason = data.get('reason', 'Cancelamento solicitado')
        
        if booking.cancel(reason):
            db.session.commit()
            return jsonify({
                'message': 'Reserva cancelada com sucesso',
                'booking': booking.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Não é possível cancelar esta reserva'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    """Confirma uma reserva"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        
        if booking.status == 'pending':
            booking.status = 'confirmed'
            db.session.commit()
            return jsonify({
                'message': 'Reserva confirmada com sucesso',
                'booking': booking.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Apenas reservas pendentes podem ser confirmadas'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>/check-in', methods=['POST'])
def check_in_booking(booking_id):
    """Realiza check-in de uma reserva"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        
        if booking.check_in():
            db.session.commit()
            return jsonify({
                'message': 'Check-in realizado com sucesso',
                'booking': booking.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Não é possível fazer check-in desta reserva'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>/check-out', methods=['POST'])
def check_out_booking(booking_id):
    """Realiza check-out de uma reserva"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        
        if booking.check_out():
            # Atualizar estatísticas do hóspede
            booking.guest.update_stats()
            
            db.session.commit()
            return jsonify({
                'message': 'Check-out realizado com sucesso',
                'booking': booking.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Não é possível fazer check-out desta reserva'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/<int:booking_id>/payment', methods=['POST'])
def update_payment(booking_id):
    """Atualiza informações de pagamento"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        data = request.get_json()
        
        if 'payment_status' in data:
            booking.payment_status = data['payment_status']
        
        if 'payment_method' in data:
            booking.payment_method = data['payment_method']
        
        if data.get('payment_status') == 'paid':
            booking.payment_date = datetime.utcnow()
        
        db.session.commit()
        return jsonify(booking.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/calendar', methods=['GET'])
def get_bookings_calendar():
    """Obtém calendário de reservas"""
    try:
        property_id = request.args.get('property_id')
        accommodation_id = request.args.get('accommodation_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Booking.query.filter(Booking.status.in_(['confirmed', 'checked_in']))
        
        if property_id:
            query = query.join(Accommodation).filter(Accommodation.property_id == property_id)
        
        if accommodation_id:
            query = query.filter_by(accommodation_id=accommodation_id)
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Booking.check_out_date >= start_date_obj)
            except ValueError:
                return jsonify({'error': 'Formato de start_date inválido. Use YYYY-MM-DD'}), 400
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Booking.check_in_date <= end_date_obj)
            except ValueError:
                return jsonify({'error': 'Formato de end_date inválido. Use YYYY-MM-DD'}), 400
        
        bookings = query.all()
        
        calendar_events = []
        for booking in bookings:
            calendar_events.append({
                'id': booking.id,
                'title': f"{booking.guest.full_name} - {booking.accommodation.name}",
                'start': booking.check_in_date.isoformat(),
                'end': booking.check_out_date.isoformat(),
                'booking_code': booking.booking_code,
                'status': booking.status,
                'guests': booking.total_guests,
                'total_amount': float(booking.total_amount),
                'accommodation_name': booking.accommodation.name,
                'guest_name': booking.guest.full_name,
                'guest_email': booking.guest.email
            })
        
        return jsonify(calendar_events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/stats', methods=['GET'])
def get_booking_stats():
    """Obtém estatísticas de reservas"""
    try:
        from sqlalchemy import func
        from datetime import timedelta
        
        property_id = request.args.get('property_id')
        
        # Período (padrão: último mês)
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        query = Booking.query
        
        if property_id:
            query = query.join(Accommodation).filter(Accommodation.property_id == property_id)
        
        # Estatísticas gerais
        total_bookings = query.count()
        
        # Reservas por status
        status_stats = db.session.query(
            Booking.status,
            func.count(Booking.id)
        ).group_by(Booking.status)
        
        if property_id:
            status_stats = status_stats.join(Accommodation).filter(Accommodation.property_id == property_id)
        
        status_counts = dict(status_stats.all())
        
        # Receita do período
        revenue_query = query.filter(
            Booking.status.in_(['confirmed', 'checked_out']),
            Booking.check_in_date >= start_date,
            Booking.check_in_date <= end_date
        )
        
        total_revenue = db.session.query(func.sum(Booking.total_amount)).filter(
            Booking.id.in_([b.id for b in revenue_query.all()])
        ).scalar() or 0
        
        # Reservas recentes
        recent_bookings = query.filter(
            Booking.created_at >= start_date
        ).count()
        
        # Check-ins hoje
        today_checkins = query.filter(
            Booking.check_in_date == date.today(),
            Booking.status.in_(['confirmed', 'checked_in'])
        ).count()
        
        # Check-outs hoje
        today_checkouts = query.filter(
            Booking.check_out_date == date.today(),
            Booking.status == 'checked_in'
        ).count()
        
        stats = {
            'total_bookings': total_bookings,
            'status_counts': status_counts,
            'recent_bookings': recent_bookings,
            'total_revenue': float(total_revenue),
            'today_checkins': today_checkins,
            'today_checkouts': today_checkouts,
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


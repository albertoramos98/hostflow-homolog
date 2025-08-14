from flask import Blueprint, request, jsonify
from src.models.user import db, User
import random
from datetime import datetime, date, timedelta
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    # Para demo, aceitar qualquer email/senha
    user_data = {
        'id': 1,
        'email': email,
        'name': 'Usuário Demo',
        'role': 'admin'
    }
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user_data
    }), 200

@user_bp.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    # Simular dados de estatísticas para o dashboard
    stats = {
        'revenue': {
            'value': 'R$ 45.230',
            'change': '+12%',
            'period': 'vs mês anterior'
        },
        'occupancy': {
            'value': '78%',
            'change': '+5%',
            'period': 'vs mês anterior'
        },
        'active_guests': {
            'value': '142',
            'change': '+8%',
            'period': 'vs mês anterior'
        },
        'checkins_today': {
            'value': '12',
            'change': '+3',
            'period': 'vs ontem'
        }
    }
    
    return jsonify(stats), 200

@user_bp.route('/dashboard/recent-bookings', methods=['GET'])
def recent_bookings():
    # Simular reservas recentes
    bookings = [
        {
            'id': 1,
            'guest_name': 'Maria Silva',
            'accommodation_name': 'Suíte Master',
            'check_in': '2024-01-15',
            'status': 'confirmed'
        },
        {
            'id': 2,
            'guest_name': 'João Santos',
            'accommodation_name': 'Quarto Duplo',
            'check_in': '2024-01-16',
            'status': 'pending'
        },
        {
            'id': 3,
            'guest_name': 'Ana Costa',
            'accommodation_name': 'Chalé Família',
            'check_in': '2024-01-17',
            'status': 'confirmed'
        }
    ]
    
    return jsonify(bookings), 200

@user_bp.route('/ai/insights', methods=['GET'])
def ai_insights():
    # Simular insights de IA baseados em regras simples
    insights = []
    
    # Insight sobre ocupação
    insights.append({
        'type': 'occupancy',
        'title': 'Taxa de Ocupação em Alta',
        'description': 'A taxa de ocupação aumentou 5% este mês. Continue investindo em marketing digital.',
        'priority': 'high',
        'action': 'Considere aumentar os preços em 10% para maximizar a receita.'
    })
    
    # Insight sobre receita
    insights.append({
        'type': 'revenue',
        'title': 'Receita Crescendo',
        'description': 'A receita mensal cresceu 12%. Ótimo trabalho!',
        'priority': 'medium',
        'action': 'Mantenha a estratégia atual e monitore a satisfação dos hóspedes.'
    })
    
    # Insight sobre sazonalidade
    insights.append({
        'type': 'seasonality',
        'title': 'Preparação para Alta Temporada',
        'description': 'Baseado nos dados históricos, a alta temporada se aproxima.',
        'priority': 'high',
        'action': 'Prepare promoções especiais e verifique a disponibilidade de quartos.'
    })
    
    return jsonify(insights), 200

@user_bp.route('/ai/predictions', methods=['GET'])
def ai_predictions():
    # Simular previsões baseadas em dados históricos
    predictions = {
        'next_month_revenue': {
            'value': 52000,
            'confidence': 85,
            'trend': 'up'
        },
        'occupancy_forecast': {
            'value': 82,
            'confidence': 78,
            'trend': 'up'
        },
        'peak_booking_days': [
            '2024-02-14',  # Dia dos Namorados
            '2024-02-24',  # Carnaval
            '2024-03-15'   # Feriado
        ]
    }
    
    return jsonify(predictions), 200

@user_bp.route('/properties', methods=['GET'])
def get_properties():
    # Simular dados de pousadas
    properties = [
        {
            'id': 1,
            'name': 'Pousada Vista Mar',
            'description': 'Uma pousada aconchegante com vista para o mar',
            'city': 'Búzios',
            'state': 'RJ',
            'is_active': True
        },
        {
            'id': 2,
            'name': 'Chalés da Montanha',
            'description': 'Chalés rústicos em meio à natureza',
            'city': 'Campos do Jordão',
            'state': 'SP',
            'is_active': True
        }
    ]
    
    return jsonify(properties), 200

@user_bp.route('/accommodations', methods=['GET'])
def get_accommodations():
    # Simular dados de acomodações
    accommodations = [
        {
            'id': 1,
            'property_id': 1,
            'name': 'Suíte Master',
            'type': 'suite',
            'capacity': 2,
            'price_per_night': 250.00,
            'is_available': True
        },
        {
            'id': 2,
            'property_id': 1,
            'name': 'Quarto Duplo',
            'type': 'quarto',
            'capacity': 2,
            'price_per_night': 180.00,
            'is_available': True
        },
        {
            'id': 3,
            'property_id': 2,
            'name': 'Chalé Família',
            'type': 'chale',
            'capacity': 4,
            'price_per_night': 320.00,
            'is_available': True
        }
    ]
    
    return jsonify(accommodations), 200

@user_bp.route('/guests', methods=['GET'])
def get_guests():
    # Simular dados de hóspedes
    guests = [
        {
            'id': 1,
            'name': 'Maria Silva',
            'email': 'maria@email.com',
            'phone': '(11) 99999-9999',
            'document': '123.456.789-00'
        },
        {
            'id': 2,
            'name': 'João Santos',
            'email': 'joao@email.com',
            'phone': '(21) 88888-8888',
            'document': '987.654.321-00'
        },
        {
            'id': 3,
            'name': 'Ana Costa',
            'email': 'ana@email.com',
            'phone': '(31) 77777-7777',
            'document': '456.789.123-00'
        }
    ]
    
    return jsonify(guests), 200

@user_bp.route('/bookings', methods=['GET'])
def get_bookings():
    # Simular dados de reservas
    bookings = [
        {
            'id': 1,
            'accommodation_id': 1,
            'guest_id': 1,
            'guest_name': 'Maria Silva',
            'accommodation_name': 'Suíte Master',
            'check_in': '2024-01-15',
            'check_out': '2024-01-18',
            'guests_count': 2,
            'total_amount': 750.00,
            'status': 'confirmed',
            'payment_status': 'paid'
        },
        {
            'id': 2,
            'accommodation_id': 2,
            'guest_id': 2,
            'guest_name': 'João Santos',
            'accommodation_name': 'Quarto Duplo',
            'check_in': '2024-01-16',
            'check_out': '2024-01-19',
            'guests_count': 2,
            'total_amount': 540.00,
            'status': 'pending',
            'payment_status': 'pending'
        },
        {
            'id': 3,
            'accommodation_id': 3,
            'guest_id': 3,
            'guest_name': 'Ana Costa',
            'accommodation_name': 'Chalé Família',
            'check_in': '2024-01-17',
            'check_out': '2024-01-20',
            'guests_count': 4,
            'total_amount': 960.00,
            'status': 'confirmed',
            'payment_status': 'paid'
        }
    ]
    
    return jsonify(bookings), 200
"""
Script para popular o banco de dados com dados de exemplo
"""
from datetime import datetime, date, timedelta
import json
from src.models.property import Property
from src.models.accommodation import Accommodation
from src.models.guest import Guest
from src.models.booking import Booking
from src.models.user import User, db

def create_sample_data():
    """Cria dados de exemplo para o sistema"""
    
    # Limpar dados existentes (exceto usuários)
    Booking.query.delete()
    Guest.query.delete()
    Accommodation.query.delete()
    Property.query.delete()
    
    # 1. Criar Pousadas
    properties_data = [
        {
            'name': 'Pousada Vista do Mar',
            'description': 'Uma pousada aconchegante com vista para o mar, localizada no coração de Búzios. Oferece quartos confortáveis e um ambiente familiar.',
            'address': 'Rua das Pedras, 123',
            'city': 'Búzios',
            'state': 'RJ',
            'zip_code': '28950-000',
            'phone': '(22) 2623-1234',
            'email': 'contato@pousadavistadomar.com.br',
            'website': 'www.pousadavistadomar.com.br',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'cancellation_policy': 'Cancelamento gratuito até 48h antes do check-in.',
            'house_rules': 'Não é permitido fumar. Animais de estimação não são aceitos. Silêncio após 22h.',
            'amenities': json.dumps([
                'Wi-Fi gratuito', 'Piscina', 'Café da manhã', 'Estacionamento',
                'Ar condicionado', 'TV a cabo', 'Frigobar', 'Vista para o mar'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
                'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800'
            ])
        },
        {
            'name': 'Chalés da Montanha',
            'description': 'Chalés rústicos em meio à natureza, perfeitos para quem busca tranquilidade e contato com a natureza em Petrópolis.',
            'address': 'Estrada da Montanha, 456',
            'city': 'Petrópolis',
            'state': 'RJ',
            'zip_code': '25750-000',
            'phone': '(24) 2237-5678',
            'email': 'reservas@chalesdamontanha.com.br',
            'website': 'www.chalesdamontanha.com.br',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'cancellation_policy': 'Cancelamento gratuito até 72h antes do check-in.',
            'house_rules': 'Permitido animais de pequeno porte. Não é permitido fumar nas acomodações.',
            'amenities': json.dumps([
                'Wi-Fi gratuito', 'Lareira', 'Cozinha equipada', 'Estacionamento',
                'Trilhas ecológicas', 'Área de churrasco', 'Vista da montanha'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'
            ])
        }
    ]
    
    properties = []
    for prop_data in properties_data:
        prop = Property(**prop_data)
        db.session.add(prop)
        properties.append(prop)
    
    db.session.flush()  # Para obter os IDs
    
    # 2. Criar Acomodações
    accommodations_data = [
        # Pousada Vista do Mar
        {
            'property_id': properties[0].id,
            'name': 'Quarto Standard Vista Mar',
            'type': 'quarto',
            'description': 'Quarto confortável com vista para o mar, cama de casal e varanda privativa.',
            'max_guests': 2,
            'bedrooms': 1,
            'bathrooms': 1,
            'beds': 1,
            'area_sqm': 25.0,
            'floor': '2º andar',
            'base_price': 180.00,
            'weekend_price': 220.00,
            'holiday_price': 280.00,
            'cleaning_fee': 30.00,
            'amenities': json.dumps([
                'Ar condicionado', 'TV a cabo', 'Frigobar', 'Wi-Fi',
                'Varanda', 'Vista para o mar', 'Roupa de cama'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',
                'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800'
            ]),
            'min_stay_nights': 2
        },
        {
            'property_id': properties[0].id,
            'name': 'Suíte Master Vista Mar',
            'type': 'suite',
            'description': 'Suíte espaçosa com vista panorâmica do mar, hidromassagem e sala de estar.',
            'max_guests': 4,
            'bedrooms': 1,
            'bathrooms': 1,
            'beds': 2,
            'area_sqm': 45.0,
            'floor': '3º andar',
            'base_price': 320.00,
            'weekend_price': 380.00,
            'holiday_price': 450.00,
            'cleaning_fee': 50.00,
            'amenities': json.dumps([
                'Ar condicionado', 'TV a cabo', 'Frigobar', 'Wi-Fi',
                'Hidromassagem', 'Sala de estar', 'Vista panorâmica',
                'Varanda ampla', 'Cofre'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800',
                'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'
            ]),
            'min_stay_nights': 2
        },
        # Chalés da Montanha
        {
            'property_id': properties[1].id,
            'name': 'Chalé Romântico',
            'type': 'chale',
            'description': 'Chalé aconchegante para casais, com lareira e vista da montanha.',
            'max_guests': 2,
            'bedrooms': 1,
            'bathrooms': 1,
            'beds': 1,
            'area_sqm': 35.0,
            'floor': 'Térreo',
            'base_price': 250.00,
            'weekend_price': 300.00,
            'holiday_price': 380.00,
            'cleaning_fee': 40.00,
            'amenities': json.dumps([
                'Lareira', 'Cozinha equipada', 'Wi-Fi', 'TV',
                'Varanda', 'Vista da montanha', 'Área externa privativa'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
            ]),
            'min_stay_nights': 1
        },
        {
            'property_id': properties[1].id,
            'name': 'Chalé Família',
            'type': 'chale',
            'description': 'Chalé amplo para famílias, com 2 quartos e sala de estar com lareira.',
            'max_guests': 6,
            'bedrooms': 2,
            'bathrooms': 2,
            'beds': 3,
            'area_sqm': 65.0,
            'floor': 'Térreo',
            'base_price': 420.00,
            'weekend_price': 480.00,
            'holiday_price': 580.00,
            'cleaning_fee': 60.00,
            'amenities': json.dumps([
                'Lareira', 'Cozinha completa', 'Wi-Fi', 'TV',
                'Sala de estar', 'Área de churrasco', 'Estacionamento',
                'Vista da montanha', 'Jardim privativo'
            ]),
            'main_image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
            'images': json.dumps([
                'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
            ]),
            'min_stay_nights': 2
        }
    ]
    
    accommodations = []
    for acc_data in accommodations_data:
        acc = Accommodation(**acc_data)
        db.session.add(acc)
        accommodations.append(acc)
    
    db.session.flush()
    
    # 3. Criar Hóspedes
    guests_data = [
        {
            'first_name': 'Maria',
            'last_name': 'Silva',
            'email': 'maria.silva@email.com',
            'phone': '(11) 99999-1234',
            'document_type': 'CPF',
            'document_number': '123.456.789-01',
            'address': 'Rua das Flores, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234-567',
            'birth_date': date(1985, 3, 15),
            'gender': 'Feminino',
            'nationality': 'Brasileira',
            'occupation': 'Engenheira',
            'preferences': json.dumps({
                'room_type': 'vista_mar',
                'bed_type': 'casal',
                'floor': 'alto'
            }),
            'newsletter_consent': True,
            'marketing_consent': True,
            'rating': 4.8
        },
        {
            'first_name': 'João',
            'last_name': 'Santos',
            'email': 'joao.santos@email.com',
            'phone': '(21) 98888-5678',
            'document_type': 'CPF',
            'document_number': '987.654.321-09',
            'address': 'Av. Atlântica, 456',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'zip_code': '22070-001',
            'birth_date': date(1978, 8, 22),
            'gender': 'Masculino',
            'nationality': 'Brasileira',
            'occupation': 'Médico',
            'special_requests': 'Quarto silencioso, longe do elevador',
            'newsletter_consent': False,
            'marketing_consent': True,
            'rating': 5.0
        },
        {
            'first_name': 'Ana',
            'last_name': 'Costa',
            'email': 'ana.costa@email.com',
            'phone': '(31) 97777-9012',
            'document_type': 'CPF',
            'document_number': '456.789.123-45',
            'address': 'Rua da Liberdade, 789',
            'city': 'Belo Horizonte',
            'state': 'MG',
            'zip_code': '30112-000',
            'birth_date': date(1992, 12, 5),
            'gender': 'Feminino',
            'nationality': 'Brasileira',
            'occupation': 'Designer',
            'preferences': json.dumps({
                'room_type': 'chale',
                'amenities': ['lareira', 'vista_montanha']
            }),
            'newsletter_consent': True,
            'marketing_consent': False,
            'rating': 4.5
        },
        {
            'first_name': 'Carlos',
            'last_name': 'Oliveira',
            'email': 'carlos.oliveira@email.com',
            'phone': '(85) 96666-3456',
            'document_type': 'CPF',
            'document_number': '789.123.456-78',
            'address': 'Rua do Sol, 321',
            'city': 'Fortaleza',
            'state': 'CE',
            'zip_code': '60000-000',
            'birth_date': date(1980, 6, 10),
            'gender': 'Masculino',
            'nationality': 'Brasileira',
            'occupation': 'Empresário',
            'special_requests': 'Check-in antecipado se possível',
            'newsletter_consent': True,
            'marketing_consent': True,
            'rating': 4.2
        }
    ]
    
    guests = []
    for guest_data in guests_data:
        guest = Guest(**guest_data)
        db.session.add(guest)
        guests.append(guest)
    
    db.session.flush()
    
    # 4. Criar Reservas
    today = date.today()
    
    bookings_data = [
        # Reserva passada (check-out concluído)
        {
            'accommodation_id': accommodations[0].id,  # Quarto Standard Vista Mar
            'guest_id': guests[0].id,  # Maria Silva
            'check_in_date': today - timedelta(days=15),
            'check_out_date': today - timedelta(days=12),
            'adults': 2,
            'children': 0,
            'base_amount': 540.00,  # 3 noites x 180
            'cleaning_fee': 30.00,
            'service_fee': 25.00,
            'taxes': 15.00,
            'total_amount': 610.00,
            'status': 'checked_out',
            'payment_status': 'paid',
            'payment_method': 'Cartão de Crédito',
            'payment_date': datetime.now() - timedelta(days=20),
            'actual_check_in': datetime.combine(today - timedelta(days=15), datetime.min.time().replace(hour=14)),
            'actual_check_out': datetime.combine(today - timedelta(days=12), datetime.min.time().replace(hour=11)),
            'source': 'direct',
            'guest_rating': 5,
            'guest_review': 'Excelente estadia! Vista maravilhosa e atendimento impecável.',
            'host_rating': 5
        },
        # Reserva atual (hóspede está na pousada)
        {
            'accommodation_id': accommodations[2].id,  # Chalé Romântico
            'guest_id': guests[1].id,  # João Santos
            'check_in_date': today - timedelta(days=1),
            'check_out_date': today + timedelta(days=2),
            'adults': 2,
            'children': 0,
            'base_amount': 750.00,  # 3 noites (1 weekend)
            'cleaning_fee': 40.00,
            'service_fee': 30.00,
            'taxes': 20.00,
            'total_amount': 840.00,
            'status': 'checked_in',
            'payment_status': 'paid',
            'payment_method': 'PIX',
            'payment_date': datetime.now() - timedelta(days=5),
            'actual_check_in': datetime.combine(today - timedelta(days=1), datetime.min.time().replace(hour=15)),
            'source': 'direct',
            'special_requests': 'Lua de mel - decoração especial se possível'
        },
        # Reserva futura confirmada
        {
            'accommodation_id': accommodations[1].id,  # Suíte Master Vista Mar
            'guest_id': guests[2].id,  # Ana Costa
            'check_in_date': today + timedelta(days=10),
            'check_out_date': today + timedelta(days=13),
            'adults': 2,
            'children': 1,
            'base_amount': 960.00,  # 3 noites
            'cleaning_fee': 50.00,
            'service_fee': 40.00,
            'taxes': 25.00,
            'total_amount': 1075.00,
            'status': 'confirmed',
            'payment_status': 'paid',
            'payment_method': 'Cartão de Crédito',
            'payment_date': datetime.now() - timedelta(days=2),
            'source': 'booking.com',
            'special_requests': 'Berço para bebê'
        },
        # Reserva futura pendente
        {
            'accommodation_id': accommodations[3].id,  # Chalé Família
            'guest_id': guests[3].id,  # Carlos Oliveira
            'check_in_date': today + timedelta(days=20),
            'check_out_date': today + timedelta(days=25),
            'adults': 4,
            'children': 2,
            'base_amount': 2400.00,  # 5 noites (inclui weekend)
            'cleaning_fee': 60.00,
            'service_fee': 50.00,
            'taxes': 35.00,
            'total_amount': 2545.00,
            'status': 'pending',
            'payment_status': 'pending',
            'source': 'direct',
            'special_requests': 'Chegada com família grande - check-in flexível'
        },
        # Reserva cancelada
        {
            'accommodation_id': accommodations[0].id,  # Quarto Standard Vista Mar
            'guest_id': guests[0].id,  # Maria Silva
            'check_in_date': today + timedelta(days=5),
            'check_out_date': today + timedelta(days=7),
            'adults': 1,
            'children': 0,
            'base_amount': 360.00,  # 2 noites
            'cleaning_fee': 30.00,
            'service_fee': 20.00,
            'taxes': 12.00,
            'total_amount': 422.00,
            'status': 'cancelled',
            'payment_status': 'refunded',
            'payment_method': 'Cartão de Crédito',
            'source': 'direct',
            'cancellation_reason': 'Mudança de planos - viagem de trabalho cancelada',
            'cancelled_at': datetime.now() - timedelta(days=3)
        }
    ]
    
    for booking_data in bookings_data:
        # Calcular noites
        booking_data['nights'] = (booking_data['check_out_date'] - booking_data['check_in_date']).days
        booking_data['total_guests'] = booking_data['adults'] + booking_data['children']
        booking_data['property_id'] = Accommodation.query.get(booking_data['accommodation_id']).property_id
        
        booking = Booking(**booking_data)
        db.session.add(booking)
    
    # Commit todas as mudanças
    db.session.commit()
    
    # Atualizar estatísticas dos hóspedes
    for guest in guests:
        guest.update_stats()
    
    db.session.commit()
    
    print("✅ Dados de exemplo criados com sucesso!")
    print(f"   - {len(properties)} pousadas")
    print(f"   - {len(accommodations)} acomodações")
    print(f"   - {len(guests)} hóspedes")
    print(f"   - {len(bookings_data)} reservas")

if __name__ == '__main__':
    create_sample_data()


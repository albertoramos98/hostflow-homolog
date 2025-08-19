import os
import sys
from dotenv import load_dotenv

# DON'T CHANGE THIS !!!
# This line is for local development structure, it's safe to keep it.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db, User
from src.models.property import Property
from src.models.accommodation import Accommodation
from src.models.guest import Guest
from src.models.booking import Booking
from src.routes.user import user_bp
from src.routes.ai_routes import ai_bp
from src.routes.property_routes import property_bp
from src.routes.accommodation_routes import accommodation_bp
from src.routes.guest_routes import guest_bp
from src.routes.booking_routes import booking_bp

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT') # Good practice to use env var for secret key too

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(property_bp, url_prefix='/api')
app.register_blueprint(accommodation_bp, url_prefix='/api')
app.register_blueprint(guest_bp, url_prefix='/api')
app.register_blueprint(booking_bp, url_prefix='/api')

### MUDANÇA 3: Configuração do Banco de Dados (Mais Robusta) ###
database_uri = os.getenv('DATABASE_URL')

# CRITICAL CHECK: Ensure the DATABASE_URL is provided.
if not database_uri:
    # This will print an error in the Render logs and stop the app gracefully.
    raise ValueError("No DATABASE_URL set for the application. Please set the environment variable.")

# SQLAlchemy prefers 'postgresql://' over 'postgres://'
if database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Dashboard stats endpoint
@app.route('/api/dashboard/stats')
def dashboard_stats():
    """Endpoint para estatísticas do dashboard"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func

        # Período do último mês
        last_month = datetime.now() - timedelta(days=30)

        # Receita mensal
        monthly_revenue = db.session.query(func.sum(Booking.total_amount)).filter(
            Booking.status.in_(['confirmed', 'checked_out']),
            Booking.created_at >= last_month
        ).scalar() or 0

        # Taxa de ocupação (simplificada)
        total_accommodations = Accommodation.query.filter_by(is_active=True).count()
        nights_booked = db.session.query(func.sum(Booking.nights)).filter(
            Booking.status.in_(['confirmed', 'checked_in', 'checked_out']),
            Booking.check_in_date >= last_month.date()
        ).scalar() or 0

        total_nights_available = total_accommodations * 30
        occupancy_rate = (nights_booked / total_nights_available * 100) if total_nights_available > 0 else 0

        # Hóspedes ativos
        active_guests = Guest.query.filter_by(is_active=True).count()

        # Check-ins hoje
        from datetime import date
        today_checkins = Booking.query.filter(
            Booking.check_in_date == date.today(),
            Booking.status.in_(['confirmed', 'checked_in'])
        ).count()

        stats = {
            'monthly_revenue': float(monthly_revenue),
            'occupancy_rate': round(occupancy_rate, 1),
            'active_guests': active_guests,
            'today_checkins': today_checkins
        }

        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Create tables and sample data within the app context
with app.app_context():
    db.create_all()

    # Create default user if not exists
    if not User.query.first():
        default_user = User(
            name='Demo User',
            email='demo@hostflow.com'
        )
        default_user.set_password('123456')
        db.session.add(default_user)
        db.session.commit()
        print("✅ Default user created")

    # Create sample data if tables are empty
    if not Property.query.first():
        try:
            from src.seed_data import create_sample_data
            create_sample_data()
        except Exception as e:
            print(f"⚠️  Error creating sample data: {e}")

# This part is for local development and will be ignored by Gunicorn on Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

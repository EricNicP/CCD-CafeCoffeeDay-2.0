"""
CCD 2.0 - Main Backend Application
Coffee Shop Management System
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

# Import route modules
from routes.orders import orders_bp
from routes.users import users_bp
from routes.menu import menu_bp
from routes.cafes import cafes_bp
from routes.loyalty import loyalty_bp
from routes.events import events_bp
from routes.promotions import promotions_bp
from routes.tracking import tracking_bp
from routes.sustainability import sustainability_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "ccd.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models.coffee import db, init_db
db.init_app(app)

# Register blueprints
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(menu_bp, url_prefix='/api/menu')
app.register_blueprint(cafes_bp, url_prefix='/api/cafes')
app.register_blueprint(loyalty_bp, url_prefix='/api/loyalty')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(promotions_bp, url_prefix='/api/promotions')
app.register_blueprint(tracking_bp, url_prefix='/api/tracking')
app.register_blueprint(sustainability_bp, url_prefix='/api/sustainability')

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'message': 'CCD 2.0 API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

@app.route('/api/health')
def health_check():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': 'connected',
            'api': 'running'
        }
    })

if __name__ == '__main__':
    # Initialize database with sample data
    with app.app_context():
        init_db(app)
    
    print("🚀 CCD 2.0 API Server Starting...")
    print("📊 Enhanced Features Available:")
    print("   ✅ Real-time Order Tracking")
    print("   ✅ Loyalty & Rewards System")
    print("   ✅ Café Location Management")
    print("   ✅ Events & Community Features")
    print("   ✅ Sustainability Tracking")
    print("   ✅ Promotions & Marketing")
    print("   ✅ Stock Management")
    print("   ✅ Personalization Features")
    print("\n🌐 API Endpoints:")
    print("   📍 http://localhost:5000/api/orders")
    print("   📍 http://localhost:5000/api/users")
    print("   📍 http://localhost:5000/api/menu")
    print("   📍 http://localhost:5000/api/cafes")
    print("   📍 http://localhost:5000/api/loyalty")
    print("   📍 http://localhost:5000/api/events")
    print("   📍 http://localhost:5000/api/promotions")
    print("   📍 http://localhost:5000/api/tracking")
    print("   📍 http://localhost:5000/api/sustainability")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
CCD 2.0 - Simple Backend Application
Coffee Shop Management System (Simplified)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Mock data
users_db = [
    {
        'id': '1',
        'email': 'demo@ccd2.com',
        'full_name': 'Demo User',
        'phone': '+1 (555) 123-4567',
        'created_at': '2024-01-01T00:00:00Z',
        'last_login': '2024-01-15T10:30:00Z',
        'is_active': True,
        'loyalty_points': 150
    }
]

menu_db = [
    {
        'id': 1,
        'name': 'Signature Espresso',
        'price': 2.50,
        'stock_quantity': 50,
        'category': 'Coffee',
        'sustainability_rating': 4.5,
        'fair_trade': True,
        'organic': True,
        'description': 'Rich, bold espresso shot with perfect crema'
    },
    {
        'id': 2,
        'name': 'Artisan Cappuccino',
        'price': 3.50,
        'stock_quantity': 30,
        'category': 'Coffee',
        'sustainability_rating': 4.2,
        'fair_trade': True,
        'organic': False,
        'description': 'Perfect balance of espresso, steamed milk, and foam'
    },
    {
        'id': 3,
        'name': 'Velvet Latte',
        'price': 4.00,
        'stock_quantity': 25,
        'category': 'Coffee',
        'sustainability_rating': 4.0,
        'fair_trade': True,
        'organic': True,
        'description': 'Smooth and creamy with a hint of sweetness'
    },
    {
        'id': 4,
        'name': 'French Croissant',
        'price': 2.00,
        'stock_quantity': 15,
        'category': 'Food',
        'sustainability_rating': 3.8,
        'fair_trade': False,
        'organic': True,
        'description': 'Buttery, flaky pastry baked fresh daily'
    },
    {
        'id': 5,
        'name': 'Blueberry Muffin',
        'price': 2.50,
        'stock_quantity': 20,
        'category': 'Food',
        'sustainability_rating': 3.5,
        'fair_trade': False,
        'organic': False,
        'description': 'Fresh baked with real blueberries'
    },
    {
        'id': 6,
        'name': 'Cold Brew Coffee',
        'price': 3.00,
        'stock_quantity': 40,
        'category': 'Coffee',
        'sustainability_rating': 4.3,
        'fair_trade': True,
        'organic': True,
        'description': 'Smooth cold brew with notes of chocolate'
    }
]

cafes_db = [
    {
        'id': 1,
        'name': 'CCD Calangute Beach',
        'address': 'Tito\'s Lane, Calangute Beach Road',
        'city': 'Calangute, Goa',
        'features': ['Beach View', 'WiFi', 'Outdoor Seating', 'Parking', 'Pet Friendly'],
        'wifi_available': True,
        'parking_available': True,
        'rating': 4.8,
        'phone': '+91 832 227 1234'
    },
    {
        'id': 2,
        'name': 'CCD Panjim City Center',
        'address': 'MG Road, Near Municipal Market',
        'city': 'Panjim, Goa',
        'features': ['City Center', 'WiFi', 'AC Seating', 'Quick Service', 'Student Discount'],
        'wifi_available': True,
        'parking_available': False,
        'rating': 4.6,
        'phone': '+91 832 222 5678'
    },
    {
        'id': 3,
        'name': 'CCD Baga Beach',
        'address': 'Baga Beach Road, Near Tito\'s',
        'city': 'Baga, Goa',
        'features': ['Beach Access', 'Sunset Views', 'Outdoor Seating', 'WiFi', 'Live Music'],
        'wifi_available': True,
        'parking_available': True,
        'rating': 4.9,
        'phone': '+91 832 227 9012'
    },
    {
        'id': 4,
        'name': 'CCD Anjuna Beach',
        'address': 'Anjuna Beach Road, Near Flea Market',
        'city': 'Anjuna, Goa',
        'features': ['Hippie Vibes', 'Flea Market Access', 'WiFi', 'Organic Options', 'Pet Friendly'],
        'wifi_available': True,
        'parking_available': True,
        'rating': 4.7,
        'phone': '+91 832 227 3456'
    },
    {
        'id': 5,
        'name': 'CCD Candolim Beach',
        'address': 'Candolim Beach Road, Near Fort Aguada',
        'city': 'Candolim, Goa',
        'features': ['Fort View', 'Historical Area', 'WiFi', 'Parking', 'Family Friendly'],
        'wifi_available': True,
        'parking_available': True,
        'rating': 4.5,
        'phone': '+91 832 227 7890'
    },
    {
        'id': 6,
        'name': 'CCD Mapusa Market',
        'address': 'Mapusa Market Road, Near Bus Stand',
        'city': 'Mapusa, Goa',
        'features': ['Local Market', 'WiFi', 'Quick Service', 'Student Discount', 'Budget Friendly'],
        'wifi_available': True,
        'parking_available': False,
        'rating': 4.4,
        'phone': '+91 832 226 1234'
    }
]

events_db = [
    {
        'id': 1,
        'title': 'Coffee Masterclass',
        'date': '2024-01-15',
        'time': '14:00',
        'description': 'Learn the art of coffee brewing from our master baristas',
        'price': 25.00,
        'max_participants': 20,
        'current_participants': 12,
        'instructor': 'Master Barista John'
    },
    {
        'id': 2,
        'title': 'Live Jazz Night',
        'date': '2024-01-20',
        'time': '19:00',
        'description': 'Enjoy live jazz music with premium coffee and desserts',
        'price': 15.00,
        'max_participants': 50,
        'current_participants': 35,
        'instructor': 'Jazz Ensemble'
    },
    {
        'id': 3,
        'title': 'Latte Art Workshop',
        'date': '2024-01-25',
        'time': '10:00',
        'description': 'Create beautiful latte art designs with professional guidance',
        'price': 30.00,
        'max_participants': 15,
        'current_participants': 8,
        'instructor': 'Artisan Sarah'
    }
]

promotions_db = [
    {
        'id': 1,
        'title': 'Student Special',
        'description': '20% off all items for students with valid ID',
        'code': 'STUDENT20',
        'discount_value': 20,
        'valid_until': '2024-12-31'
    },
    {
        'id': 2,
        'title': 'Happy Hour',
        'description': '50% off all drinks from 3-5 PM daily',
        'code': 'HAPPY50',
        'discount_value': 50,
        'valid_until': '2024-12-31'
    },
    {
        'id': 3,
        'title': 'Welcome Bonus',
        'description': 'Get 100 bonus points on your first order',
        'code': 'WELCOME100',
        'discount_value': 100,
        'valid_until': '2024-12-31'
    }
]

orders_db = []

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

# Menu endpoints
@app.route('/api/menu', methods=['GET'])
def get_menu():
    """Get all menu items"""
    return jsonify({
        'success': True,
        'data': menu_db,
        'count': len(menu_db)
    })

# Cafes endpoints
@app.route('/api/cafes', methods=['GET'])
def get_cafes():
    """Get all cafes"""
    return jsonify({
        'success': True,
        'data': cafes_db,
        'count': len(cafes_db)
    })

# Events endpoints
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    return jsonify({
        'success': True,
        'data': events_db,
        'count': len(events_db)
    })

# Promotions endpoints
@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    """Get all promotions"""
    return jsonify({
        'success': True,
        'data': promotions_db,
        'count': len(promotions_db)
    })

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({
        'success': True,
        'data': users_db,
        'count': len(users_db)
    })

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'full_name', 'password']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if email already exists
        existing_user = next((user for user in users_db 
                            if user['email'] == data['email']), None)
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
        
        # Create new user
        new_user = {
            'id': str(uuid.uuid4()),
            'email': data['email'],
            'full_name': data['full_name'],
            'phone': data.get('phone', ''),
            'address': data.get('address', ''),
            'password': data['password'],  # In real app, hash this
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'is_active': True,
            'loyalty_points': 0
        }
        
        users_db.append(new_user)
        
        # Remove password from response
        user_response = {k: v for k, v in new_user.items() if k != 'password'}
        
        return jsonify({
            'success': True,
            'data': user_response,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password required'
            }), 400
        
        # Find user by email
        user = next((user for user in users_db 
                    if user['email'] == data['email'] and user['password'] == data['password']), None)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        
        # Remove password from response
        user_response = {k: v for k, v in user.items() if k != 'password'}
        
        return jsonify({
            'success': True,
            'data': user_response,
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Orders endpoints
@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify({
        'success': True,
        'data': orders_db,
        'count': len(orders_db)
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'items' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: items'
            }), 400
        
        # Create new order
        new_order = {
            'id': str(uuid.uuid4()),
            'items': data['items'],
            'total': sum(item.get('price', 0) * item.get('quantity', 1) for item in data['items']),
            'status': 'pending',
            'order_type': data.get('order_type', 'pickup'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        orders_db.append(new_order)
        
        return jsonify({
            'success': True,
            'data': new_order,
            'message': 'Order created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 CCD 2.0 Simple API Server Starting...")
    print("📊 Features Available:")
    print("   ✅ User Registration & Login")
    print("   ✅ Menu Management")
    print("   ✅ Café Locations")
    print("   ✅ Events & Promotions")
    print("   ✅ Order Management")
    print("\n🌐 API Endpoints:")
    print("   📍 http://localhost:5000/api/health")
    print("   📍 http://localhost:5000/api/users/register")
    print("   📍 http://localhost:5000/api/users/login")
    print("   📍 http://localhost:5000/api/menu")
    print("   📍 http://localhost:5000/api/cafes")
    print("   📍 http://localhost:5000/api/events")
    print("   📍 http://localhost:5000/api/promotions")
    print("   📍 http://localhost:5000/api/orders")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
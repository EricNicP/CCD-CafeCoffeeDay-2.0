"""
Users API Routes
Handles all user-related operations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

users_bp = Blueprint('users', __name__)

# Mock data for development
users_db = [
    {
        'id': '1',
        'username': 'john_doe',
        'email': 'john@example.com',
        'full_name': 'John Doe',
        'phone': '+1234567890',
        'address': '123 Main St, City, State',
        'created_at': '2024-01-01T00:00:00Z',
        'last_login': '2024-01-15T10:30:00Z',
        'is_active': True
    },
    {
        'id': '2',
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'full_name': 'Jane Smith',
        'phone': '+1234567891',
        'address': '456 Oak Ave, City, State',
        'created_at': '2024-01-02T00:00:00Z',
        'last_login': '2024-01-14T15:45:00Z',
        'is_active': True
    }
]

@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        return jsonify({
            'success': True,
            'data': users_db,
            'count': len(users_db)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    try:
        user = next((user for user in users_db if user['id'] == user_id), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@users_bp.route('/register', methods=['POST'])
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
        
        return jsonify({
            'success': True,
            'data': new_user,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@users_bp.route('/login', methods=['POST'])
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

@users_bp.route('/', methods=['POST'])
def create_user():
    """Create new user (legacy endpoint)"""
    return register_user()

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        
        # Find user
        user = next((user for user in users_db if user['id'] == user_id), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Update allowed fields
        updatable_fields = ['full_name', 'phone', 'address', 'email']
        for field in updatable_fields:
            if field in data:
                user[field] = data[field]
        
        return jsonify({
            'success': True,
            'data': user,
            'message': 'User updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@users_bp.route('/<user_id>/login', methods=['POST'])
def user_login(user_id):
    """Update user's last login time"""
    try:
        user = next((user for user in users_db if user['id'] == user_id), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user['last_login'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': user,
            'message': 'Login recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

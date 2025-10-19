"""
Menu API Routes
Handles all menu-related operations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

menu_bp = Blueprint('menu', __name__)

# Mock data for development
menu_items = [
    {
        'id': '1',
        'name': 'Espresso',
        'description': 'Rich, full-bodied coffee with a thick layer of crema',
        'price': 3.50,
        'category': 'coffee',
        'size': 'small',
        'available': True,
        'image_url': '/static/images/espresso.jpg',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': '2',
        'name': 'Cappuccino',
        'description': 'Espresso with steamed milk and foam',
        'price': 4.50,
        'category': 'coffee',
        'size': 'medium',
        'available': True,
        'image_url': '/static/images/cappuccino.jpg',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': '3',
        'name': 'Latte',
        'description': 'Espresso with steamed milk and a small amount of foam',
        'price': 5.00,
        'category': 'coffee',
        'size': 'large',
        'available': True,
        'image_url': '/static/images/latte.jpg',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': '4',
        'name': 'Croissant',
        'description': 'Buttery, flaky pastry perfect with coffee',
        'price': 3.00,
        'category': 'pastry',
        'size': 'regular',
        'available': True,
        'image_url': '/static/images/croissant.jpg',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    }
]

@menu_bp.route('/', methods=['GET'])
def get_menu():
    """Get all menu items"""
    try:
        # Filter by category if provided
        category = request.args.get('category')
        available_only = request.args.get('available', 'true').lower() == 'true'
        
        filtered_items = menu_items
        
        if category:
            filtered_items = [item for item in filtered_items if item['category'] == category]
        
        if available_only:
            filtered_items = [item for item in filtered_items if item['available']]
        
        return jsonify({
            'success': True,
            'data': filtered_items,
            'count': len(filtered_items)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/<item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get specific menu item by ID"""
    try:
        item = next((item for item in menu_items if item['id'] == item_id), None)
        if not item:
            return jsonify({
                'success': False,
                'error': 'Menu item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': item
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/', methods=['POST'])
def create_menu_item():
    """Create new menu item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'price', 'category']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new menu item
        new_item = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'category': data['category'],
            'size': data.get('size', 'regular'),
            'available': data.get('available', True),
            'image_url': data.get('image_url', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        menu_items.append(new_item)
        
        return jsonify({
            'success': True,
            'data': new_item,
            'message': 'Menu item created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/<item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update menu item"""
    try:
        data = request.get_json()
        
        # Find item
        item = next((item for item in menu_items if item['id'] == item_id), None)
        if not item:
            return jsonify({
                'success': False,
                'error': 'Menu item not found'
            }), 404
        
        # Update allowed fields
        updatable_fields = ['name', 'description', 'price', 'category', 'size', 'available', 'image_url']
        for field in updatable_fields:
            if field in data:
                item[field] = data[field]
        
        item['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': item,
            'message': 'Menu item updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all menu categories"""
    try:
        categories = list(set(item['category'] for item in menu_items))
        return jsonify({
            'success': True,
            'data': categories
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

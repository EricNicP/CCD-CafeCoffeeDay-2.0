"""
Orders API Routes
Handles all order-related operations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__)

# Mock data for development
orders_db = [
    {
        'id': '1',
        'customer_id': '1',
        'items': [
            {'coffee_id': '1', 'name': 'Espresso', 'quantity': 2, 'price': 3.50},
            {'coffee_id': '2', 'name': 'Cappuccino', 'quantity': 1, 'price': 4.50}
        ],
        'total': 11.50,
        'status': 'pending',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-15T10:30:00Z'
    }
]

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        return jsonify({
            'success': True,
            'data': orders_db,
            'count': len(orders_db)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order by ID"""
    try:
        order = next((order for order in orders_db if order['id'] == order_id), None)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': order
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'customer_id' not in data or 'items' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: customer_id, items'
            }), 400
        
        # Create new order
        new_order = {
            'id': str(uuid.uuid4()),
            'customer_id': data['customer_id'],
            'items': data['items'],
            'total': sum(item.get('price', 0) * item.get('quantity', 1) for item in data['items']),
            'status': 'pending',
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

@orders_bp.route('/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        # Find and update order
        order = next((order for order in orders_db if order['id'] == order_id), None)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        order['status'] = new_status
        order['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Order status updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

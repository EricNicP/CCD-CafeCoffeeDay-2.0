"""
Real-time Tracking API Routes
Handles order tracking, stock updates, and live status
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
from ..models.coffee import db, Order, OrderTracking, StockUpdate, Coffee

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/orders/<order_id>/status', methods=['GET'])
def get_order_status(order_id):
    """Get real-time order status and tracking"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        # Get tracking updates
        tracking_updates = OrderTracking.query.filter_by(order_id=order_id).order_by(OrderTracking.created_at.desc()).all()
        
        # Calculate estimated time
        estimated_time = None
        if order.estimated_ready_time:
            estimated_time = order.estimated_ready_time.isoformat()
        elif order.preparation_start_time:
            # Estimate based on preparation time
            prep_time = timedelta(minutes=10)  # Default preparation time
            estimated_time = (order.preparation_start_time + prep_time).isoformat()
        
        return jsonify({
            'success': True,
            'data': {
                'order_id': order.id,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'estimated_ready_time': estimated_time,
                'tracking_updates': [update.to_dict() for update in tracking_updates],
                'order_type': order.order_type,
                'cafe_id': order.cafe_id,
                'table_number': order.table_number
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tracking_bp.route('/orders/<order_id>/update', methods=['POST'])
def update_order_status(order_id):
    """Update order status with tracking"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        message = data.get('message')
        estimated_time = data.get('estimated_time')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        # Update order status
        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.now()
        
        # Set specific timestamps based on status
        if new_status == 'preparing' and not order.preparation_start_time:
            order.preparation_start_time = datetime.now()
        elif new_status == 'ready' and not order.ready_time:
            order.ready_time = datetime.now()
            order.preparation_end_time = datetime.now()
        
        # Set estimated time
        if estimated_time:
            order.estimated_ready_time = datetime.fromisoformat(estimated_time.replace('Z', '+00:00'))
        
        # Create tracking update
        tracking_update = OrderTracking(
            order_id=order_id,
            status=new_status,
            message=message or f'Order status changed from {old_status} to {new_status}',
            estimated_time=order.estimated_ready_time
        )
        
        db.session.add(tracking_update)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'order_id': order.id,
                'old_status': old_status,
                'new_status': new_status,
                'updated_at': order.updated_at.isoformat(),
                'tracking_update': tracking_update.to_dict()
            },
            'message': 'Order status updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tracking_bp.route('/stock/updates', methods=['GET'])
def get_stock_updates():
    """Get recent stock updates"""
    try:
        coffee_id = request.args.get('coffee_id')
        cafe_id = request.args.get('cafe_id')
        limit = request.args.get('limit', 50, type=int)
        
        query = StockUpdate.query
        
        if coffee_id:
            query = query.filter_by(coffee_id=coffee_id)
        if cafe_id:
            query = query.filter_by(cafe_id=cafe_id)
        
        updates = query.order_by(StockUpdate.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [update.to_dict() for update in updates],
            'count': len(updates)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tracking_bp.route('/stock/update', methods=['POST'])
def update_stock():
    """Update stock levels"""
    try:
        data = request.get_json()
        coffee_id = data.get('coffee_id')
        quantity_change = data.get('quantity_change', 0)
        reason = data.get('reason', 'manual_update')
        cafe_id = data.get('cafe_id')
        updated_by = data.get('updated_by')
        
        if not coffee_id:
            return jsonify({
                'success': False,
                'error': 'Coffee ID is required'
            }), 400
        
        coffee = Coffee.query.get(coffee_id)
        if not coffee:
            return jsonify({
                'success': False,
                'error': 'Coffee item not found'
            }), 404
        
        # Update stock quantity
        old_quantity = coffee.stock_quantity
        new_quantity = max(0, old_quantity + quantity_change)
        coffee.stock_quantity = new_quantity
        
        # Update availability based on stock
        coffee.available = new_quantity > coffee.min_stock_level
        
        # Create stock update record
        stock_update = StockUpdate(
            coffee_id=coffee_id,
            cafe_id=cafe_id,
            quantity_change=quantity_change,
            new_stock_level=new_quantity,
            reason=reason,
            updated_by=updated_by
        )
        
        db.session.add(stock_update)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'coffee_id': coffee.id,
                'coffee_name': coffee.name,
                'old_quantity': old_quantity,
                'new_quantity': new_quantity,
                'quantity_change': quantity_change,
                'available': coffee.available,
                'stock_update': stock_update.to_dict()
            },
            'message': 'Stock updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tracking_bp.route('/orders/<order_id>/qr', methods=['GET'])
def generate_qr_code(order_id):
    """Generate QR code for table ordering"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        # Generate QR code data
        qr_data = {
            'order_id': order.id,
            'table_number': order.table_number,
            'cafe_id': order.cafe_id,
            'created_at': order.created_at.isoformat()
        }
        
        # In a real implementation, you would generate an actual QR code
        # For now, we'll return the data that would be encoded
        return jsonify({
            'success': True,
            'data': {
                'qr_data': qr_data,
                'qr_code_url': f'/api/tracking/orders/{order_id}/qr.png',  # Placeholder
                'order_id': order.id,
                'table_number': order.table_number
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







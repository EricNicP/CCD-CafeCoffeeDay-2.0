"""
Promotions API Routes
Handles marketing promotions, offers, and geo-targeted campaigns
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
from ..models.coffee import db, Promotion

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/', methods=['GET'])
def get_promotions():
    """Get all active promotions"""
    try:
        # Filter parameters
        promo_type = request.args.get('type')
        city = request.args.get('city')
        user_location = request.args.get('user_location')
        
        query = Promotion.query.filter_by(is_active=True)
        query = query.filter(Promotion.start_date <= datetime.now())
        query = query.filter(Promotion.end_date >= datetime.now())
        
        if promo_type:
            query = query.filter_by(promo_type=promo_type)
        
        promotions = query.order_by(Promotion.created_at.desc()).all()
        
        # Filter geo-targeted promotions
        if city or user_location:
            filtered_promotions = []
            for promo in promotions:
                if promo.geo_targeted:
                    target_cities = promo.target_cities or '[]'
                    if city and city in target_cities:
                        filtered_promotions.append(promo)
                else:
                    filtered_promotions.append(promo)
            promotions = filtered_promotions
        
        return jsonify({
            'success': True,
            'data': [promo.to_dict() for promo in promotions],
            'count': len(promotions)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@promotions_bp.route('/<promo_id>', methods=['GET'])
def get_promotion(promo_id):
    """Get specific promotion by ID"""
    try:
        promotion = Promotion.query.get(promo_id)
        if not promotion:
            return jsonify({
                'success': False,
                'error': 'Promotion not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': promotion.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@promotions_bp.route('/validate', methods=['POST'])
def validate_promo_code():
    """Validate promo code and calculate discount"""
    try:
        data = request.get_json()
        promo_code = data.get('promo_code')
        order_amount = data.get('order_amount', 0)
        user_location = data.get('user_location')
        
        if not promo_code:
            return jsonify({
                'success': False,
                'error': 'Promo code is required'
            }), 400
        
        promotion = Promotion.query.filter_by(promo_code=promo_code).first()
        if not promotion:
            return jsonify({
                'success': False,
                'error': 'Invalid promo code'
            }), 404
        
        # Check if promotion is active
        if not promotion.is_active:
            return jsonify({
                'success': False,
                'error': 'Promotion is not active'
            }), 400
        
        # Check date validity
        now = datetime.now()
        if now < promotion.start_date or now > promotion.end_date:
            return jsonify({
                'success': False,
                'error': 'Promotion has expired'
            }), 400
        
        # Check usage limit
        if promotion.usage_limit and promotion.usage_count >= promotion.usage_limit:
            return jsonify({
                'success': False,
                'error': 'Promotion usage limit reached'
            }), 400
        
        # Check minimum order amount
        if promotion.min_order_amount and order_amount < promotion.min_order_amount:
            return jsonify({
                'success': False,
                'error': f'Minimum order amount of ₹{promotion.min_order_amount} required'
            }), 400
        
        # Check geo-targeting
        if promotion.geo_targeted and user_location:
            target_cities = promotion.target_cities or '[]'
            if user_location not in target_cities:
                return jsonify({
                    'success': False,
                    'error': 'Promotion not available in your location'
                }), 400
        
        # Calculate discount
        discount_amount = 0
        if promotion.discount_percentage:
            discount_amount = (order_amount * promotion.discount_percentage) / 100
            if promotion.max_discount:
                discount_amount = min(discount_amount, promotion.max_discount)
        elif promotion.discount_amount:
            discount_amount = promotion.discount_amount
        
        return jsonify({
            'success': True,
            'data': {
                'promotion_id': promotion.id,
                'title': promotion.title,
                'discount_amount': discount_amount,
                'final_amount': order_amount - discount_amount,
                'promo_type': promotion.promo_type
            },
            'message': 'Promo code is valid'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@promotions_bp.route('/', methods=['POST'])
def create_promotion():
    """Create new promotion"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'promo_type', 'start_date', 'end_date']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Parse datetime strings
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        # Create new promotion
        new_promotion = Promotion(
            title=data['title'],
            description=data.get('description'),
            promo_type=data['promo_type'],
            discount_percentage=data.get('discount_percentage'),
            discount_amount=data.get('discount_amount'),
            min_order_amount=data.get('min_order_amount'),
            max_discount=data.get('max_discount'),
            promo_code=data.get('promo_code'),
            start_date=start_date,
            end_date=end_date,
            usage_limit=data.get('usage_limit'),
            geo_targeted=data.get('geo_targeted', False),
            target_cities=data.get('target_cities')
        )
        
        db.session.add(new_promotion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_promotion.to_dict(),
            'message': 'Promotion created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@promotions_bp.route('/<promo_id>/use', methods=['POST'])
def use_promotion(promo_id):
    """Mark promotion as used"""
    try:
        promotion = Promotion.query.get(promo_id)
        if not promotion:
            return jsonify({
                'success': False,
                'error': 'Promotion not found'
            }), 404
        
        # Increment usage count
        promotion.usage_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'usage_count': promotion.usage_count,
                'remaining_uses': promotion.usage_limit - promotion.usage_count if promotion.usage_limit else None
            },
            'message': 'Promotion usage recorded'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







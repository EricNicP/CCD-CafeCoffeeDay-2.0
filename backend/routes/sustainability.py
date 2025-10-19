"""
Sustainability API Routes
Handles sustainability tracking, green points, and farm-to-cup information
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
from ..models.coffee import db, Coffee, User, Order

sustainability_bp = Blueprint('sustainability', __name__)

@sustainability_bp.route('/coffee/<coffee_id>/sustainability', methods=['GET'])
def get_coffee_sustainability(coffee_id):
    """Get sustainability information for a coffee item"""
    try:
        coffee = Coffee.query.get(coffee_id)
        if not coffee:
            return jsonify({
                'success': False,
                'error': 'Coffee item not found'
            }), 404
        
        sustainability_data = {
            'coffee_id': coffee.id,
            'name': coffee.name,
            'sustainability_rating': coffee.sustainability_rating,
            'carbon_footprint': coffee.carbon_footprint,
            'fair_trade': coffee.fair_trade,
            'organic': coffee.organic,
            'farm_info': coffee.farm_info,
            'ingredients': coffee.ingredients,
            'dietary_tags': coffee.dietary_tags,
            'allergens': coffee.allergens
        }
        
        return jsonify({
            'success': True,
            'data': sustainability_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sustainability_bp.route('/farm-to-cup', methods=['GET'])
def get_farm_to_cup_info():
    """Get farm-to-cup information for all coffee items"""
    try:
        coffees = Coffee.query.filter(Coffee.farm_info.isnot(None)).all()
        
        farm_to_cup_data = []
        for coffee in coffees:
            farm_to_cup_data.append({
                'coffee_id': coffee.id,
                'name': coffee.name,
                'farm_info': coffee.farm_info,
                'sustainability_rating': coffee.sustainability_rating,
                'fair_trade': coffee.fair_trade,
                'organic': coffee.organic,
                'carbon_footprint': coffee.carbon_footprint
            })
        
        return jsonify({
            'success': True,
            'data': farm_to_cup_data,
            'count': len(farm_to_cup_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sustainability_bp.route('/green-points/<user_id>', methods=['GET'])
def get_user_green_points(user_id):
    """Get user's green points for eco-friendly actions"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Calculate green points based on eco-friendly orders
        eco_friendly_orders = Order.query.filter_by(customer_id=user_id).join(Coffee).filter(
            Coffee.organic == True
        ).count()
        
        green_points = eco_friendly_orders * 10  # 10 points per eco-friendly order
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user.id,
                'green_points': green_points,
                'eco_friendly_orders': eco_friendly_orders,
                'sustainability_level': 'Bronze' if green_points < 100 else 'Silver' if green_points < 500 else 'Gold'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sustainability_bp.route('/green-points/<user_id>/earn', methods=['POST'])
def earn_green_points(user_id):
    """Earn green points for eco-friendly actions"""
    try:
        data = request.get_json()
        action = data.get('action')  # 'own_cup', 'eco_packaging', 'organic_order'
        points = data.get('points', 0)
        
        if not action:
            return jsonify({
                'success': False,
                'error': 'Action is required'
            }), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Calculate points based on action
        if action == 'own_cup':
            points = 20
        elif action == 'eco_packaging':
            points = 15
        elif action == 'organic_order':
            points = 10
        
        # Update user's loyalty points (green points are part of loyalty system)
        user.loyalty_points += points
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user.id,
                'action': action,
                'points_earned': points,
                'total_loyalty_points': user.loyalty_points
            },
            'message': f'{points} green points earned for {action}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sustainability_bp.route('/impact', methods=['GET'])
def get_sustainability_impact():
    """Get overall sustainability impact metrics"""
    try:
        # Calculate sustainability metrics
        total_organic_orders = db.session.query(Order).join(Coffee).filter(
            Coffee.organic == True
        ).count()
        
        total_fair_trade_orders = db.session.query(Order).join(Coffee).filter(
            Coffee.fair_trade == True
        ).count()
        
        total_co2_saved = db.session.query(db.func.sum(Coffee.carbon_footprint)).join(Order).scalar() or 0
        
        avg_sustainability_rating = db.session.query(db.func.avg(Coffee.sustainability_rating)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_organic_orders': total_organic_orders,
                'total_fair_trade_orders': total_fair_trade_orders,
                'total_co2_saved': round(total_co2_saved, 2),
                'average_sustainability_rating': round(avg_sustainability_rating, 2),
                'eco_friendly_percentage': round((total_organic_orders / max(total_organic_orders + total_fair_trade_orders, 1)) * 100, 2)
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sustainability_bp.route('/practices', methods=['GET'])
def get_eco_practices():
    """Get information about eco-friendly practices"""
    try:
        practices = [
            {
                'id': 'own_cup',
                'name': 'Bring Your Own Cup',
                'description': 'Bring your own reusable cup and get 20 green points',
                'points': 20,
                'impact': 'Reduces single-use cup waste'
            },
            {
                'id': 'eco_packaging',
                'name': 'Eco-Friendly Packaging',
                'description': 'Choose eco-friendly packaging options',
                'points': 15,
                'impact': 'Reduces plastic waste'
            },
            {
                'id': 'organic_order',
                'name': 'Organic Coffee',
                'description': 'Order organic and fair-trade coffee',
                'points': 10,
                'impact': 'Supports sustainable farming'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': practices
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







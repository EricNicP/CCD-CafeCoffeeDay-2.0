"""
Loyalty & Rewards API Routes
Handles loyalty points, rewards, and gamification
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
from ..models.coffee import db, User, LoyaltyTransaction, Order

loyalty_bp = Blueprint('loyalty', __name__)

@loyalty_bp.route('/<user_id>/points', methods=['GET'])
def get_user_points(user_id):
    """Get user's loyalty points and level"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Calculate loyalty level based on points
        level_thresholds = {
            'Bronze': 0,
            'Silver': 500,
            'Gold': 1500,
            'Platinum': 3000
        }
        
        current_level = 'Bronze'
        for level, threshold in level_thresholds.items():
            if user.loyalty_points >= threshold:
                current_level = level
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user.id,
                'points': user.loyalty_points,
                'level': current_level,
                'total_orders': user.total_orders,
                'total_spent': user.total_spent,
                'streak_days': user.streak_days,
                'next_level_points': level_thresholds.get('Silver', 500) - user.loyalty_points if current_level == 'Bronze' else None
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@loyalty_bp.route('/<user_id>/transactions', methods=['GET'])
def get_loyalty_transactions(user_id):
    """Get user's loyalty transaction history"""
    try:
        transactions = LoyaltyTransaction.query.filter_by(user_id=user_id).order_by(LoyaltyTransaction.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [transaction.to_dict() for transaction in transactions],
            'count': len(transactions)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@loyalty_bp.route('/<user_id>/earn', methods=['POST'])
def earn_points(user_id):
    """Earn loyalty points for user"""
    try:
        data = request.get_json()
        points = data.get('points', 0)
        description = data.get('description', 'Points earned')
        order_id = data.get('order_id')
        
        if points <= 0:
            return jsonify({
                'success': False,
                'error': 'Points must be positive'
            }), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Create loyalty transaction
        transaction = LoyaltyTransaction(
            user_id=user_id,
            transaction_type='earned',
            points=points,
            description=description,
            order_id=order_id
        )
        
        # Update user points
        user.loyalty_points += points
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': transaction.to_dict(),
            'message': f'{points} points earned successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@loyalty_bp.route('/<user_id>/redeem', methods=['POST'])
def redeem_points(user_id):
    """Redeem loyalty points"""
    try:
        data = request.get_json()
        points_to_redeem = data.get('points', 0)
        description = data.get('description', 'Points redeemed')
        
        if points_to_redeem <= 0:
            return jsonify({
                'success': False,
                'error': 'Points must be positive'
            }), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if user.loyalty_points < points_to_redeem:
            return jsonify({
                'success': False,
                'error': 'Insufficient points'
            }), 400
        
        # Create loyalty transaction
        transaction = LoyaltyTransaction(
            user_id=user_id,
            transaction_type='redeemed',
            points=-points_to_redeem,
            description=description
        )
        
        # Update user points
        user.loyalty_points -= points_to_redeem
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': transaction.to_dict(),
            'message': f'{points_to_redeem} points redeemed successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@loyalty_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get loyalty points leaderboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get top users by loyalty points
        top_users = User.query.order_by(User.loyalty_points.desc()).limit(limit).all()
        
        leaderboard = []
        for i, user in enumerate(top_users, 1):
            leaderboard.append({
                'rank': i,
                'user_id': user.id,
                'username': user.username,
                'points': user.loyalty_points,
                'level': user.loyalty_level,
                'total_orders': user.total_orders
            })
        
        return jsonify({
            'success': True,
            'data': leaderboard,
            'count': len(leaderboard)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@loyalty_bp.route('/<user_id>/streak', methods=['POST'])
def update_streak(user_id):
    """Update user's streak based on order activity"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        today = datetime.now().date()
        last_order_date = user.last_order_date.date() if user.last_order_date else None
        
        if last_order_date:
            days_diff = (today - last_order_date).days
            
            if days_diff == 1:  # Consecutive day
                user.streak_days += 1
            elif days_diff > 1:  # Streak broken
                user.streak_days = 1
            # If days_diff == 0, same day, no change
        else:
            user.streak_days = 1
        
        user.last_order_date = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'streak_days': user.streak_days,
                'last_order_date': user.last_order_date.isoformat()
            },
            'message': 'Streak updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







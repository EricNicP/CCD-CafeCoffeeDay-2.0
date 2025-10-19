"""
Events API Routes
Handles café events, bookings, and community features
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
from ..models.coffee import db, Event, Cafe

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def get_events():
    """Get all events with filtering"""
    try:
        # Filter parameters
        cafe_id = request.args.get('cafe_id')
        event_type = request.args.get('type')
        upcoming_only = request.args.get('upcoming', 'true').lower() == 'true'
        
        query = Event.query.filter_by(is_active=True)
        
        if cafe_id:
            query = query.filter_by(cafe_id=cafe_id)
        if event_type:
            query = query.filter_by(event_type=event_type)
        if upcoming_only:
            query = query.filter(Event.start_time > datetime.now())
        
        events = query.order_by(Event.start_time.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [event.to_dict() for event in events],
            'count': len(events)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@events_bp.route('/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get specific event by ID"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@events_bp.route('/', methods=['POST'])
def create_event():
    """Create new event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['cafe_id', 'title', 'event_type', 'start_time', 'end_time']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Parse datetime strings
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        
        # Create new event
        new_event = Event(
            cafe_id=data['cafe_id'],
            title=data['title'],
            description=data.get('description'),
            event_type=data['event_type'],
            start_time=start_time,
            end_time=end_time,
            max_capacity=data.get('max_capacity'),
            price=data.get('price', 0.0),
            image_url=data.get('image_url')
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_event.to_dict(),
            'message': 'Event created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@events_bp.route('/<event_id>/book', methods=['POST'])
def book_event(event_id):
    """Book an event"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        tickets = data.get('tickets', 1)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        if not event.is_active:
            return jsonify({
                'success': False,
                'error': 'Event is not active'
            }), 400
        
        if event.start_time < datetime.now():
            return jsonify({
                'success': False,
                'error': 'Event has already started'
            }), 400
        
        # Check capacity
        if event.max_capacity and (event.current_bookings + tickets) > event.max_capacity:
            return jsonify({
                'success': False,
                'error': 'Event is fully booked'
            }), 400
        
        # Update bookings
        event.current_bookings += tickets
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'event_id': event.id,
                'user_id': user_id,
                'tickets': tickets,
                'total_cost': event.price * tickets,
                'remaining_capacity': event.max_capacity - event.current_bookings if event.max_capacity else None
            },
            'message': 'Event booked successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@events_bp.route('/types', methods=['GET'])
def get_event_types():
    """Get all available event types"""
    try:
        event_types = db.session.query(Event.event_type).distinct().all()
        types = [event_type[0] for event_type in event_types]
        
        return jsonify({
            'success': True,
            'data': types
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







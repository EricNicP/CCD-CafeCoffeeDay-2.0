"""
Café Locations API Routes
Handles café location management and filtering
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
from models.coffee import db, Cafe

cafes_bp = Blueprint('cafes', __name__)

@cafes_bp.route('/', methods=['GET'])
def get_cafes():
    """Get all café locations with filtering"""
    try:
        # Filter parameters
        city = request.args.get('city')
        wifi = request.args.get('wifi', '').lower()
        parking = request.args.get('parking', '').lower()
        open_mic = request.args.get('open_mic', '').lower()
        coworking = request.args.get('coworking', '').lower()
        
        query = Cafe.query
        
        if city:
            query = query.filter(Cafe.city.ilike(f'%{city}%'))
        if wifi == 'true':
            query = query.filter(Cafe.wifi_available == True)
        if parking == 'true':
            query = query.filter(Cafe.parking_available == True)
        if open_mic == 'true':
            query = query.filter(Cafe.open_mic_nights == True)
        if coworking == 'true':
            query = query.filter(Cafe.coworking_friendly == True)
        
        cafes = query.all()
        
        return jsonify({
            'success': True,
            'data': [cafe.to_dict() for cafe in cafes],
            'count': len(cafes)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cafes_bp.route('/<cafe_id>', methods=['GET'])
def get_cafe(cafe_id):
    """Get specific café by ID"""
    try:
        cafe = Cafe.query.get(cafe_id)
        if not cafe:
            return jsonify({
                'success': False,
                'error': 'Café not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cafe.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cafes_bp.route('/nearby', methods=['GET'])
def get_nearby_cafes():
    """Get nearby cafés based on coordinates"""
    try:
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lng', type=float)
        radius = request.args.get('radius', 10, type=float)  # km
        
        if not latitude or not longitude:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        # Simple distance calculation (for production, use proper geospatial queries)
        cafes = Cafe.query.all()
        nearby_cafes = []
        
        for cafe in cafes:
            if cafe.latitude and cafe.longitude:
                # Calculate distance (simplified)
                lat_diff = abs(cafe.latitude - latitude)
                lng_diff = abs(cafe.longitude - longitude)
                distance = (lat_diff + lng_diff) * 111  # Rough km conversion
                
                if distance <= radius:
                    cafe_data = cafe.to_dict()
                    cafe_data['distance'] = round(distance, 2)
                    nearby_cafes.append(cafe_data)
        
        return jsonify({
            'success': True,
            'data': nearby_cafes,
            'count': len(nearby_cafes)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cafes_bp.route('/', methods=['POST'])
def create_cafe():
    """Create new café location"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'city', 'state', 'pincode']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new café
        new_cafe = Cafe(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            phone=data.get('phone'),
            email=data.get('email'),
            wifi_available=data.get('wifi_available', True),
            parking_available=data.get('parking_available', False),
            open_mic_nights=data.get('open_mic_nights', False),
            coworking_friendly=data.get('coworking_friendly', False),
            ambience_rating=data.get('ambience_rating', 0.0)
        )
        
        db.session.add(new_cafe)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_cafe.to_dict(),
            'message': 'Café created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500









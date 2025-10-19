"""
Coffee Shop Database Models
SQLAlchemy models for CCD 2.0 - Enhanced with all features
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import json

db = SQLAlchemy()

class User(db.Model):
    """Enhanced User model for customer management with personalization"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Enhanced personalization fields
    dietary_preferences = db.Column(db.Text, nullable=True)  # JSON: vegan, gluten-free, etc.
    favorite_items = db.Column(db.Text, nullable=True)  # JSON: favorite coffee IDs
    customizations = db.Column(db.Text, nullable=True)  # JSON: saved customizations
    birthday = db.Column(db.Date, nullable=True)
    student_id = db.Column(db.String(50), nullable=True)
    referral_code = db.Column(db.String(20), unique=True, nullable=True)
    referred_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Loyalty & Rewards
    loyalty_points = db.Column(db.Integer, default=0)
    loyalty_level = db.Column(db.String(20), default='Bronze')  # Bronze, Silver, Gold, Platinum
    total_orders = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    streak_days = db.Column(db.Integer, default=0)
    last_order_date = db.Column(db.DateTime, nullable=True)
    
    # Preferences
    preferred_cafes = db.Column(db.Text, nullable=True)  # JSON: preferred café IDs
    notification_preferences = db.Column(db.Text, nullable=True)  # JSON: notification settings
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    favorites = db.relationship('UserFavorite', backref='user', lazy=True)
    loyalty_transactions = db.relationship('LoyaltyTransaction', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class Coffee(db.Model):
    """Enhanced Coffee/Menu item model with real-time stock and dietary info"""
    __tablename__ = 'coffees'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # coffee, pastry, beverage
    size = db.Column(db.String(20), default='regular')
    available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Enhanced features
    stock_quantity = db.Column(db.Integer, default=100)  # Real-time stock tracking
    min_stock_level = db.Column(db.Integer, default=10)
    preparation_time = db.Column(db.Integer, default=5)  # Minutes to prepare
    calories = db.Column(db.Integer, nullable=True)
    dietary_tags = db.Column(db.Text, nullable=True)  # JSON: vegan, gluten-free, sugar-free, etc.
    allergens = db.Column(db.Text, nullable=True)  # JSON: allergen information
    ingredients = db.Column(db.Text, nullable=True)  # JSON: ingredient list
    customization_options = db.Column(db.Text, nullable=True)  # JSON: available customizations
    popularity_score = db.Column(db.Float, default=0.0)  # For recommendations
    seasonal = db.Column(db.Boolean, default=False)
    seasonal_start = db.Column(db.Date, nullable=True)
    seasonal_end = db.Column(db.Date, nullable=True)
    
    # Sustainability info
    sustainability_rating = db.Column(db.Float, nullable=True)  # 1-5 stars
    carbon_footprint = db.Column(db.Float, nullable=True)  # CO2 emissions
    fair_trade = db.Column(db.Boolean, default=False)
    organic = db.Column(db.Boolean, default=False)
    farm_info = db.Column(db.Text, nullable=True)  # Farm-to-cup story
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='coffee_item', lazy=True)
    reviews = db.relationship('Review', backref='coffee', lazy=True)
    favorites = db.relationship('UserFavorite', backref='coffee', lazy=True)
    stock_updates = db.relationship('StockUpdate', backref='coffee', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'size': self.size,
            'available': self.available,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Order(db.Model):
    """Enhanced Order model with delivery and real-time tracking"""
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, ready, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Enhanced ordering features
    order_type = db.Column(db.String(20), default='dine_in')  # dine_in, takeaway, delivery
    cafe_id = db.Column(db.String(36), nullable=True)  # Which café location
    table_number = db.Column(db.String(10), nullable=True)  # For dine-in orders
    qr_code = db.Column(db.String(100), nullable=True)  # QR code for table ordering
    
    # Delivery information
    delivery_address = db.Column(db.Text, nullable=True)
    delivery_instructions = db.Column(db.Text, nullable=True)
    delivery_fee = db.Column(db.Float, default=0.0)
    estimated_delivery_time = db.Column(db.DateTime, nullable=True)
    actual_delivery_time = db.Column(db.DateTime, nullable=True)
    delivery_partner = db.Column(db.String(50), nullable=True)  # Swiggy, Zomato, CCD delivery
    
    # Real-time tracking
    preparation_start_time = db.Column(db.DateTime, nullable=True)
    preparation_end_time = db.Column(db.DateTime, nullable=True)
    ready_time = db.Column(db.DateTime, nullable=True)
    estimated_ready_time = db.Column(db.DateTime, nullable=True)
    
    # Payment and loyalty
    payment_method = db.Column(db.String(20), nullable=True)  # UPI, card, wallet, cash
    payment_status = db.Column(db.String(20), default='pending')
    loyalty_points_earned = db.Column(db.Integer, default=0)
    loyalty_points_used = db.Column(db.Integer, default=0)
    discount_applied = db.Column(db.Float, default=0.0)
    promo_code = db.Column(db.String(20), nullable=True)
    
    # Special features
    is_reorder = db.Column(db.Boolean, default=False)  # Quick reorder
    original_order_id = db.Column(db.String(36), nullable=True)  # For reorders
    special_occasion = db.Column(db.String(50), nullable=True)  # birthday, anniversary, etc.
    customization_notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    tracking_updates = db.relationship('OrderTracking', backref='order', lazy=True)
    feedback = db.relationship('OrderFeedback', backref='order', lazy=True, uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    """Order item model for individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    coffee_id = db.Column(db.String(36), db.ForeignKey('coffees.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)  # Price at time of order
    special_instructions = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'coffee_id': self.coffee_id,
            'quantity': self.quantity,
            'price': self.price,
            'special_instructions': self.special_instructions,
            'coffee_name': self.coffee_item.name if self.coffee_item else None
        }

# New models for enhanced features

class Cafe(db.Model):
    """Café locations model"""
    __tablename__ = 'cafes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    
    # Café features
    wifi_available = db.Column(db.Boolean, default=True)
    parking_available = db.Column(db.Boolean, default=False)
    open_mic_nights = db.Column(db.Boolean, default=False)
    coworking_friendly = db.Column(db.Boolean, default=False)
    ambience_rating = db.Column(db.Float, default=0.0)
    
    # Operating hours
    opening_time = db.Column(db.Time, nullable=True)
    closing_time = db.Column(db.Time, nullable=True)
    is_24_hours = db.Column(db.Boolean, default=False)
    
    # Relationships
    orders = db.relationship('Order', backref='cafe_location', lazy=True)
    events = db.relationship('Event', backref='cafe', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'email': self.email,
            'wifi_available': self.wifi_available,
            'parking_available': self.parking_available,
            'open_mic_nights': self.open_mic_nights,
            'coworking_friendly': self.coworking_friendly,
            'ambience_rating': self.ambience_rating
        }

class UserFavorite(db.Model):
    """User favorites model"""
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    coffee_id = db.Column(db.String(36), db.ForeignKey('coffees.id'), nullable=False)
    customizations = db.Column(db.Text, nullable=True)  # JSON: saved customizations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'coffee_id': self.coffee_id,
            'customizations': self.customizations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LoyaltyTransaction(db.Model):
    """Loyalty points transactions"""
    __tablename__ = 'loyalty_transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # earned, redeemed, bonus, penalty
    points = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'points': self.points,
            'description': self.description,
            'order_id': self.order_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Review(db.Model):
    """User reviews for coffee items"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    coffee_id = db.Column(db.String(36), db.ForeignKey('coffees.id'), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text, nullable=True)
    photos = db.Column(db.Text, nullable=True)  # JSON: photo URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'coffee_id': self.coffee_id,
            'order_id': self.order_id,
            'rating': self.rating,
            'review_text': self.review_text,
            'photos': self.photos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StockUpdate(db.Model):
    """Real-time stock updates"""
    __tablename__ = 'stock_updates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    coffee_id = db.Column(db.String(36), db.ForeignKey('coffees.id'), nullable=False)
    cafe_id = db.Column(db.String(36), db.ForeignKey('cafes.id'), nullable=True)
    quantity_change = db.Column(db.Integer, nullable=False)  # + or - quantity
    new_stock_level = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100), nullable=True)  # sale, restock, waste, etc.
    updated_by = db.Column(db.String(36), nullable=True)  # staff member ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'coffee_id': self.coffee_id,
            'cafe_id': self.cafe_id,
            'quantity_change': self.quantity_change,
            'new_stock_level': self.new_stock_level,
            'reason': self.reason,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OrderTracking(db.Model):
    """Real-time order tracking updates"""
    __tablename__ = 'order_tracking'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=True)
    estimated_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'status': self.status,
            'message': self.message,
            'estimated_time': self.estimated_time.isoformat() if self.estimated_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OrderFeedback(db.Model):
    """Order feedback and ratings"""
    __tablename__ = 'order_feedback'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    food_quality_rating = db.Column(db.Integer, nullable=True)
    service_rating = db.Column(db.Integer, nullable=True)
    ambience_rating = db.Column(db.Integer, nullable=True)
    feedback_text = db.Column(db.Text, nullable=True)
    photos = db.Column(db.Text, nullable=True)  # JSON: photo URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'overall_rating': self.overall_rating,
            'food_quality_rating': self.food_quality_rating,
            'service_rating': self.service_rating,
            'ambience_rating': self.ambience_rating,
            'feedback_text': self.feedback_text,
            'photos': self.photos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Event(db.Model):
    """Café events and bookings"""
    __tablename__ = 'events'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cafe_id = db.Column(db.String(36), db.ForeignKey('cafes.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # poetry, music, brewflix, etc.
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=True)
    current_bookings = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cafe_id': self.cafe_id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_capacity': self.max_capacity,
            'current_bookings': self.current_bookings,
            'price': self.price,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Promotion(db.Model):
    """Marketing promotions and offers"""
    __tablename__ = 'promotions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    promo_type = db.Column(db.String(50), nullable=False)  # discount, free_item, loyalty_bonus
    discount_percentage = db.Column(db.Float, nullable=True)
    discount_amount = db.Column(db.Float, nullable=True)
    min_order_amount = db.Column(db.Float, nullable=True)
    max_discount = db.Column(db.Float, nullable=True)
    promo_code = db.Column(db.String(20), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    usage_limit = db.Column(db.Integer, nullable=True)
    usage_count = db.Column(db.Integer, default=0)
    geo_targeted = db.Column(db.Boolean, default=False)
    target_cities = db.Column(db.Text, nullable=True)  # JSON: target cities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'promo_type': self.promo_type,
            'discount_percentage': self.discount_percentage,
            'discount_amount': self.discount_amount,
            'min_order_amount': self.min_order_amount,
            'max_discount': self.max_discount,
            'promo_code': self.promo_code,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'geo_targeted': self.geo_targeted,
            'target_cities': self.target_cities,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Database initialization function
def init_db(app):
    """Initialize database with app context and enhanced sample data"""
    with app.app_context():
        db.create_all()
        
        # Create sample data if database is empty
        if Coffee.query.count() == 0:
            # Enhanced sample coffees with all new features
            sample_coffees = [
                Coffee(
                    name='Espresso',
                    description='Rich, full-bodied coffee with a thick layer of crema',
                    price=3.50,
                    category='coffee',
                    size='small',
                    stock_quantity=50,
                    preparation_time=3,
                    calories=5,
                    dietary_tags='["vegan", "sugar-free"]',
                    allergens='[]',
                    ingredients='["coffee beans", "water"]',
                    sustainability_rating=4.5,
                    fair_trade=True,
                    organic=True,
                    farm_info='Sourced from sustainable farms in Colombia'
                ),
                Coffee(
                    name='Cappuccino',
                    description='Espresso with steamed milk and foam',
                    price=4.50,
                    category='coffee',
                    size='medium',
                    stock_quantity=30,
                    preparation_time=5,
                    calories=120,
                    dietary_tags='["vegetarian"]',
                    allergens='["dairy"]',
                    ingredients='["coffee beans", "milk", "foam"]',
                    sustainability_rating=4.0,
                    fair_trade=True,
                    organic=False
                ),
                Coffee(
                    name='Latte',
                    description='Espresso with steamed milk and a small amount of foam',
                    price=5.00,
                    category='coffee',
                    size='large',
                    stock_quantity=25,
                    preparation_time=6,
                    calories=150,
                    dietary_tags='["vegetarian"]',
                    allergens='["dairy"]',
                    ingredients='["coffee beans", "milk"]',
                    sustainability_rating=4.0,
                    fair_trade=True,
                    organic=False
                ),
                Coffee(
                    name='Croissant',
                    description='Buttery, flaky pastry perfect with coffee',
                    price=3.00,
                    category='pastry',
                    size='regular',
                    stock_quantity=20,
                    preparation_time=2,
                    calories=200,
                    dietary_tags='["vegetarian"]',
                    allergens='["gluten", "dairy", "eggs"]',
                    ingredients='["flour", "butter", "eggs", "yeast"]',
                    sustainability_rating=3.5,
                    fair_trade=False,
                    organic=False
                ),
                Coffee(
                    name='Vegan Latte',
                    description='Plant-based latte with oat milk',
                    price=5.50,
                    category='coffee',
                    size='medium',
                    stock_quantity=15,
                    preparation_time=6,
                    calories=100,
                    dietary_tags='["vegan", "dairy-free"]',
                    allergens='[]',
                    ingredients='["coffee beans", "oat milk"]',
                    sustainability_rating=4.8,
                    fair_trade=True,
                    organic=True,
                    farm_info='Organic coffee with sustainable oat milk'
                )
            ]
            
            for coffee in sample_coffees:
                db.session.add(coffee)
            
            # Create sample café locations
            sample_cafes = [
                Cafe(
                    name='CCD Downtown',
                    address='123 Main Street, Downtown',
                    city='Mumbai',
                    state='Maharashtra',
                    pincode='400001',
                    latitude=19.0760,
                    longitude=72.8777,
                    phone='+91-9876543210',
                    email='downtown@ccd.com',
                    wifi_available=True,
                    parking_available=True,
                    open_mic_nights=True,
                    coworking_friendly=True,
                    ambience_rating=4.5,
                    opening_time=datetime.strptime('06:00', '%H:%M').time(),
                    closing_time=datetime.strptime('23:00', '%H:%M').time()
                ),
                Cafe(
                    name='CCD Airport',
                    address='Terminal 2, Mumbai Airport',
                    city='Mumbai',
                    state='Maharashtra',
                    pincode='400099',
                    latitude=19.0896,
                    longitude=72.8656,
                    phone='+91-9876543211',
                    email='airport@ccd.com',
                    wifi_available=True,
                    parking_available=False,
                    open_mic_nights=False,
                    coworking_friendly=False,
                    ambience_rating=4.0,
                    is_24_hours=True
                )
            ]
            
            for cafe in sample_cafes:
                db.session.add(cafe)
            
            # Create sample events
            sample_events = [
                Event(
                    cafe_id=sample_cafes[0].id,
                    title='Poetry Slam Night',
                    description='Join us for an evening of spoken word poetry',
                    event_type='poetry',
                    start_time=datetime.now() + timedelta(days=7, hours=19),
                    end_time=datetime.now() + timedelta(days=7, hours=22),
                    max_capacity=50,
                    price=100.0,
                    image_url='/static/images/poetry-slam.jpg'
                ),
                Event(
                    cafe_id=sample_cafes[0].id,
                    title='Brewflix Movie Night',
                    description='Watch classic movies while enjoying your favorite coffee',
                    event_type='brewflix',
                    start_time=datetime.now() + timedelta(days=14, hours=20),
                    end_time=datetime.now() + timedelta(days=14, hours=23),
                    max_capacity=30,
                    price=150.0,
                    image_url='/static/images/movie-night.jpg'
                )
            ]
            
            for event in sample_events:
                db.session.add(event)
            
            # Create sample promotions
            sample_promotions = [
                Promotion(
                    title='Happy Hour Coffee',
                    description='Get any coffee for just ₹49 during happy hours',
                    promo_type='discount',
                    discount_percentage=30.0,
                    min_order_amount=100.0,
                    max_discount=50.0,
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=30),
                    geo_targeted=True,
                    target_cities='["Mumbai", "Delhi", "Bangalore"]'
                ),
                Promotion(
                    title='Student Special',
                    description='20% off for students with valid ID',
                    promo_type='discount',
                    discount_percentage=20.0,
                    min_order_amount=50.0,
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=365)
                )
            ]
            
            for promotion in sample_promotions:
                db.session.add(promotion)
            
            db.session.commit()
            print("Enhanced sample data created successfully!")
            print(f"Created {len(sample_coffees)} coffee items")
            print(f"Created {len(sample_cafes)} café locations")
            print(f"Created {len(sample_events)} events")
            print(f"Created {len(sample_promotions)} promotions")

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeSection, setActiveSection] = useState('home');
  const [menu, setMenu] = useState([]);
  const [cafes, setCafes] = useState([]);
  const [events, setEvents] = useState([]);
  const [promotions, setPromotions] = useState([]);
  const [cart, setCart] = useState([]);
  const [orders, setOrders] = useState([]);
  const [user, setUser] = useState({ id: 1, name: 'Coffee Lover', points: 0 });
  const [loyaltyPoints, setLoyaltyPoints] = useState(0);
  const [loading, setLoading] = useState(true);
  const [backendConnected, setBackendConnected] = useState(false);

  // Fetch data from backend API
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      console.log('🔄 Fetching data from backend...');
      
      // Test backend connection first
      const healthResponse = await fetch('/api/health');
      if (healthResponse.ok) {
        setBackendConnected(true);
        console.log('✅ Backend connected!');
      }

      // Fetch menu from backend
      const menuResponse = await fetch('/api/menu');
      if (menuResponse.ok) {
        const menuData = await menuResponse.json();
        setMenu(menuData.data || menuData);
        console.log('✅ Menu loaded:', menuData.data?.length || menuData.length, 'items');
      }

      // Fetch cafes
      const cafesResponse = await fetch('/api/cafes');
      if (cafesResponse.ok) {
        const cafesData = await cafesResponse.json();
        setCafes(cafesData.data || cafesData);
        console.log('✅ Cafes loaded:', cafesData.data?.length || cafesData.length, 'locations');
      }

      // Fetch events
      const eventsResponse = await fetch('/api/events');
      if (eventsResponse.ok) {
        const eventsData = await eventsResponse.json();
        setEvents(eventsData.data || eventsData);
        console.log('✅ Events loaded:', eventsData.data?.length || eventsData.length, 'events');
      }

      // Fetch promotions
      const promotionsResponse = await fetch('/api/promotions');
      if (promotionsResponse.ok) {
        const promotionsData = await promotionsResponse.json();
        setPromotions(promotionsData.data || promotionsData);
        console.log('✅ Promotions loaded:', promotionsData.data?.length || promotionsData.length, 'offers');
      }

    } catch (error) {
      console.log('❌ Backend not connected, using mock data');
      setBackendConnected(false);
      
      // Fallback to mock data
      setMenu([
        { id: 1, name: 'Espresso', price: 2.50, stock_quantity: 50, category: 'Coffee', sustainability_rating: 4.5, fair_trade: true, organic: true, description: 'Rich, bold espresso shot' },
        { id: 2, name: 'Cappuccino', price: 3.50, stock_quantity: 30, category: 'Coffee', sustainability_rating: 4.2, fair_trade: true, organic: false, description: 'Perfect balance of espresso, steamed milk, and foam' },
        { id: 3, name: 'Latte', price: 4.00, stock_quantity: 25, category: 'Coffee', sustainability_rating: 4.0, fair_trade: true, organic: true, description: 'Smooth and creamy with a hint of sweetness' },
        { id: 4, name: 'Croissant', price: 2.00, stock_quantity: 15, category: 'Food', sustainability_rating: 3.8, fair_trade: false, organic: true, description: 'Buttery, flaky pastry' },
        { id: 5, name: 'Blueberry Muffin', price: 2.50, stock_quantity: 20, category: 'Food', sustainability_rating: 3.5, fair_trade: false, organic: false, description: 'Fresh baked with real blueberries' }
      ]);
      setCafes([
        { id: 1, name: 'Downtown Café', address: '123 Main Street', city: 'Downtown', features: ['WiFi', 'Outdoor Seating', 'Live Music', 'Parking'], wifi_available: true, parking_available: true },
        { id: 2, name: 'University Branch', address: '456 Campus Avenue', city: 'University District', features: ['Student Discount', 'Study Area', 'Quick Service', 'WiFi'], wifi_available: true, parking_available: false },
        { id: 3, name: 'Beachside Café', address: '789 Ocean Drive', city: 'Beachside', features: ['Ocean View', 'Outdoor Seating', 'Sunset Views', 'WiFi'], wifi_available: true, parking_available: true }
      ]);
      setEvents([
        { id: 1, title: 'Coffee Tasting Workshop', date: '2024-01-15', time: '14:00', description: 'Learn about different coffee beans and brewing methods', price: 25.00, max_participants: 20, current_participants: 12 },
        { id: 2, title: 'Live Music Night', date: '2024-01-20', time: '19:00', description: 'Local artists performing acoustic sets', price: 15.00, max_participants: 50, current_participants: 35 },
        { id: 3, title: 'Latte Art Class', date: '2024-01-25', time: '10:00', description: 'Learn to create beautiful latte art designs', price: 30.00, max_participants: 15, current_participants: 8 }
      ]);
      setPromotions([
        { id: 1, title: 'Student Discount', description: '20% off all items for students with valid ID', code: 'STUDENT20', discount_value: 20 },
        { id: 2, title: 'Happy Hour', description: '50% off all drinks from 3-5 PM', code: 'HAPPY50', discount_value: 50 },
        { id: 3, title: 'First Order Bonus', description: 'Get 100 bonus points on your first order', code: 'WELCOME100', discount_value: 100 }
      ]);
    }
    setLoading(false);
  };

  const addToCart = (item) => {
    if (item.stock_quantity > 0) {
      const existingItem = cart.find(cartItem => cartItem.id === item.id);
      if (existingItem) {
        setCart(cart.map(cartItem => 
          cartItem.id === item.id 
            ? { ...cartItem, quantity: cartItem.quantity + 1 }
            : cartItem
        ));
      } else {
        setCart([...cart, { ...item, quantity: 1 }]);
      }
      console.log('🛒 Added to cart:', item.name);
    }
  };

  const removeFromCart = (itemId) => {
    setCart(cart.filter(item => item.id !== itemId));
    console.log('🗑️ Removed from cart:', itemId);
  };

  const updateCartQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId);
    } else {
      setCart(cart.map(item => 
        item.id === itemId ? { ...item, quantity } : item
      ));
    }
  };

  const placeOrder = async () => {
    if (cart.length === 0) return;

    const orderData = {
      items: cart,
      total: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0),
      order_type: 'pickup',
      user_id: user.id
    };

    try {
      if (backendConnected) {
        const response = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(orderData)
        });
        
        if (response.ok) {
          const newOrder = await response.json();
          setOrders([...orders, newOrder.data || newOrder]);
          setLoyaltyPoints(prev => prev + Math.floor(newOrder.data?.total || newOrder.total));
          console.log('✅ Order placed via backend:', newOrder);
        }
      } else {
        // Fallback to local state
        const newOrder = {
          id: orders.length + 1,
          items: [...cart],
          total: orderData.total,
          status: 'Preparing',
          timestamp: new Date().toLocaleString(),
          loyalty_points_earned: Math.floor(orderData.total)
        };
        setOrders([...orders, newOrder]);
        setLoyaltyPoints(prev => prev + newOrder.loyalty_points_earned);
        console.log('✅ Order placed locally:', newOrder);
      }
      
      setCart([]);
      alert(`🎉 Order placed! Total: $${orderData.total.toFixed(2)}`);
    } catch (error) {
      console.error('❌ Order failed:', error);
      alert('❌ Order failed. Please try again.');
    }
  };

  const bookEvent = async (eventId) => {
    const event = events.find(e => e.id === eventId);
    if (!event) return;

    if (event.current_participants >= event.max_participants) {
      alert('❌ Event is fully booked!');
      return;
    }

    // Simulate booking
    alert(`🎫 Booked: ${event.title}\n📅 ${event.date} at ${event.time}\n💰 $${event.price}`);
    console.log('🎫 Event booked:', event.title);
  };

  const applyPromoCode = (code) => {
    const promo = promotions.find(p => p.code === code);
    if (promo) {
      alert(`🎉 Promo applied: ${promo.title}\n${promo.description}`);
      console.log('🎉 Promo applied:', promo.title);
    } else {
      alert('❌ Invalid promo code');
    }
  };

  const renderHome = () => (
    <div className="home-section">
      <div className="status-banner">
        {backendConnected ? (
          <div className="status-connected">✅ Connected to Backend API</div>
        ) : (
          <div className="status-offline">⚠️ Using Offline Mode (Mock Data)</div>
        )}
      </div>
      
      <h2>☕ Welcome to CCD 2.0 Coffee Shop</h2>
      <div className="stats">
        <div className="stat">
          <h3>{menu.length}</h3>
          <p>Menu Items</p>
        </div>
        <div className="stat">
          <h3>{cafes.length}</h3>
          <p>Café Locations</p>
        </div>
        <div className="stat">
          <h3>{orders.length}</h3>
          <p>Total Orders</p>
        </div>
        <div className="stat">
          <h3>{loyaltyPoints}</h3>
          <p>Loyalty Points</p>
        </div>
      </div>
      
      <div className="feature-highlights">
        <h3>🌟 Featured Features</h3>
        <div className="features-grid">
          <div className="feature-card">
            <h4>🌱 Sustainability</h4>
            <p>Fair trade, organic, and eco-friendly options</p>
          </div>
          <div className="feature-card">
            <h4>🎯 Loyalty Program</h4>
            <p>Earn points with every purchase</p>
          </div>
          <div className="feature-card">
            <h4>📱 Smart Ordering</h4>
            <p>Real-time stock and preparation tracking</p>
          </div>
          <div className="feature-card">
            <h4>🏪 Multiple Locations</h4>
            <p>Find cafés near you with unique features</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderMenu = () => (
    <div className="menu-section">
      <h2>☕ Menu</h2>
      <div className="menu-filters">
        <button className="filter-btn active">All</button>
        <button className="filter-btn">Coffee</button>
        <button className="filter-btn">Food</button>
        <button className="filter-btn">Organic</button>
        <button className="filter-btn">Fair Trade</button>
      </div>
      <div className="menu-grid">
        {menu.map(item => (
          <div key={item.id} className="menu-item">
            <div className="item-header">
              <h3>{item.name}</h3>
              <div className="sustainability-badges">
                {item.fair_trade && <span className="badge fair-trade">Fair Trade</span>}
                {item.organic && <span className="badge organic">Organic</span>}
              </div>
            </div>
            <p className="description">{item.description}</p>
            <p className="price">${item.price}</p>
            <p className="stock">Stock: {item.stock_quantity}</p>
            <p className="sustainability">🌱 Rating: {item.sustainability_rating}/5</p>
            <button 
              onClick={() => addToCart(item)} 
              disabled={item.stock_quantity === 0}
              className="add-btn"
            >
              {item.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCafes = () => (
    <div className="cafes-section">
      <h2>🏪 Find Our Cafés</h2>
      <div className="cafes-grid">
        {cafes.map(cafe => (
          <div key={cafe.id} className="cafe-card">
            <h3>{cafe.name}</h3>
            <p className="address">{cafe.address}</p>
            <p className="city">{cafe.city}</p>
            <div className="features">
              {cafe.open_mic_nights && <span className="feature-tag">🎤 Open Mic</span>}
              {cafe.coworking_friendly && <span className="feature-tag">💻 Co-working</span>}
              {cafe.is_24_hours && <span className="feature-tag">🌙 24/7</span>}
            </div>
            <div className="cafe-info">
              {cafe.wifi_available && <span title="WiFi Available" className="info-tag">📶 WiFi</span>}
              {cafe.parking_available && <span title="Parking Available" className="info-tag">🅿️ Parking</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderEvents = () => (
    <div className="events-section">
      <h2>🎉 Upcoming Events</h2>
      <div className="events-grid">
        {events.map(event => (
          <div key={event.id} className="event-card">
            <h3>{event.title}</h3>
            <p className="date">{new Date(event.start_time || event.date).toLocaleString()}</p>
            <p className="description">{event.description}</p>
            <p className="price">${event.price}</p>
            <p className="participants">{event.current_participants}/{event.max_participants} participants</p>
            <button 
              onClick={() => bookEvent(event.id)}
              disabled={event.current_participants >= event.max_participants}
              className="book-btn"
            >
              {event.current_participants >= event.max_participants ? 'Fully Booked' : 'Book Now'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPromotions = () => (
    <div className="promotions-section">
      <h2>🎁 Current Promotions</h2>
      <div className="promotions-grid">
        {promotions.map(promo => (
          <div key={promo.id} className="promo-card">
            <h3>{promo.title}</h3>
            <p>{promo.description}</p>
            <p className="code">Code: {promo.code}</p>
            <button 
              onClick={() => applyPromoCode(promo.code)}
              className="apply-btn"
            >
              Apply Code
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCart = () => (
    <div className="cart-section">
      <h2>🛒 Shopping Cart ({cart.length} items)</h2>
      {cart.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        <div>
          {cart.map((item, index) => (
            <div key={index} className="cart-item">
              <div className="cart-item-info">
                <span className="item-name">{item.name}</span>
                <span className="item-price">${item.price}</span>
              </div>
              <div className="cart-item-controls">
                <button onClick={() => updateCartQuantity(item.id, item.quantity - 1)}>-</button>
                <span className="quantity">{item.quantity}</span>
                <button onClick={() => updateCartQuantity(item.id, item.quantity + 1)}>+</button>
                <button onClick={() => removeFromCart(item.id)} className="remove-btn">🗑️</button>
              </div>
            </div>
          ))}
          <div className="cart-total">
            <strong>Total: ${cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2)}</strong>
          </div>
          <button onClick={placeOrder} className="order-btn">Place Order</button>
        </div>
      )}
    </div>
  );

  const renderOrders = () => (
    <div className="orders-section">
      <h2>📋 Order History</h2>
      {orders.length === 0 ? (
        <p>No orders yet</p>
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className="order-item">
              <h3>Order #{order.id}</h3>
              <p>Status: {order.status}</p>
              <p>Total: ${order.total.toFixed(2)}</p>
              <p>Time: {order.timestamp}</p>
              <div className="order-items">
                {order.items.map((item, index) => (
                  <span key={index}>{item.name} x{item.quantity}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  if (loading) {
    return <div className="loading">🔄 Loading CCD 2.0...</div>;
  }

  return (
    <div className="App">
      <nav className="navbar">
        <h1>☕ CCD 2.0 Coffee Shop</h1>
        <div className="nav-buttons">
          <button onClick={() => setActiveSection('home')} className={activeSection === 'home' ? 'active' : ''}>
            🏠 Home
          </button>
          <button onClick={() => setActiveSection('menu')} className={activeSection === 'menu' ? 'active' : ''}>
            ☕ Menu
          </button>
          <button onClick={() => setActiveSection('cafes')} className={activeSection === 'cafes' ? 'active' : ''}>
            🏪 Cafés
          </button>
          <button onClick={() => setActiveSection('events')} className={activeSection === 'events' ? 'active' : ''}>
            🎉 Events
          </button>
          <button onClick={() => setActiveSection('promotions')} className={activeSection === 'promotions' ? 'active' : ''}>
            🎁 Promotions
          </button>
          <button onClick={() => setActiveSection('cart')} className={activeSection === 'cart' ? 'active' : ''}>
            🛒 Cart ({cart.length})
          </button>
          <button onClick={() => setActiveSection('orders')} className={activeSection === 'orders' ? 'active' : ''}>
            📋 Orders
          </button>
        </div>
      </nav>

      <main className="main-content">
        {activeSection === 'home' && renderHome()}
        {activeSection === 'menu' && renderMenu()}
        {activeSection === 'cafes' && renderCafes()}
        {activeSection === 'events' && renderEvents()}
        {activeSection === 'promotions' && renderPromotions()}
        {activeSection === 'cart' && renderCart()}
        {activeSection === 'orders' && renderOrders()}
      </main>
    </div>
  );
}

export default App;
    <Router>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/menu" element={<MenuPage />} />
            <Route path="/order" element={<OrderPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import './ProfilePage.css';

const ProfilePage = () => {
  const [user, setUser] = useState({
    id: '1',
    username: 'john_doe',
    email: 'john@example.com',
    full_name: 'John Doe',
    phone: '+1234567890',
    address: '123 Main St, City, State',
    created_at: '2024-01-01T00:00:00Z',
    last_login: '2024-01-15T10:30:00Z',
    is_active: true
  });
  
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockOrders = [
        {
          id: '1',
          items: [
            { name: 'Espresso', quantity: 2, price: 3.50 },
            { name: 'Cappuccino', quantity: 1, price: 4.50 }
          ],
          total: 11.50,
          status: 'completed',
          created_at: '2024-01-15T10:30:00Z'
        },
        {
          id: '2',
          items: [
            { name: 'Latte', quantity: 1, price: 5.00 },
            { name: 'Croissant', quantity: 2, price: 3.00 }
          ],
          total: 11.00,
          status: 'pending',
          created_at: '2024-01-14T15:45:00Z'
        }
      ];
      setOrders(mockOrders);
      setLoading(false);
    }, 1000);
  }, []);

  const handleUpdateProfile = (e) => {
    e.preventDefault();
    // TODO: Update profile via API
    console.log('Profile updated:', user);
    alert('Profile updated successfully!');
  };

  const handleInputChange = (field, value) => {
    setUser({ ...user, [field]: value });
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1>My Profile</h1>
        <p>Manage your account and view order history</p>
      </div>

      <div className="profile-tabs">
        <button 
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </button>
        <button 
          className={`tab-btn ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          Order History
        </button>
      </div>

      <div className="profile-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <div className="profile-card">
              <h2>Personal Information</h2>
              <form onSubmit={handleUpdateProfile} className="profile-form">
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="full_name">Full Name</label>
                    <input
                      type="text"
                      id="full_name"
                      value={user.full_name}
                      onChange={(e) => handleInputChange('full_name', e.target.value)}
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                      type="text"
                      id="username"
                      value={user.username}
                      onChange={(e) => handleInputChange('username', e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      value={user.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="phone">Phone</label>
                    <input
                      type="tel"
                      id="phone"
                      value={user.phone}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="address">Address</label>
                  <textarea
                    id="address"
                    value={user.address}
                    onChange={(e) => handleInputChange('address', e.target.value)}
                    rows="3"
                  />
                </div>

                <button type="submit" className="btn btn-primary">
                  Update Profile
                </button>
              </form>
            </div>

            <div className="profile-stats">
              <div className="stat-card">
                <h3>Member Since</h3>
                <p>{new Date(user.created_at).toLocaleDateString()}</p>
              </div>
              <div className="stat-card">
                <h3>Last Login</h3>
                <p>{new Date(user.last_login).toLocaleString()}</p>
              </div>
              <div className="stat-card">
                <h3>Total Orders</h3>
                <p>{orders.length}</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'orders' && (
          <div className="orders-section">
            <h2>Order History</h2>
            
            {orders.length === 0 ? (
              <div className="no-orders">
                <p>No orders found</p>
              </div>
            ) : (
              <div className="orders-list">
                {orders.map(order => (
                  <div key={order.id} className="order-card">
                    <div className="order-header">
                      <div className="order-info">
                        <h3>Order #{order.id}</h3>
                        <p>{new Date(order.created_at).toLocaleString()}</p>
                      </div>
                      <div className="order-status">
                        <span className={`status-badge ${order.status}`}>
                          {order.status}
                        </span>
                        <span className="order-total">${order.total.toFixed(2)}</span>
                      </div>
                    </div>
                    
                    <div className="order-items">
                      {order.items.map((item, index) => (
                        <div key={index} className="order-item">
                          <span className="item-name">{item.name}</span>
                          <span className="item-quantity">x{item.quantity}</span>
                          <span className="item-price">${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;

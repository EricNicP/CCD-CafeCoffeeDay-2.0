import React, { useState } from 'react';
import './OrderPage.css';

const OrderPage = () => {
  const [orderItems, setOrderItems] = useState([]);
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    email: '',
    phone: '',
    address: ''
  });

  const addToOrder = (item) => {
    const existingItem = orderItems.find(orderItem => orderItem.id === item.id);
    if (existingItem) {
      setOrderItems(orderItems.map(orderItem =>
        orderItem.id === item.id
          ? { ...orderItem, quantity: orderItem.quantity + 1 }
          : orderItem
      ));
    } else {
      setOrderItems([...orderItems, { ...item, quantity: 1 }]);
    }
  };

  const removeFromOrder = (itemId) => {
    setOrderItems(orderItems.filter(item => item.id !== itemId));
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromOrder(itemId);
    } else {
      setOrderItems(orderItems.map(item =>
        item.id === itemId ? { ...item, quantity: newQuantity } : item
      ));
    }
  };

  const calculateTotal = () => {
    return orderItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const handleSubmitOrder = () => {
    if (orderItems.length === 0) {
      alert('Please add items to your order');
      return;
    }
    
    if (!customerInfo.name || !customerInfo.email) {
      alert('Please fill in your name and email');
      return;
    }

    // TODO: Submit order to backend
    console.log('Order submitted:', { items: orderItems, customer: customerInfo });
    alert('Order submitted successfully!');
    
    // Reset form
    setOrderItems([]);
    setCustomerInfo({ name: '', email: '', phone: '', address: '' });
  };

  return (
    <div className="order-page">
      <div className="order-header">
        <h1>Place Your Order</h1>
        <p>Customize your coffee experience</p>
      </div>

      <div className="order-content">
        <div className="order-items">
          <h2>Your Order</h2>
          
          {orderItems.length === 0 ? (
            <div className="empty-order">
              <p>Your order is empty</p>
              <p>Visit our menu to add items</p>
            </div>
          ) : (
            <div className="order-list">
              {orderItems.map(item => (
                <div key={item.id} className="order-item">
                  <div className="item-info">
                    <h4>{item.name}</h4>
                    <p>{item.description}</p>
                    <span className="item-price">${item.price.toFixed(2)}</span>
                  </div>
                  
                  <div className="item-controls">
                    <button 
                      className="quantity-btn"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      -
                    </button>
                    <span className="quantity">{item.quantity}</span>
                    <button 
                      className="quantity-btn"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      +
                    </button>
                    <button 
                      className="remove-btn"
                      onClick={() => removeFromOrder(item.id)}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {orderItems.length > 0 && (
            <div className="order-total">
              <h3>Total: ${calculateTotal().toFixed(2)}</h3>
            </div>
          )}
        </div>

        <div className="customer-info">
          <h2>Customer Information</h2>
          <form className="customer-form">
            <div className="form-group">
              <label htmlFor="name">Full Name *</label>
              <input
                type="text"
                id="name"
                value={customerInfo.name}
                onChange={(e) => setCustomerInfo({...customerInfo, name: e.target.value})}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="email">Email *</label>
              <input
                type="email"
                id="email"
                value={customerInfo.email}
                onChange={(e) => setCustomerInfo({...customerInfo, email: e.target.value})}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="phone">Phone</label>
              <input
                type="tel"
                id="phone"
                value={customerInfo.phone}
                onChange={(e) => setCustomerInfo({...customerInfo, phone: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="address">Address</label>
              <textarea
                id="address"
                value={customerInfo.address}
                onChange={(e) => setCustomerInfo({...customerInfo, address: e.target.value})}
                rows="3"
              />
            </div>
          </form>
        </div>
      </div>

      {orderItems.length > 0 && (
        <div className="order-actions">
          <button 
            className="btn btn-primary btn-large"
            onClick={handleSubmitOrder}
          >
            Place Order
          </button>
        </div>
      )}
    </div>
  );
};

export default OrderPage;

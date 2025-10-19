import React, { useState, useEffect } from 'react';
import CoffeeCard from '../components/CoffeeCard';
import './HomePage.css';

const HomePage = () => {
  const [featuredItems, setFeaturedItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockData = [
        {
          id: '1',
          name: 'Espresso',
          description: 'Rich, full-bodied coffee with a thick layer of crema',
          price: 3.50,
          category: 'coffee',
          size: 'small',
          available: true,
          image_url: ''
        },
        {
          id: '2',
          name: 'Cappuccino',
          description: 'Espresso with steamed milk and foam',
          price: 4.50,
          category: 'coffee',
          size: 'medium',
          available: true,
          image_url: ''
        },
        {
          id: '3',
          name: 'Latte',
          description: 'Espresso with steamed milk and a small amount of foam',
          price: 5.00,
          category: 'coffee',
          size: 'large',
          available: true,
          image_url: ''
        }
      ];
      setFeaturedItems(mockData);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAddToOrder = (coffee) => {
    console.log('Adding to order:', coffee);
    // TODO: Implement add to order functionality
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="homepage">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to CCD 2.0</h1>
          <p>Experience the perfect blend of tradition and innovation in every cup</p>
          <button className="btn btn-primary btn-large">
            Explore Menu
          </button>
        </div>
      </section>

      <section className="featured-section">
        <div className="section-header">
          <h2>Featured Items</h2>
          <p>Discover our most popular coffee selections</p>
        </div>
        
        <div className="featured-grid">
          {featuredItems.map(coffee => (
            <CoffeeCard 
              key={coffee.id} 
              coffee={coffee} 
              onAddToOrder={handleAddToOrder}
            />
          ))}
        </div>
      </section>

      <section className="stats-section">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">☕</div>
            <div className="stat-content">
              <h3>1000+</h3>
              <p>Cups Served Daily</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-content">
              <h3>4.8</h3>
              <p>Customer Rating</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🏆</div>
            <div className="stat-content">
              <h3>15+</h3>
              <p>Years Experience</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;

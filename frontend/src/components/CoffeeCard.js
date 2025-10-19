import React from 'react';
import './CoffeeCard.css';

const CoffeeCard = ({ coffee, onAddToOrder }) => {
  const handleAddToOrder = () => {
    if (onAddToOrder) {
      onAddToOrder(coffee);
    }
  };

  return (
    <div className="coffee-card">
      <div className="coffee-image">
        {coffee.image_url ? (
          <img src={coffee.image_url} alt={coffee.name} />
        ) : (
          <div className="placeholder-image">
            <span className="coffee-icon">☕</span>
          </div>
        )}
      </div>
      
      <div className="coffee-content">
        <div className="coffee-header">
          <h3 className="coffee-name">{coffee.name}</h3>
          <span className="coffee-category">{coffee.category}</span>
        </div>
        
        <p className="coffee-description">{coffee.description}</p>
        
        <div className="coffee-footer">
          <div className="coffee-price">
            <span className="price">${coffee.price.toFixed(2)}</span>
            <span className="size">{coffee.size}</span>
          </div>
          
          <button 
            className={`btn btn-primary ${!coffee.available ? 'disabled' : ''}`}
            onClick={handleAddToOrder}
            disabled={!coffee.available}
          >
            {coffee.available ? 'Add to Order' : 'Unavailable'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CoffeeCard;

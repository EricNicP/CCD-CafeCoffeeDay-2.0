import React, { useState, useEffect } from 'react';
import CoffeeCard from '../components/CoffeeCard';
import './MenuPage.css';

const MenuPage = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [categories, setCategories] = useState(['all']);
  const [dietaryFilters, setDietaryFilters] = useState([]);
  const [sortBy, setSortBy] = useState('popularity');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Simulate API call with enhanced data
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
          stock_quantity: 50,
          preparation_time: 3,
          calories: 5,
          dietary_tags: ['vegan', 'sugar-free'],
          allergens: [],
          sustainability_rating: 4.5,
          fair_trade: true,
          organic: true,
          farm_info: 'Sourced from sustainable farms in Colombia',
          popularity_score: 4.8,
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
          stock_quantity: 30,
          preparation_time: 5,
          calories: 120,
          dietary_tags: ['vegetarian'],
          allergens: ['dairy'],
          sustainability_rating: 4.0,
          fair_trade: true,
          organic: false,
          popularity_score: 4.6,
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
          stock_quantity: 25,
          preparation_time: 6,
          calories: 150,
          dietary_tags: ['vegetarian'],
          allergens: ['dairy'],
          sustainability_rating: 4.0,
          fair_trade: true,
          organic: false,
          popularity_score: 4.7,
          image_url: ''
        },
        {
          id: '4',
          name: 'Croissant',
          description: 'Buttery, flaky pastry perfect with coffee',
          price: 3.00,
          category: 'pastry',
          size: 'regular',
          available: true,
          stock_quantity: 20,
          preparation_time: 2,
          calories: 200,
          dietary_tags: ['vegetarian'],
          allergens: ['gluten', 'dairy', 'eggs'],
          sustainability_rating: 3.5,
          fair_trade: false,
          organic: false,
          popularity_score: 4.2,
          image_url: ''
        },
        {
          id: '5',
          name: 'Vegan Latte',
          description: 'Plant-based latte with oat milk',
          price: 5.50,
          category: 'coffee',
          size: 'medium',
          available: true,
          stock_quantity: 15,
          preparation_time: 6,
          calories: 100,
          dietary_tags: ['vegan', 'dairy-free'],
          allergens: [],
          sustainability_rating: 4.8,
          fair_trade: true,
          organic: true,
          farm_info: 'Organic coffee with sustainable oat milk',
          popularity_score: 4.5,
          image_url: ''
        },
        {
          id: '6',
          name: 'Green Tea',
          description: 'Premium green tea with antioxidants',
          price: 2.00,
          category: 'beverage',
          size: 'medium',
          available: true,
          stock_quantity: 40,
          preparation_time: 3,
          calories: 0,
          dietary_tags: ['vegan', 'sugar-free'],
          allergens: [],
          sustainability_rating: 4.2,
          fair_trade: false,
          organic: true,
          popularity_score: 3.8,
          image_url: ''
        }
      ];
      setMenuItems(mockData);
      
      // Extract unique categories
      const uniqueCategories = ['all', ...new Set(mockData.map(item => item.category))];
      setCategories(uniqueCategories);
      
      setLoading(false);
    }, 1000);
  }, []);

  const handleAddToOrder = (coffee) => {
    console.log('Adding to order:', coffee);
    // TODO: Implement add to order functionality
  };

  // Enhanced filtering and sorting
  const filteredItems = menuItems.filter(item => {
    // Category filter
    if (selectedCategory !== 'all' && item.category !== selectedCategory) {
      return false;
    }
    
    // Search filter
    if (searchTerm && !item.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    
    // Dietary filters
    if (dietaryFilters.length > 0) {
      const hasMatchingDietaryTag = dietaryFilters.some(filter => 
        item.dietary_tags && item.dietary_tags.includes(filter)
      );
      if (!hasMatchingDietaryTag) {
        return false;
      }
    }
    
    return true;
  }).sort((a, b) => {
    switch (sortBy) {
      case 'price_low':
        return a.price - b.price;
      case 'price_high':
        return b.price - a.price;
      case 'popularity':
        return b.popularity_score - a.popularity_score;
      case 'sustainability':
        return b.sustainability_rating - a.sustainability_rating;
      case 'preparation_time':
        return a.preparation_time - b.preparation_time;
      default:
        return 0;
    }
  });

  const dietaryOptions = ['vegan', 'vegetarian', 'dairy-free', 'sugar-free', 'gluten-free'];
  const sortOptions = [
    { value: 'popularity', label: 'Most Popular' },
    { value: 'price_low', label: 'Price: Low to High' },
    { value: 'price_high', label: 'Price: High to Low' },
    { value: 'sustainability', label: 'Most Sustainable' },
    { value: 'preparation_time', label: 'Quickest to Prepare' }
  ];

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="menu-page">
      <div className="menu-header">
        <h1>Our Menu</h1>
        <p>Discover our carefully crafted selection of coffee, pastries, and beverages</p>
      </div>

      <div className="menu-filters">
        {/* Search Bar */}
        <div className="search-section">
          <input
            type="text"
            placeholder="Search menu items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Category Filters */}
        <div className="category-filters">
          {categories.map(category => (
            <button
              key={category}
              className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category)}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>

        {/* Dietary Filters */}
        <div className="dietary-filters">
          <h4>Dietary Preferences</h4>
          <div className="dietary-options">
            {dietaryOptions.map(option => (
              <label key={option} className="dietary-option">
                <input
                  type="checkbox"
                  checked={dietaryFilters.includes(option)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setDietaryFilters([...dietaryFilters, option]);
                    } else {
                      setDietaryFilters(dietaryFilters.filter(f => f !== option));
                    }
                  }}
                />
                <span>{option.charAt(0).toUpperCase() + option.slice(1).replace('-', ' ')}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Sort Options */}
        <div className="sort-section">
          <label htmlFor="sort-select">Sort by:</label>
          <select
            id="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="menu-grid">
        {filteredItems.map(item => (
          <CoffeeCard 
            key={item.id} 
            coffee={item} 
            onAddToOrder={handleAddToOrder}
          />
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className="no-items">
          <p>No items found in this category.</p>
        </div>
      )}
    </div>
  );
};

export default MenuPage;

  const handleAddToOrder = (coffee) => {
    console.log('Adding to order:', coffee);
    // TODO: Implement add to order functionality
  };

  // Enhanced filtering and sorting
  const filteredItems = menuItems.filter(item => {
    // Category filter
    if (selectedCategory !== 'all' && item.category !== selectedCategory) {
      return false;
    }
    
    // Search filter
    if (searchTerm && !item.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    
    // Dietary filters
    if (dietaryFilters.length > 0) {
      const hasMatchingDietaryTag = dietaryFilters.some(filter => 
        item.dietary_tags && item.dietary_tags.includes(filter)
      );
      if (!hasMatchingDietaryTag) {
        return false;
      }
    }
    
    return true;
  }).sort((a, b) => {
    switch (sortBy) {
      case 'price_low':
        return a.price - b.price;
      case 'price_high':
        return b.price - a.price;
      case 'popularity':
        return b.popularity_score - a.popularity_score;
      case 'sustainability':
        return b.sustainability_rating - a.sustainability_rating;
      case 'preparation_time':
        return a.preparation_time - b.preparation_time;
      default:
        return 0;
    }
  });

  const dietaryOptions = ['vegan', 'vegetarian', 'dairy-free', 'sugar-free', 'gluten-free'];
  const sortOptions = [
    { value: 'popularity', label: 'Most Popular' },
    { value: 'price_low', label: 'Price: Low to High' },
    { value: 'price_high', label: 'Price: High to Low' },
    { value: 'sustainability', label: 'Most Sustainable' },
    { value: 'preparation_time', label: 'Quickest to Prepare' }
  ];

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="menu-page">
      <div className="menu-header">
        <h1>Our Menu</h1>
        <p>Discover our carefully crafted selection of coffee, pastries, and beverages</p>
      </div>

      <div className="menu-filters">
        {/* Search Bar */}
        <div className="search-section">
          <input
            type="text"
            placeholder="Search menu items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Category Filters */}
        <div className="category-filters">
          {categories.map(category => (
            <button
              key={category}
              className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category)}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>

        {/* Dietary Filters */}
        <div className="dietary-filters">
          <h4>Dietary Preferences</h4>
          <div className="dietary-options">
            {dietaryOptions.map(option => (
              <label key={option} className="dietary-option">
                <input
                  type="checkbox"
                  checked={dietaryFilters.includes(option)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setDietaryFilters([...dietaryFilters, option]);
                    } else {
                      setDietaryFilters(dietaryFilters.filter(f => f !== option));
                    }
                  }}
                />
                <span>{option.charAt(0).toUpperCase() + option.slice(1).replace('-', ' ')}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Sort Options */}
        <div className="sort-section">
          <label htmlFor="sort-select">Sort by:</label>
          <select
            id="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="menu-grid">
        {filteredItems.map(item => (
          <CoffeeCard 
            key={item.id} 
            coffee={item} 
            onAddToOrder={handleAddToOrder}
          />
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className="no-items">
          <p>No items found in this category.</p>
        </div>
      )}
    </div>
  );
};

export default MenuPage;

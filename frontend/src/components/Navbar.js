import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">☕</span>
          CCD 2.0
        </Link>
        
        <div className="navbar-menu">
          <Link to="/" className={`navbar-link ${isActive('/')}`}>
            Home
          </Link>
          <Link to="/menu" className={`navbar-link ${isActive('/menu')}`}>
            Menu
          </Link>
          <Link to="/cafes" className={`navbar-link ${isActive('/cafes')}`}>
            Find Cafés
          </Link>
          <Link to="/events" className={`navbar-link ${isActive('/events')}`}>
            Events
          </Link>
          <Link to="/order" className={`navbar-link ${isActive('/order')}`}>
            Order
          </Link>
          <Link to="/profile" className={`navbar-link ${isActive('/profile')}`}>
            Profile
          </Link>
        </div>
        
        <div className="navbar-actions">
          <button className="btn btn-primary">
            Sign In
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
    </nav>
  );
};

export default Navbar;


import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { removeToken, getUser, hasRole } from '../utils/auth';
import './Navbar.css';

function Navbar() {
  const navigate = useNavigate();
  const user = getUser();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" onClick={closeMenu}>CV-Align</Link>
      </div>
      
      <div className={`navbar-toggle ${isMenuOpen ? 'active' : ''}`} onClick={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
      </div>
      
      <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
        <Link to="/" className="navbar-item" onClick={closeMenu}>Dashboard</Link>
        {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
          <Link to="/create-job" className="navbar-item" onClick={closeMenu}>Create Job</Link>
        )}
        <div className="navbar-user">
          <span className="user-info">
            {user?.full_name} ({user?.role})
          </span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
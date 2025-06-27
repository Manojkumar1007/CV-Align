import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { removeToken, getUser, hasRole } from '../utils/auth';
import './Navbar.css';

function Navbar() {
  const navigate = useNavigate();
  const user = getUser();

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">CV-Align</Link>
      </div>
      <div className="navbar-menu">
        <Link to="/" className="navbar-item">Dashboard</Link>
        {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
          <Link to="/create-job" className="navbar-item">Create Job</Link>
        )}
      </div>
      <div className="navbar-user">
        <span className="user-info">
          {user?.full_name} ({user?.role})
        </span>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
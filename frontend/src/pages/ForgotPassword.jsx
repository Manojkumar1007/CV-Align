import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import './ForgotPassword.css';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [emailSent, setEmailSent] = useState(false);

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      setError('Email is required');
      return;
    }
    
    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await authAPI.requestPasswordReset(email);
      setMessage(response.data.message);
      setEmailSent(true);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to send reset email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setEmail(e.target.value);
    if (error) setError('');
    if (message) setMessage('');
  };

  if (emailSent) {
    return (
      <div className="forgot-password-container">
        <div className="forgot-password-card">
          <div className="success-icon">✉️</div>
          <h1>Check Your Email</h1>
          <div className="success-message">
            <p>{message}</p>
            <p>Please check your email and click the reset link to continue.</p>
          </div>
          
          <div className="reset-actions">
            <button 
              onClick={() => {
                setEmailSent(false);
                setEmail('');
                setMessage('');
              }}
              className="btn btn-outline"
            >
              Send Another Email
            </button>
            <Link to="/login" className="btn btn-primary">
              Back to Login
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h1>CV-Align</h1>
        <h2>Reset Your Password</h2>
        <p className="reset-description">
          Enter your email address and we'll send you a link to reset your password.
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={handleChange}
              placeholder="Enter your email address"
              disabled={loading}
              autoFocus
            />
          </div>
          
          {error && <div className="alert alert-error">{error}</div>}
          {message && <div className="alert alert-success">{message}</div>}
          
          <button 
            type="submit" 
            disabled={loading} 
            className={`btn btn-primary reset-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? 'Sending Reset Link...' : 'Send Reset Link'}
          </button>
        </form>
        
        <div className="login-link">
          <p>Remember your password? <Link to="/login">Sign in here</Link></p>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
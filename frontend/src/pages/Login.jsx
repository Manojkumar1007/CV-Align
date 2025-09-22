import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { setToken, setUser, isAuthenticated } from '../utils/auth';
import './Login.css';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated()) {
      navigate('/');
    }
  }, [navigate]);

  const validateField = (name, value) => {
    let error = '';
    
    switch (name) {
      case 'email':
        if (!value) {
          error = 'Email is required';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          error = 'Please enter a valid email address';
        }
        break;
      case 'password':
        if (!value) {
          error = 'Password is required';
        } else if (value.length < 6) {
          error = 'Password must be at least 6 characters';
        }
        break;
      default:
        break;
    }
    
    return error;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors({
        ...fieldErrors,
        [name]: ''
      });
    }
    
    // Clear general error
    if (error) {
      setError('');
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    const fieldError = validateField(name, value);
    
    setFieldErrors({
      ...fieldErrors,
      [name]: fieldError
    });
  };

  const validateForm = () => {
    const errors = {};
    
    Object.keys(formData).forEach(field => {
      const fieldError = validateField(field, formData[field]);
      if (fieldError) {
        errors[field] = fieldError;
      }
    });
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(formData);
      setToken(response.data.access_token);
      
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
      
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (email, password) => {
    setFormData({ email, password });
    setFieldErrors({});
    setError('');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>CV-Align</h1>
        <h2>Login</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.email ? 'error' : ''}
              placeholder="Enter your email"
              disabled={loading}
            />
            {fieldErrors.email && <div className="form-error">{fieldErrors.email}</div>}
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.password ? 'error' : ''}
              placeholder="Enter your password"
              disabled={loading}
            />
            {fieldErrors.password && <div className="form-error">{fieldErrors.password}</div>}
          </div>
          
          {error && <div className="alert alert-error">{error}</div>}
          
          <button 
            type="submit" 
            disabled={loading} 
            className={`btn btn-primary login-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
          
          <div className="forgot-password-link">
            <Link to="/forgot-password">Forgot your password?</Link>
          </div>
        </form>
        
        <div className="demo-credentials">
          <h3>Demo Credentials:</h3>
          <div className="demo-buttons">
            <button 
              type="button"
              className="btn btn-outline demo-btn"
              onClick={() => handleDemoLogin('admin@demo.com', 'admin123')}
              disabled={loading}
            >
              Use Admin Demo
            </button>
            <button 
              type="button"
              className="btn btn-outline demo-btn"
              onClick={() => handleDemoLogin('recruiter@demo.com', 'recruiter123')}
              disabled={loading}
            >
              Use Recruiter Demo
            </button>
          </div>
          <div className="demo-text">
            <p><strong>Admin:</strong> admin@demo.com / admin123</p>
            <p><strong>Recruiter:</strong> recruiter@demo.com / recruiter123</p>
          </div>
        </div>
        
        <div className="register-link">
          <p>Don't have an account? <Link to="/register">Create one here</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Login;
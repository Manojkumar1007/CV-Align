import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import './ResetPassword.css';

function ResetPassword() {
  const [searchParams] = useSearchParams();
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});
  const [resetSuccess, setResetSuccess] = useState(false);
  
  const token = searchParams.get('token');

  useEffect(() => {
    if (!token) {
      setError('Invalid reset link. Please request a new password reset.');
    }
  }, [token]);

  const validateField = (name, value) => {
    let error = '';
    
    switch (name) {
      case 'password':
        if (!value) {
          error = 'Password is required';
        } else if (value.length < 8) {
          error = 'Password must be at least 8 characters';
        } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          error = 'Password must contain at least one uppercase letter, one lowercase letter, and one number';
        }
        break;
      case 'confirmPassword':
        if (!value) {
          error = 'Please confirm your password';
        } else if (value !== formData.password) {
          error = 'Passwords do not match';
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
    
    // Validate confirm password when password changes
    if (name === 'password' && formData.confirmPassword) {
      const confirmError = formData.confirmPassword !== value ? 'Passwords do not match' : '';
      setFieldErrors(prev => ({
        ...prev,
        confirmPassword: confirmError
      }));
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
    
    if (!token) {
      setError('Invalid reset link. Please request a new password reset.');
      return;
    }
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setError('');

    try {
      await authAPI.confirmPasswordReset({
        token: token,
        new_password: formData.password
      });
      
      setResetSuccess(true);
    } catch (error) {
      if (error.response?.status === 400) {
        setError(error.response.data.detail || 'Reset link has expired. Please request a new password reset.');
      } else {
        setError('Failed to reset password. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (resetSuccess) {
    return (
      <div className="reset-password-container">
        <div className="reset-password-card">
          <div className="success-icon">✅</div>
          <h1>Password Reset Successful</h1>
          <div className="success-message">
            <p>Your password has been successfully reset.</p>
            <p>You can now login with your new password.</p>
          </div>
          
          <Link to="/login" className="btn btn-primary">
            Continue to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="reset-password-container">
      <div className="reset-password-card">
        <h1>CV-Align</h1>
        <h2>Set New Password</h2>
        <p className="reset-description">
          Please enter your new password below.
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="password">New Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.password ? 'error' : ''}
              placeholder="Enter your new password"
              disabled={loading || !token}
            />
            {fieldErrors.password && <div className="form-error">{fieldErrors.password}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.confirmPassword ? 'error' : ''}
              placeholder="Confirm your new password"
              disabled={loading || !token}
            />
            {fieldErrors.confirmPassword && <div className="form-error">{fieldErrors.confirmPassword}</div>}
          </div>
          
          {error && <div className="alert alert-error">{error}</div>}
          
          <button 
            type="submit" 
            disabled={loading || !token} 
            className={`btn btn-primary reset-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? 'Resetting Password...' : 'Reset Password'}
          </button>
        </form>
        
        <div className="login-link">
          <p>Remember your password? <Link to="/login">Sign in here</Link></p>
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;
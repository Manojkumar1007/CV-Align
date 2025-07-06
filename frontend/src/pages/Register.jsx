import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI, usersAPI } from '../services/api';
import { setToken, setUser, isAuthenticated } from '../utils/auth';
import Loading from '../components/Loading';
import './Register.css';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    role: 'recruiter',
    company_id: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [fieldErrors, setFieldErrors] = useState({});
  const [companies, setCompanies] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated()) {
      navigate('/');
    }
    fetchCompanies();
  }, [navigate]);

  const fetchCompanies = async () => {
    try {
      const response = await usersAPI.getCompanies();
      setCompanies(response.data);
    } catch (error) {
      setError('Failed to load companies');
    } finally {
      setLoadingCompanies(false);
    }
  };

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
      case 'full_name':
        if (!value) {
          error = 'Full name is required';
        } else if (value.length < 2) {
          error = 'Full name must be at least 2 characters';
        }
        break;
      case 'role':
        if (!value) {
          error = 'Role is required';
        }
        break;
      case 'company_id':
        if (!value) {
          error = 'Company is required';
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
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setError('');

    try {
      const registrationData = {
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        role: formData.role,
        company_id: parseInt(formData.company_id)
      };

      await authAPI.register(registrationData);
      
      // Auto login after successful registration
      const loginResponse = await authAPI.login({
        email: formData.email,
        password: formData.password
      });
      
      setToken(loginResponse.data.access_token);
      
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
      
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loadingCompanies) {
    return <Loading message="Loading registration form..." fullScreen />;
  }

  return (
    <div className="register-container">
      <div className="register-card">
        <h1>CV-Align</h1>
        <h2>Create Account</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="full_name">Full Name</label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.full_name ? 'error' : ''}
              placeholder="Enter your full name"
              disabled={loading}
            />
            {fieldErrors.full_name && <div className="form-error">{fieldErrors.full_name}</div>}
          </div>

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

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              onBlur={handleBlur}
              className={fieldErrors.confirmPassword ? 'error' : ''}
              placeholder="Confirm your password"
              disabled={loading}
            />
            {fieldErrors.confirmPassword && <div className="form-error">{fieldErrors.confirmPassword}</div>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="role">Role</label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                onBlur={handleBlur}
                className={fieldErrors.role ? 'error' : ''}
                disabled={loading}
              >
                <option value="recruiter">Recruiter</option>
                <option value="hiring_manager">Hiring Manager</option>
                <option value="admin">Admin</option>
              </select>
              {fieldErrors.role && <div className="form-error">{fieldErrors.role}</div>}
            </div>

            <div className="form-group">
              <label htmlFor="company_id">Company</label>
              <select
                id="company_id"
                name="company_id"
                value={formData.company_id}
                onChange={handleChange}
                onBlur={handleBlur}
                className={fieldErrors.company_id ? 'error' : ''}
                disabled={loading}
              >
                <option value="">Select a company</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>
                    {company.name}
                  </option>
                ))}
              </select>
              {fieldErrors.company_id && <div className="form-error">{fieldErrors.company_id}</div>}
            </div>
          </div>
          
          {error && <div className="alert alert-error">{error}</div>}
          
          <button 
            type="submit" 
            disabled={loading} 
            className={`btn btn-primary register-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>
        
        <div className="login-link">
          <p>Already have an account? <Link to="/login">Sign in here</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Register;
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../pages/Login';

// Mock the auth utility and API
jest.mock('../utils/auth', () => ({
  isAuthenticated: () => false,
  setToken: jest.fn(),
  setUser: jest.fn()
}));

jest.mock('../services/api', () => ({
  authAPI: {
    login: jest.fn(),
    getCurrentUser: jest.fn()
  }
}));

const LoginWrapper = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

test('renders login form', () => {
  render(
    <LoginWrapper>
      <Login />
    </LoginWrapper>
  );
  
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
});

test('displays demo credentials', () => {
  render(
    <LoginWrapper>
      <Login />
    </LoginWrapper>
  );
  
  expect(screen.getByText(/demo credentials/i)).toBeInTheDocument();
  expect(screen.getByText(/admin@demo.com/)).toBeInTheDocument();
  expect(screen.getByText(/recruiter@demo.com/)).toBeInTheDocument();
});

test('validates required fields', async () => {
  render(
    <LoginWrapper>
      <Login />
    </LoginWrapper>
  );
  
  const loginButton = screen.getByRole('button', { name: /login/i });
  fireEvent.click(loginButton);
  
  // Form should have HTML5 validation for required fields
  const emailInput = screen.getByLabelText(/email/i);
  const passwordInput = screen.getByLabelText(/password/i);
  
  expect(emailInput).toBeRequired();
  expect(passwordInput).toBeRequired();
});
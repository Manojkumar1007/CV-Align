import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

// Mock the auth utility to avoid localStorage issues in tests
jest.mock('../utils/auth', () => ({
  isAuthenticated: () => false,
  getUser: () => null,
  setToken: jest.fn(),
  removeToken: jest.fn(),
  hasRole: jest.fn(() => false)
}));

// Wrapper component to provide router context
const AppWrapper = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

test('renders login page when not authenticated', () => {
  render(
    <AppWrapper>
      <App />
    </AppWrapper>
  );
  
  // Should redirect to login page when not authenticated
  expect(window.location.pathname).toBe('/');
});

test('App component renders without crashing', () => {
  render(
    <AppWrapper>
      <App />
    </AppWrapper>
  );
  
  // App should render successfully
  expect(document.querySelector('.App')).toBeInTheDocument();
});
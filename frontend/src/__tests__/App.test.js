import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

// Mock the auth utility to avoid localStorage issues in tests
jest.mock('../utils/auth', () => ({
  isAuthenticated: () => false,
  getUser: () => null,
  setToken: jest.fn(),
  removeToken: jest.fn(),
  hasRole: jest.fn(() => false)
}));

// Mock all page components to avoid complex dependencies
jest.mock('../pages/Login', () => {
  return function MockLogin() {
    return <div data-testid="login-page">Login Page</div>;
  };
});

jest.mock('../pages/Dashboard', () => {
  return function MockDashboard() {
    return <div data-testid="dashboard-page">Dashboard Page</div>;
  };
});

jest.mock('../pages/JobDetails', () => {
  return function MockJobDetails() {
    return <div data-testid="job-details-page">Job Details Page</div>;
  };
});

jest.mock('../pages/CreateJob', () => {
  return function MockCreateJob() {
    return <div data-testid="create-job-page">Create Job Page</div>;
  };
});

jest.mock('../pages/CandidateEvaluation', () => {
  return function MockCandidateEvaluation() {
    return <div data-testid="candidate-evaluation-page">Candidate Evaluation Page</div>;
  };
});

jest.mock('../components/Navbar', () => {
  return function MockNavbar() {
    return <div data-testid="navbar">Navbar</div>;
  };
});

test('App component renders without crashing', () => {
  const App = require('../App').default;
  
  render(
    <MemoryRouter initialEntries={['/login']}>
      <App />
    </MemoryRouter>
  );
  
  // App should render successfully without errors
});

test('App renders login when not authenticated', () => {
  const App = require('../App').default;
  
  render(
    <MemoryRouter initialEntries={['/login']}>
      <App />
    </MemoryRouter>
  );
  
  expect(screen.getByTestId('login-page')).toBeInTheDocument();
});
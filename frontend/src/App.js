import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './utils/auth';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import JobDetails from './pages/JobDetails';
import CreateJob from './pages/CreateJob';
import CandidateEvaluation from './pages/CandidateEvaluation';
import Navbar from './components/Navbar';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';
import './App.css';

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <Router>
          <div className="App">
            {isAuthenticated() && <Navbar />}
            <main className="main-content">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                <Route path="/jobs/:id" element={
                  <ProtectedRoute>
                    <JobDetails />
                  </ProtectedRoute>
                } />
                <Route path="/create-job" element={
                  <ProtectedRoute>
                    <CreateJob />
                  </ProtectedRoute>
                } />
                <Route path="/evaluation/:id" element={
                  <ProtectedRoute>
                    <CandidateEvaluation />
                  </ProtectedRoute>
                } />
              </Routes>
            </main>
          </div>
        </Router>
      </ToastProvider>
    </ErrorBoundary>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { jobsAPI } from '../services/api';
import { hasRole } from '../utils/auth';
import './Dashboard.css';

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await jobsAPI.getJobs();
      setJobs(response.data);
    } catch (error) {
      setError('Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await jobsAPI.deleteJob(jobId);
        setJobs(jobs.filter(job => job.id !== jobId));
      } catch (error) {
        setError('Failed to delete job');
      }
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="dashboard">
          <div className="dashboard-header">
            <div className="skeleton skeleton-line title" style={{ width: '200px' }}></div>
            <div className="skeleton skeleton-line" style={{ width: '150px', height: '40px' }}></div>
          </div>
          <div className="grid grid-auto">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="skeleton-card">
                <div className="skeleton skeleton-line title"></div>
                <div className="skeleton skeleton-line subtitle"></div>
                <div className="skeleton skeleton-line content"></div>
                <div className="skeleton skeleton-line content short"></div>
                <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                  <div className="skeleton skeleton-line" style={{ width: '100px', height: '35px' }}></div>
                  <div className="skeleton skeleton-line" style={{ width: '80px', height: '35px' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
            <Link to="/create-job" className="btn btn-primary">
              Create New Job
            </Link>
          )}
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="grid grid-auto">
          {jobs.length === 0 ? (
            <div className="no-jobs">
              <h3>No jobs available</h3>
              <p>Create your first job to start evaluating CVs</p>
              {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
                <Link to="/create-job" className="btn btn-primary" style={{ marginTop: '1rem' }}>
                  Create Your First Job
                </Link>
              )}
            </div>
          ) : (
            jobs.map(job => (
              <div key={job.id} className="card">
                <div className="card-header">
                  <h3 className="card-title">{job.title}</h3>
                  <span className="experience-level">{job.experience_level}</span>
                </div>
                
                <div className="card-content">
                  <p className="job-description">
                    {job.description.length > 150 
                      ? `${job.description.substring(0, 150)}...`
                      : job.description
                    }
                  </p>
                  
                  <div className="job-meta">
                    <span>Created: {new Date(job.created_at).toLocaleDateString()}</span>
                    {job.is_active && <span className="active-badge">Active</span>}
                  </div>
                </div>
                
                <div className="card-footer">
                  <div className="job-actions">
                    <Link to={`/jobs/${job.id}`} className="btn btn-primary">
                      View Details
                    </Link>
                    {hasRole(['admin', 'recruiter']) && (
                      <button 
                        onClick={() => handleDeleteJob(job.id)}
                        className="btn btn-danger"
                      >
                        Delete
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
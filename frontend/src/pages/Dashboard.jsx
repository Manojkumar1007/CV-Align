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

  if (loading) return <div className="loading">Loading jobs...</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
          <Link to="/create-job" className="create-job-btn">
            Create New Job
          </Link>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="jobs-grid">
        {jobs.length === 0 ? (
          <div className="no-jobs">
            <h3>No jobs available</h3>
            <p>Create your first job to start evaluating CVs</p>
          </div>
        ) : (
          jobs.map(job => (
            <div key={job.id} className="job-card">
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className="experience-level">{job.experience_level}</span>
              </div>
              
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
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;
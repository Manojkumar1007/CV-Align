import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { jobsAPI } from '../services/api';
import { hasRole } from '../utils/auth';
import SearchBar from '../components/SearchBar';
import './Dashboard.css';

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({});

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await jobsAPI.getJobs();
      setJobs(response.data);
      setFilteredJobs(response.data);
    } catch (error) {
      setError('Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  };

  const filterJobs = useCallback((searchTerm, filters) => {
    let filtered = [...jobs];

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(job =>
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.requirements.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (job.preferred_skills && job.preferred_skills.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Apply experience level filter
    if (filters.experience_level) {
      filtered = filtered.filter(job => job.experience_level === filters.experience_level);
    }

    // Apply status filter
    if (filters.status) {
      if (filters.status === 'active') {
        filtered = filtered.filter(job => job.is_active);
      } else if (filters.status === 'inactive') {
        filtered = filtered.filter(job => !job.is_active);
      }
    }

    // Apply date filter
    if (filters.date_range) {
      const now = new Date();
      const filterDate = new Date();
      
      switch (filters.date_range) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0);
          filtered = filtered.filter(job => new Date(job.created_at) >= filterDate);
          break;
        case 'week':
          filterDate.setDate(now.getDate() - 7);
          filtered = filtered.filter(job => new Date(job.created_at) >= filterDate);
          break;
        case 'month':
          filterDate.setMonth(now.getMonth() - 1);
          filtered = filtered.filter(job => new Date(job.created_at) >= filterDate);
          break;
        default:
          break;
      }
    }

    setFilteredJobs(filtered);
  }, [jobs]);

  useEffect(() => {
    filterJobs(searchTerm, filters);
  }, [searchTerm, filters, filterJobs]);

  const handleSearch = useCallback((term) => {
    setSearchTerm(term);
  }, []);

  const handleFilter = useCallback((newFilters) => {
    setFilters(newFilters);
  }, []);

  const handleDeleteJob = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await jobsAPI.deleteJob(jobId);
        const updatedJobs = jobs.filter(job => job.id !== jobId);
        setJobs(updatedJobs);
        setFilteredJobs(updatedJobs.filter(job => {
          // Re-apply current filters after deletion
          let shouldInclude = true;
          
          if (searchTerm) {
            shouldInclude = shouldInclude && (
              job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
              job.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
              job.requirements.toLowerCase().includes(searchTerm.toLowerCase()) ||
              (job.preferred_skills && job.preferred_skills.toLowerCase().includes(searchTerm.toLowerCase()))
            );
          }
          
          if (filters.experience_level) {
            shouldInclude = shouldInclude && job.experience_level === filters.experience_level;
          }
          
          if (filters.status) {
            if (filters.status === 'active') {
              shouldInclude = shouldInclude && job.is_active;
            } else if (filters.status === 'inactive') {
              shouldInclude = shouldInclude && !job.is_active;
            }
          }
          
          return shouldInclude;
        }));
      } catch (error) {
        setError('Failed to delete job');
      }
    }
  };

  const jobFilters = [
    {
      key: 'experience_level',
      label: 'Experience Level',
      options: [
        { value: 'entry', label: 'Entry Level' },
        { value: 'mid', label: 'Mid Level' },
        { value: 'senior', label: 'Senior Level' },
        { value: 'lead', label: 'Lead/Principal' },
        { value: 'executive', label: 'Executive' }
      ]
    },
    {
      key: 'status',
      label: 'Status',
      options: [
        { value: 'active', label: 'Active' },
        { value: 'inactive', label: 'Inactive' }
      ]
    },
    {
      key: 'date_range',
      label: 'Created',
      options: [
        { value: 'today', label: 'Today' },
        { value: 'week', label: 'This Week' },
        { value: 'month', label: 'This Month' }
      ]
    }
  ];

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

        <SearchBar
          placeholder="Search jobs by title, description, or skills..."
          onSearch={handleSearch}
          onFilter={handleFilter}
          filters={jobFilters}
          className="dashboard-search"
        />

        <div className="dashboard-stats">
          <div className="stat-item">
            <span className="stat-number">{filteredJobs.length}</span>
            <span className="stat-label">
              {filteredJobs.length === 1 ? 'Job' : 'Jobs'} 
              {searchTerm || Object.keys(filters).length > 0 ? ' (filtered)' : ''}
            </span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{filteredJobs.filter(job => job.is_active).length}</span>
            <span className="stat-label">Active</span>
          </div>
        </div>

        <div className="grid grid-auto">
          {filteredJobs.length === 0 ? (
            jobs.length === 0 ? (
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
              <div className="no-results">
                <h3>No jobs match your search</h3>
                <p>Try adjusting your search terms or filters</p>
              </div>
            )
          ) : (
            filteredJobs.map(job => (
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
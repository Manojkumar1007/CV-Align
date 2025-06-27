import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobsAPI } from '../services/api';
import './CreateJob.css';

function CreateJob() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    requirements: '',
    preferred_skills: '',
    experience_level: 'entry'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await jobsAPI.createJob(formData);
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-job">
      <div className="create-job-container">
        <h1>Create New Job</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Job Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="e.g. Senior Software Engineer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="experience_level">Experience Level *</label>
            <select
              id="experience_level"
              name="experience_level"
              value={formData.experience_level}
              onChange={handleChange}
              required
            >
              <option value="entry">Entry Level</option>
              <option value="mid">Mid Level</option>
              <option value="senior">Senior Level</option>
              <option value="lead">Lead/Principal</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Job Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="6"
              placeholder="Describe the role, responsibilities, and what the ideal candidate would do..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="requirements">Requirements *</label>
            <textarea
              id="requirements"
              name="requirements"
              value={formData.requirements}
              onChange={handleChange}
              required
              rows="6"
              placeholder="List the essential qualifications, skills, and experience required..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="preferred_skills">Preferred Skills</label>
            <textarea
              id="preferred_skills"
              name="preferred_skills"
              value={formData.preferred_skills}
              onChange={handleChange}
              rows="4"
              placeholder="List any nice-to-have skills, certifications, or experience..."
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Creating...' : 'Create Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateJob;
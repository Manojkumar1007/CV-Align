import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { jobsAPI, evaluationsAPI } from '../services/api';
import { hasRole } from '../utils/auth';
import CVUpload from '../components/CVUpload';
import CandidateList from '../components/CandidateList';
import './JobDetails.css';

function JobDetails() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showUpload, setShowUpload] = useState(false);

  useEffect(() => {
    fetchJobData();
  }, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchJobData = async () => {
    try {
      const [jobResponse, candidatesResponse] = await Promise.all([
        jobsAPI.getJob(id),
        evaluationsAPI.getJobCandidates(id)
      ]);
      setJob(jobResponse.data);
      setCandidates(candidatesResponse.data);
    } catch (error) {
      setError('Failed to fetch job details');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (newEvaluation) => {
    setCandidates([newEvaluation, ...candidates]);
    setShowUpload(false);
  };

  if (loading) return <div className="loading">Loading job details...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!job) return <div className="error-message">Job not found</div>;

  return (
    <div className="job-details">
      <div className="job-header">
        <div className="job-info">
          <h1>{job.title}</h1>
          <div className="job-meta">
            <span className="experience-level">{job.experience_level}</span>
            <span>Created: {new Date(job.created_at).toLocaleDateString()}</span>
            {job.is_active && <span className="active-badge">Active</span>}
          </div>
        </div>
        <div className="job-actions">
          <Link to="/" className="btn btn-secondary">Back to Dashboard</Link>
          {hasRole(['admin', 'recruiter', 'hiring_manager']) && (
            <button
              onClick={() => setShowUpload(!showUpload)}
              className="btn btn-primary"
            >
              {showUpload ? 'Cancel Upload' : 'Upload CV'}
            </button>
          )}
        </div>
      </div>

      <div className="job-content">
        <div className="job-description-section">
          <h2>Job Description</h2>
          <p>{job.description}</p>
        </div>

        <div className="job-requirements-section">
          <h2>Requirements</h2>
          <p>{job.requirements}</p>
        </div>

        {job.preferred_skills && (
          <div className="job-skills-section">
            <h2>Preferred Skills</h2>
            <p>{job.preferred_skills}</p>
          </div>
        )}
      </div>

      {showUpload && (
        <div className="upload-section">
          <CVUpload jobId={id} onUploadSuccess={handleUploadSuccess} />
        </div>
      )}

      <div className="candidates-section">
        <h2>Candidates ({candidates.length})</h2>
        <CandidateList candidates={candidates} />
      </div>
    </div>
  );
}

export default JobDetails;
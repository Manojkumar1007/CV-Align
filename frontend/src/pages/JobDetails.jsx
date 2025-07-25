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
  const [processingUpload, setProcessingUpload] = useState(false);

  useEffect(() => {
    fetchJobData();
  }, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchJobData = async (retryCount = 0) => {
    try {
      const [jobResponse, candidatesResponse] = await Promise.all([
        jobsAPI.getJob(id),
        evaluationsAPI.getJobCandidates(id)
      ]);
      setJob(jobResponse.data);
      setCandidates(candidatesResponse.data);
      setError(''); // Clear any previous errors
    } catch (error) {
      console.error('Error fetching job data:', error);
      
      // Retry on network errors (but not on auth/permission errors)
      if (retryCount < 2 && (!error.response || error.response.status >= 500)) {
        console.log(`Retrying request (attempt ${retryCount + 1}/2)...`);
        setTimeout(() => fetchJobData(retryCount + 1), 1000);
        return;
      }
      
      if (error.response?.status === 401) {
        setError('Session expired. Please login again.');
      } else if (error.response?.status === 404) {
        setError('Job not found or you do not have permission to view this job.');
      } else if (error.response?.status === 403) {
        setError('You do not have permission to view this job.');
      } else {
        setError(error.response?.data?.detail || 'Failed to fetch job details. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = async (uploadResponse) => {
    console.log('Upload success - starting processing state', uploadResponse);
    // Show processing state immediately
    setProcessingUpload(true);
    setShowUpload(false);
    
    try {
      // Fetch the full evaluation data using the evaluation_id
      const evaluationResponse = await evaluationsAPI.getEvaluation(uploadResponse.evaluation_id);
      console.log('Full evaluation data:', evaluationResponse.data);
      
      // Hide processing state and add the full candidate data
      setTimeout(() => {
        console.log('Processing complete - adding candidate and hiding loading');
        setCandidates([evaluationResponse.data, ...candidates]);
        setProcessingUpload(false);
      }, 1500);
    } catch (error) {
      console.error('Error fetching evaluation data:', error);
      setProcessingUpload(false);
      setError('Failed to load candidate data after upload');
    }
  };

  const handleCandidateDeleted = (deletedCandidateId) => {
    setCandidates(candidates.filter(candidate => candidate.id !== deletedCandidateId));
  };

  if (loading) return <div className="loading">Loading job details...</div>;
  if (error) return (
    <div className="error-message">
      {error}
      <button 
        onClick={() => {
          setError('');
          setLoading(true);
          fetchJobData();
        }}
        className="btn btn-secondary"
        style={{ marginLeft: '10px' }}
      >
        Retry
      </button>
    </div>
  );
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
        <h2>Candidates ({processingUpload ? candidates.length + 1 : candidates.length})</h2>
        <CandidateList 
          candidates={candidates} 
          onCandidateDeleted={handleCandidateDeleted}
          processingUpload={processingUpload}
        />
      </div>
    </div>
  );
}

export default JobDetails;
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { evaluationsAPI } from '../services/api';
import { hasRole } from '../utils/auth';
import './CandidateList.css';

function CandidateList({ candidates, onCandidateDeleted, processingUpload }) {
  const [deletingId, setDeletingId] = useState(null);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [candidateToDelete, setCandidateToDelete] = useState(null);
  const getScoreColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 65) return '#f39c12';
    if (score >= 50) return '#e67e22';
    return '#e74c3c';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDeleteClick = (candidate) => {
    setCandidateToDelete(candidate);
    setShowConfirmDialog(true);
  };

  const handleConfirmDelete = async () => {
    if (!candidateToDelete) return;
    
    setDeletingId(candidateToDelete.id);
    try {
      await evaluationsAPI.deleteEvaluation(candidateToDelete.id);
      setShowConfirmDialog(false);
      setCandidateToDelete(null);
      if (onCandidateDeleted) {
        onCandidateDeleted(candidateToDelete.id);
      }
    } catch (error) {
      console.error('Error deleting candidate:', error);
      alert('Failed to delete candidate. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleCancelDelete = () => {
    setShowConfirmDialog(false);
    setCandidateToDelete(null);
  };

  const LoadingCard = () => (
    <div className="candidate-card loading-card">
      <div className="candidate-rank">#1</div>
      
      <div className="candidate-info">
        <div className="loading-placeholder loading-name"></div>
        <div className="loading-placeholder loading-email"></div>
        <div className="loading-placeholder loading-file"></div>
        <div className="loading-placeholder loading-date"></div>
      </div>
      
      <div className="candidate-scores">
        <div className="overall-score">
          <div className="score-circle loading-score">
            <div className="loading-spinner"></div>
          </div>
          <span>Processing...</span>
        </div>
        
        <div className="detailed-scores">
          <div className="score-item">
            <span className="score-label">Skills:</span>
            <div className="loading-placeholder loading-score-value"></div>
          </div>
          <div className="score-item">
            <span className="score-label">Experience:</span>
            <div className="loading-placeholder loading-score-value"></div>
          </div>
          <div className="score-item">
            <span className="score-label">Education:</span>
            <div className="loading-placeholder loading-score-value"></div>
          </div>
        </div>
      </div>
      
      <div className="candidate-feedback">
        <div className="loading-placeholder loading-feedback"></div>
      </div>
      
      <div className="candidate-actions">
        <div className="loading-placeholder loading-button"></div>
      </div>
    </div>
  );

  // Show "no candidates" message only when not processing and no candidates
  if (candidates.length === 0 && !processingUpload) {
    return (
      <div className="no-candidates">
        <p>No candidates have been evaluated for this job yet.</p>
        <p>Upload a CV to get started with the evaluation process.</p>
      </div>
    );
  }

  return (
    <div className="candidate-list">
      <div className="candidates-header">
        <div className="sort-info">
          Candidates sorted by overall score (highest first)
        </div>
      </div>
      
      <div className="candidates-grid">
        {processingUpload && <LoadingCard />}
        {candidates.map((candidate, index) => (
          <div key={candidate.id} className="candidate-card">
            <div className="candidate-rank">#{index + 1}</div>
            
            <div className="candidate-info">
              <h3>{candidate.candidate_name}</h3>
              {candidate.candidate_email && (
                <p className="candidate-email">{candidate.candidate_email}</p>
              )}
              <p className="candidate-file">{candidate.cv_filename}</p>
              <p className="candidate-date">Evaluated: {formatDate(candidate.created_at)}</p>
            </div>
            
            <div className="candidate-scores">
              <div className="overall-score">
                <div
                  className="score-circle"
                  style={{ backgroundColor: getScoreColor(candidate.overall_score) }}
                >
                  {candidate.overall_score}
                </div>
                <span>Overall</span>
              </div>
              
              <div className="detailed-scores">
                <div className="score-item">
                  <span className="score-label">Skills:</span>
                  <span className="score-value">{candidate.skills_score}</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Experience:</span>
                  <span className="score-value">{candidate.experience_score}</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Education:</span>
                  <span className="score-value">{candidate.education_score}</span>
                </div>
              </div>
            </div>
            
            <div className="candidate-feedback">
              <p>{candidate.feedback}</p>
            </div>
            
            <div className="candidate-actions">
              <Link
                to={`/evaluation/${candidate.id}`}
                className="btn btn-primary"
              >
                View Details
              </Link>
              {hasRole(['admin', 'recruiter']) && (
                <button
                  onClick={() => handleDeleteClick(candidate)}
                  disabled={deletingId === candidate.id}
                  className="btn btn-danger"
                  style={{ marginLeft: '10px' }}
                >
                  {deletingId === candidate.id ? 'Deleting...' : 'Delete'}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {showConfirmDialog && (
        <div className="modal-overlay" onClick={handleCancelDelete}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Delete Candidate</h3>
            <p>
              Are you sure you want to delete <strong>{candidateToDelete?.candidate_name}</strong>?
            </p>
            <p className="warning-text">
              This action cannot be undone. All evaluation data will be permanently removed.
            </p>
            <div className="modal-actions">
              <button 
                onClick={handleCancelDelete}
                className="btn btn-secondary"
              >
                Cancel
              </button>
              <button 
                onClick={handleConfirmDelete}
                className="btn btn-danger"
                disabled={deletingId}
              >
                {deletingId ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CandidateList;
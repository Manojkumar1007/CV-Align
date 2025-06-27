import React from 'react';
import { Link } from 'react-router-dom';
import './CandidateList.css';

function CandidateList({ candidates }) {
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

  if (candidates.length === 0) {
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
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CandidateList;
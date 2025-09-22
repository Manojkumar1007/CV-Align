import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { evaluationsAPI } from '../services/api';
import { exportEvaluationToPDF, exportEvaluationToExcel } from '../utils/exportUtils';
import { useToast } from '../components/Toast';
import './CandidateEvaluation.css';

function CandidateEvaluation() {
  const { id } = useParams();
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [exporting, setExporting] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetchEvaluation();
  }, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchEvaluation = async () => {
    try {
      const response = await evaluationsAPI.getEvaluation(id);
      setEvaluation(response.data);
    } catch (error) {
      setError('Failed to fetch evaluation details');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 65) return '#f39c12';
    if (score >= 50) return '#e67e22';
    return '#e74c3c';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleExportPDF = async () => {
    if (!evaluation || exporting) return;
    
    setExporting(true);
    try {
      await exportEvaluationToPDF(evaluation);
      toast.success('PDF report generated successfully!');
    } catch (error) {
      toast.error(error.message || 'Failed to generate PDF report');
    } finally {
      setExporting(false);
    }
  };

  const handleExportExcel = async () => {
    if (!evaluation || exporting) return;
    
    setExporting(true);
    try {
      await exportEvaluationToExcel(evaluation);
      toast.success('Excel file generated successfully!');
    } catch (error) {
      toast.error(error.message || 'Failed to generate Excel file');
    } finally {
      setExporting(false);
    }
  };

  if (loading) return <div className="loading">Loading evaluation...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!evaluation) return <div className="error-message">Evaluation not found</div>;

  return (
    <div className="candidate-evaluation">
      <div className="evaluation-header">
        <div className="candidate-info">
          <h1>{evaluation.candidate_name}</h1>
          {evaluation.candidate_email && (
            <p className="candidate-email">{evaluation.candidate_email}</p>
          )}
          <p className="evaluation-meta">
            CV: {evaluation.cv_filename} | Evaluated: {formatDate(evaluation.created_at)}
          </p>
        </div>
        <div className="header-actions">
          <div className="export-buttons">
            <button
              onClick={handleExportPDF}
              disabled={exporting}
              className={`btn btn-outline export-btn ${exporting ? 'loading' : ''}`}
              title="Export as PDF"
            >
              {exporting ? 'Generating...' : '📄 Export PDF'}
            </button>
            <button
              onClick={handleExportExcel}
              disabled={exporting}
              className={`btn btn-outline export-btn ${exporting ? 'loading' : ''}`}
              title="Export as Excel"
            >
              {exporting ? 'Generating...' : '📊 Export Excel'}
            </button>
          </div>
          <Link to={`/jobs/${evaluation.job_id}`} className="btn btn-secondary">
            Back to Job
          </Link>
        </div>
      </div>

      <div className="evaluation-content">
        <div className="scores-section">
          <h2>Evaluation Scores</h2>
          <div className="scores-grid">
            <div className="score-card overall">
              <div
                className="score-circle large"
                style={{ backgroundColor: getScoreColor(evaluation.overall_score) }}
              >
                {evaluation.overall_score}
              </div>
              <h3>Overall Score</h3>
              <p>Comprehensive evaluation based on all criteria</p>
            </div>
            
            <div className="score-card">
              <div
                className="score-circle"
                style={{ backgroundColor: getScoreColor(evaluation.skills_score) }}
              >
                {evaluation.skills_score}
              </div>
              <h3>Skills Match</h3>
              <p>Technical and professional skills alignment</p>
            </div>
            
            <div className="score-card">
              <div
                className="score-circle"
                style={{ backgroundColor: getScoreColor(evaluation.experience_score) }}
              >
                {evaluation.experience_score}
              </div>
              <h3>Experience</h3>
              <p>Relevant work experience and background</p>
            </div>
            
            <div className="score-card">
              <div
                className="score-circle"
                style={{ backgroundColor: getScoreColor(evaluation.education_score) }}
              >
                {evaluation.education_score}
              </div>
              <h3>Education</h3>
              <p>Educational qualifications and certifications</p>
            </div>
          </div>
        </div>

        <div className="feedback-section">
          <h2>Overall Feedback</h2>
          <div className="feedback-content">
            <p>{evaluation.feedback}</p>
          </div>
        </div>

        <div className="analysis-sections">
          <div className="strengths-section">
            <h2>Strengths</h2>
            <div className="analysis-content">
              {evaluation.strengths.split('\n').map((strength, index) => (
                <div key={index} className="analysis-item positive">
                  ✓ {strength}
                </div>
              ))}
            </div>
          </div>

          <div className="weaknesses-section">
            <h2>Areas for Improvement</h2>
            <div className="analysis-content">
              {evaluation.weaknesses.split('\n').map((weakness, index) => (
                <div key={index} className="analysis-item negative">
                  ⚠ {weakness}
                </div>
              ))}
            </div>
          </div>

          <div className="recommendations-section">
            <h2>Recommendations</h2>
            <div className="analysis-content">
              {evaluation.recommendations.split('\n').map((recommendation, index) => (
                <div key={index} className="analysis-item neutral">
                  💡 {recommendation}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CandidateEvaluation;
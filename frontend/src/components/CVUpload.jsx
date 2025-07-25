import React, { useState } from 'react';
import { evaluationsAPI } from '../services/api';
import './CVUpload.css';

function CVUpload({ jobId, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError('');
    }
  };

  const validateFile = (file) => {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!allowedTypes.includes(file.type)) {
      return 'Only PDF, DOCX, and TXT files are allowed';
    }

    if (file.size > maxSize) {
      return 'File size must be less than 10MB';
    }

    return null;
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setUploading(true);
    setError('');

    try {
      const response = await evaluationsAPI.uploadCV(jobId, file);
      onUploadSuccess(response.data);
      setFile(null);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to upload CV');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="cv-upload">
      <h3>Upload Candidate CV</h3>
      
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="upload-content">
          <div className="upload-icon">📄</div>
          <p>Drag and drop your CV here, or click to select</p>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.docx,.txt"
            className="file-input"
          />
          <p className="file-types">Supported formats: PDF, DOCX, TXT (max 10MB)</p>
        </div>
      </div>

      {file && (
        <div className="file-info">
          <p><strong>Selected file:</strong> {file.name}</p>
          <p><strong>Size:</strong> {(file.size / 1024 / 1024).toFixed(2)} MB</p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      <div className="upload-actions">
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="btn btn-primary"
        >
{uploading ? 'Uploading and Processing...' : 'Upload and Evaluate'}
        </button>
      </div>
    </div>
  );
}

export default CVUpload;
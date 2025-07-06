import React from 'react';
import './Loading.css';

function Loading({ message = "Loading...", fullScreen = false }) {
  const content = (
    <div className={`loading-container ${fullScreen ? 'fullscreen' : ''}`}>
      <div className="loading-spinner"></div>
      <span className="loading-message">{message}</span>
    </div>
  );

  return content;
}

export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton-header">
        <div className="skeleton skeleton-line title"></div>
        <div className="skeleton skeleton-line subtitle"></div>
      </div>
      <div className="skeleton skeleton-line content"></div>
      <div className="skeleton skeleton-line content"></div>
      <div className="skeleton skeleton-line content short"></div>
      <div className="skeleton-footer">
        <div className="skeleton skeleton-line" style={{ width: '100px', height: '35px' }}></div>
        <div className="skeleton skeleton-line" style={{ width: '80px', height: '35px' }}></div>
      </div>
    </div>
  );
}

export function SkeletonTable({ rows = 5, columns = 4 }) {
  return (
    <div className="skeleton-table">
      <div className="skeleton-table-header">
        {[...Array(columns)].map((_, i) => (
          <div key={i} className="skeleton skeleton-line" style={{ height: '20px' }}></div>
        ))}
      </div>
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="skeleton-table-row">
          {[...Array(columns)].map((_, j) => (
            <div key={j} className="skeleton skeleton-line" style={{ height: '16px' }}></div>
          ))}
        </div>
      ))}
    </div>
  );
}

export function SkeletonForm() {
  return (
    <div className="skeleton-form">
      <div className="skeleton skeleton-line title" style={{ width: '200px', marginBottom: '2rem' }}></div>
      {[...Array(4)].map((_, i) => (
        <div key={i} className="skeleton-form-group">
          <div className="skeleton skeleton-line" style={{ width: '120px', height: '20px', marginBottom: '0.5rem' }}></div>
          <div className="skeleton skeleton-line" style={{ width: '100%', height: '40px' }}></div>
        </div>
      ))}
      <div className="skeleton skeleton-line" style={{ width: '150px', height: '40px', marginTop: '1rem' }}></div>
    </div>
  );
}

export default Loading;
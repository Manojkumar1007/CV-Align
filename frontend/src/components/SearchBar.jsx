import React, { useState, useEffect } from 'react';
import './SearchBar.css';

function SearchBar({ 
  placeholder = "Search...", 
  onSearch, 
  onFilter, 
  filters = [], 
  className = "",
  debounceMs = 300 
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState({});
  const [showFilters, setShowFilters] = useState(false);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(searchTerm);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [searchTerm, onSearch, debounceMs]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (filterKey, value) => {
    const newFilters = { ...selectedFilters };
    
    if (value === '' || value === 'all') {
      delete newFilters[filterKey];
    } else {
      newFilters[filterKey] = value;
    }
    
    setSelectedFilters(newFilters);
    onFilter(newFilters);
  };

  const handleClearAll = () => {
    setSearchTerm('');
    setSelectedFilters({});
    onSearch('');
    onFilter({});
  };

  const hasActiveFilters = searchTerm || Object.keys(selectedFilters).length > 0;

  return (
    <div className={`search-bar ${className}`}>
      <div className="search-input-wrapper">
        <div className="search-input-container">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder={placeholder}
            value={searchTerm}
            onChange={handleSearchChange}
            className="search-input"
          />
          {searchTerm && (
            <button
              className="clear-search-btn"
              onClick={() => setSearchTerm('')}
              title="Clear search"
            >
              ×
            </button>
          )}
        </div>
        
        {filters.length > 0 && (
          <button
            className={`filter-toggle-btn ${showFilters ? 'active' : ''}`}
            onClick={() => setShowFilters(!showFilters)}
            title="Toggle filters"
          >
            <span className="filter-icon">⚙️</span>
            {Object.keys(selectedFilters).length > 0 && (
              <span className="filter-count">{Object.keys(selectedFilters).length}</span>
            )}
          </button>
        )}
      </div>

      {filters.length > 0 && showFilters && (
        <div className="filters-container">
          <div className="filters-row">
            {filters.map((filter) => (
              <div key={filter.key} className="filter-group">
                <label className="filter-label">{filter.label}</label>
                <select
                  value={selectedFilters[filter.key] || ''}
                  onChange={(e) => handleFilterChange(filter.key, e.target.value)}
                  className="filter-select"
                >
                  <option value="">All {filter.label}</option>
                  {filter.options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
          
          {hasActiveFilters && (
            <div className="filter-actions">
              <button
                className="btn btn-outline clear-filters-btn"
                onClick={handleClearAll}
              >
                Clear All
              </button>
            </div>
          )}
        </div>
      )}

      {hasActiveFilters && (
        <div className="active-filters">
          {searchTerm && (
            <span className="filter-tag">
              Search: "{searchTerm}"
              <button onClick={() => setSearchTerm('')}>×</button>
            </span>
          )}
          {Object.entries(selectedFilters).map(([key, value]) => {
            const filter = filters.find(f => f.key === key);
            const option = filter?.options.find(o => o.value === value);
            return (
              <span key={key} className="filter-tag">
                {filter?.label}: {option?.label || value}
                <button onClick={() => handleFilterChange(key, '')}>×</button>
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
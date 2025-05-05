import React from 'react';
import './AppCard.css';

const AppCard = ({ name, description, status, tags }) => {
  return (
    <div className="app-card">
      <div className="app-card-header">
        <h3>{name}</h3>
        {status && (
          <span className={`app-badge ${status === 'Beta' ? 'app-badge-beta' : 'app-badge-new'}`}>
            {status}
          </span>
        )}
      </div>
      <p className="app-card-description">{description}</p>
      <div className="app-card-details">
        <div className="app-card-tags">
          {tags && tags.map((tag, index) => (
            <span key={index} className="app-tag">{tag}</span>
          ))}
        </div>
        <div className="app-card-actions">
          <button className="app-button">Launch</button>
        </div>
      </div>
    </div>
  );
};

// Default props
AppCard.defaultProps = {
  name: 'App Name',
  description: 'App description goes here',
  status: '',
  tags: []
};

export default AppCard;
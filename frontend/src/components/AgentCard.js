import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AgentCard.css';

function AgentCard({ agent, onUpdate }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/agent/${agent.id}`);
  };

  const getRatingStars = (rating) => {
    if (!rating) return 'No ratings yet';
    const stars = '★'.repeat(Math.round(rating)) + '☆'.repeat(5 - Math.round(rating));
    return `${stars} (${rating.toFixed(1)})`;
  };

  return (
    <div className="agent-card" onClick={handleClick}>
      <div className="agent-card-header">
        <h3>{agent.name}</h3>
        <div className="agent-rating">{getRatingStars(agent.average_rating)}</div>
      </div>
      <p className="agent-description">
        {agent.description || 'No description provided'}
      </p>
      <div className="agent-meta">
        <span className="agent-creator">By: {agent.creator_username}</span>
        <span className="agent-usage">Used: {agent.usage_count} times</span>
      </div>
      {agent.tags && (
        <div className="agent-tags">
          {agent.tags.split(',').map((tag, index) => (
            <span key={index} className="tag">{tag.trim()}</span>
          ))}
        </div>
      )}
    </div>
  );
}

export default AgentCard;

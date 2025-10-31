import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { agentsAPI, ratingsAPI, reviewsAPI } from '../services/api';
import './AgentDetail.css';

function AgentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [agent, setAgent] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState('');
  const [executeInput, setExecuteInput] = useState('{}');
  const [executeResult, setExecuteResult] = useState(null);

  useEffect(() => {
    loadAgent();
    loadReviews();
  }, [id]);

  const loadAgent = async () => {
    try {
      const response = await agentsAPI.get(id);
      setAgent(response.data);
    } catch (error) {
      console.error('Error loading agent:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadReviews = async () => {
    try {
      const response = await reviewsAPI.list(id);
      setReviews(response.data);
    } catch (error) {
      console.error('Error loading reviews:', error);
    }
  };

  const handleFork = async () => {
    try {
      const response = await agentsAPI.fork(id);
      navigate(`/agent/${response.data.id}`);
    } catch (error) {
      alert('Error forking agent: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleRating = async () => {
    try {
      await ratingsAPI.create({ agent_id: parseInt(id), rating });
      loadAgent();
      alert('Rating submitted successfully!');
    } catch (error) {
      alert('Error submitting rating: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleReview = async () => {
    try {
      await reviewsAPI.create({ agent_id: parseInt(id), comment: review });
      setReview('');
      loadReviews();
      alert('Review submitted successfully!');
    } catch (error) {
      alert('Error submitting review: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleExecute = async () => {
    try {
      const inputData = JSON.parse(executeInput);
      const response = await agentsAPI.execute(parseInt(id), inputData);
      setExecuteResult(response.data);
    } catch (error) {
      setExecuteResult({
        success: false,
        error: error.response?.data?.detail || error.message
      });
    }
  };

  if (loading) {
    return <div className="loading">Loading agent...</div>;
  }

  if (!agent) {
    return <div className="error">Agent not found</div>;
  }

  return (
    <div className="agent-detail">
      <div className="agent-header">
        <h1>{agent.name}</h1>
        <div className="agent-actions">
          <button onClick={handleFork} className="btn-secondary">Fork Agent</button>
        </div>
      </div>

      <div className="agent-info">
        <div className="info-row">
          <strong>Creator:</strong> {agent.creator_username}
        </div>
        <div className="info-row">
          <strong>Version:</strong> {agent.version}
        </div>
        <div className="info-row">
          <strong>Usage Count:</strong> {agent.usage_count}
        </div>
        <div className="info-row">
          <strong>Rating:</strong> {agent.average_rating ? `${agent.average_rating.toFixed(1)} / 5.0` : 'No ratings yet'}
        </div>
        {agent.tags && (
          <div className="info-row">
            <strong>Tags:</strong>
            <div className="tags">
              {agent.tags.split(',').map((tag, index) => (
                <span key={index} className="tag">{tag.trim()}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="section">
        <h2>Description</h2>
        <p>{agent.description || 'No description provided'}</p>
      </div>

      <div className="section">
        <h2>Code</h2>
        <pre className="code-block">{agent.code}</pre>
      </div>

      <div className="section">
        <h2>Execute Agent</h2>
        <p>Enter input data as JSON:</p>
        <textarea
          value={executeInput}
          onChange={(e) => setExecuteInput(e.target.value)}
          className="execute-input"
          rows="4"
          placeholder='{"key": "value"}'
        />
        <button onClick={handleExecute} className="btn-primary">Execute</button>
        
        {executeResult && (
          <div className={`execute-result ${executeResult.success ? 'success' : 'error'}`}>
            <h3>{executeResult.success ? 'Output:' : 'Error:'}</h3>
            <pre>{executeResult.success ? executeResult.output : executeResult.error}</pre>
          </div>
        )}
      </div>

      <div className="section">
        <h2>Rate This Agent</h2>
        <div className="rating-form">
          <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
            <option value="1">1 Star</option>
            <option value="2">2 Stars</option>
            <option value="3">3 Stars</option>
            <option value="4">4 Stars</option>
            <option value="5">5 Stars</option>
          </select>
          <button onClick={handleRating} className="btn-primary">Submit Rating</button>
        </div>
      </div>

      <div className="section">
        <h2>Write a Review</h2>
        <textarea
          value={review}
          onChange={(e) => setReview(e.target.value)}
          className="review-input"
          rows="4"
          placeholder="Share your thoughts about this agent..."
        />
        <button onClick={handleReview} className="btn-primary">Submit Review</button>
      </div>

      <div className="section">
        <h2>Reviews ({reviews.length})</h2>
        {reviews.length === 0 ? (
          <p>No reviews yet. Be the first to review!</p>
        ) : (
          <div className="reviews-list">
            {reviews.map((review) => (
              <div key={review.id} className="review-item">
                <div className="review-header">
                  <strong>{review.username}</strong>
                  <span className="review-date">
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p>{review.comment}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AgentDetail;

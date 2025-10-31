import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { agentsAPI } from '../services/api';
import './CreateAgent.css';

function CreateAgent() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    code: '# Your Python code here\n# Use input_data to access input\n# Set result variable for output\n\nresult = "Hello from agent!"',
    tags: '',
    is_public: true
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await agentsAPI.create(formData);
      navigate(`/agent/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create agent');
    }
  };

  return (
    <div className="create-agent">
      <h1>Create New Agent</h1>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="agent-form">
        <div className="form-group">
          <label>Agent Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="e.g., Text Summarizer"
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            placeholder="Describe what your agent does..."
          />
        </div>

        <div className="form-group">
          <label>Agent Code *</label>
          <textarea
            name="code"
            value={formData.code}
            onChange={handleChange}
            rows="15"
            required
            className="code-input"
            placeholder="# Your Python code here"
          />
          <small>
            Tip: Use <code>input_data</code> to access input and set <code>result</code> for output
          </small>
        </div>

        <div className="form-group">
          <label>Tags (comma-separated)</label>
          <input
            type="text"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="e.g., nlp, text-processing, ai"
          />
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="is_public"
              checked={formData.is_public}
              onChange={handleChange}
            />
            Make this agent public
          </label>
        </div>

        <div className="form-actions">
          <button type="button" onClick={() => navigate('/')} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-primary">
            Create Agent
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateAgent;

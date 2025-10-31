import React, { useState, useEffect } from 'react';
import { agentsAPI } from '../services/api';
import AgentCard from '../components/AgentCard';
import './Marketplace.css';

function Marketplace() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [tags, setTags] = useState('');

  useEffect(() => {
    loadAgents();
  }, [search, tags]);

  const loadAgents = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (tags) params.tags = tags;
      
      const response = await agentsAPI.list(params);
      setAgents(response.data);
    } catch (error) {
      console.error('Error loading agents:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="marketplace">
      <div className="marketplace-header">
        <h1>Agent Marketplace</h1>
        <p>Discover, use, and fork AI agents created by the community</p>
      </div>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search agents..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        <input
          type="text"
          placeholder="Filter by tags (comma-separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading">Loading agents...</div>
      ) : (
        <div className="agents-grid">
          {agents.length === 0 ? (
            <p className="no-agents">No agents found. Be the first to create one!</p>
          ) : (
            agents.map(agent => (
              <AgentCard key={agent.id} agent={agent} onUpdate={loadAgents} />
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default Marketplace;

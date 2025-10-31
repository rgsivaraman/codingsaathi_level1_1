import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData);
  },
  getMe: () => api.get('/auth/me'),
};

// Agents API
export const agentsAPI = {
  list: (params) => api.get('/agents/', { params }),
  get: (id) => api.get(`/agents/${id}`),
  create: (data) => api.post('/agents/', data),
  update: (id, data) => api.put(`/agents/${id}`, data),
  delete: (id) => api.delete(`/agents/${id}`),
  fork: (id) => api.post(`/agents/${id}/fork`),
  execute: (agentId, inputData) => api.post('/agents/execute', { agent_id: agentId, input_data: inputData }),
  myAgents: () => api.get('/agents/my-agents'),
};

// Ratings & Reviews API
export const ratingsAPI = {
  create: (data) => api.post('/api/ratings', data),
  list: (agentId) => api.get(`/api/agents/${agentId}/ratings`),
};

export const reviewsAPI = {
  create: (data) => api.post('/api/reviews', data),
  list: (agentId) => api.get(`/api/agents/${agentId}/reviews`),
  update: (id, data) => api.put(`/api/reviews/${id}`, data),
  delete: (id) => api.delete(`/api/reviews/${id}`),
};

export default api;

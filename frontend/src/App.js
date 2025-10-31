import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Marketplace from './pages/Marketplace';
import AgentDetail from './pages/AgentDetail';
import CreateAgent from './pages/CreateAgent';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">Agent Marketplace</Link>
            <div className="nav-menu">
              {isAuthenticated ? (
                <>
                  <Link to="/" className="nav-link">Marketplace</Link>
                  <Link to="/create" className="nav-link">Create Agent</Link>
                  <button onClick={handleLogout} className="nav-link logout-btn">Logout</button>
                </>
              ) : (
                <>
                  <Link to="/login" className="nav-link">Login</Link>
                  <Link to="/register" className="nav-link">Register</Link>
                </>
              )}
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/login" element={
              isAuthenticated ? <Navigate to="/" /> : <Login setIsAuthenticated={setIsAuthenticated} />
            } />
            <Route path="/register" element={
              isAuthenticated ? <Navigate to="/" /> : <Register />
            } />
            <Route path="/" element={
              isAuthenticated ? <Marketplace /> : <Navigate to="/login" />
            } />
            <Route path="/agent/:id" element={
              isAuthenticated ? <AgentDetail /> : <Navigate to="/login" />
            } />
            <Route path="/create" element={
              isAuthenticated ? <CreateAgent /> : <Navigate to="/login" />
            } />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 Agent Marketplace. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

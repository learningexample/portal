import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';

// Import API utilities
import { fetchConfig } from './api/config';

// Import components
import NavBar from './components/NavBar';
import Footer from './components/Footer';

// Import pages
import Dashboard from './pages/Dashboard';
import DepartmentApps from './pages/DepartmentApps';
import AppStore from './pages/AppStore';

function App() {
  const [config, setConfig] = useState({
    company: {},
    departments: [],
    app_store: {},
    user: {}
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Load configuration data when the app starts
    const loadConfig = async () => {
      try {
        setLoading(true);
        const data = await fetchConfig();
        setConfig(data);
      } catch (err) {
        console.error('Error loading configuration:', err);
        setError('Failed to load portal configuration. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadConfig();
  }, []);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Container className="py-5 text-center">
        <h2>Error</h2>
        <p className="text-danger">{error}</p>
        <button
          className="btn btn-primary"
          onClick={() => window.location.reload()}
        >
          Retry
        </button>
      </Container>
    );
  }

  return (
    <Router>
      <div className="app">
        <NavBar
          company={config.company}
          user={config.user}
          departments={config.departments}
        />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard config={config} />} />
            <Route path="/department/:departmentId" element={<DepartmentApps config={config} />} />
            <Route path="/app-store" element={<AppStore appStore={config.app_store} departments={config.departments} />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer company={config.company} />
      </div>
    </Router>
  );
}

export default App;
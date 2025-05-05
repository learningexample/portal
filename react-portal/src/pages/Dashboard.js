import React from 'react';
import { Link } from 'react-router-dom';
import AppCard from '../components/AppCard';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <h1 className="page-title">AI Portal Dashboard</h1>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Apps</h3>
          <p className="stat-value">24</p>
        </div>
        <div className="stat-card">
          <h3>Recent Activity</h3>
          <p className="stat-value">12</p>
        </div>
        <div className="stat-card">
          <h3>Most Popular</h3>
          <p className="stat-value">Text AI</p>
        </div>
      </div>

      <div className="section">
        <div className="section-header">
          <h2>Recent Apps</h2>
          <Link to="/app-store" className="view-all">View All</Link>
        </div>
        <div className="app-grid">
          <AppCard 
            name="Text Generation AI" 
            description="Generate creative and professional text content using our advanced language model."
            status="New"
            tags={['Text', 'Generation', 'GPT']}
          />
          <AppCard 
            name="Image Analysis Tool" 
            description="Analyze and extract insights from images with our computer vision system."
            status="Beta"
            tags={['Vision', 'Analysis', 'Recognition']}
          />
          <AppCard 
            name="Data Visualization App" 
            description="Create interactive charts and graphs from your data."
            tags={['Data', 'Charts', 'Visualization']}
          />
        </div>
      </div>

      <div className="section">
        <div className="section-header">
          <h2>Recommended for You</h2>
        </div>
        <div className="app-grid">
          <AppCard 
            name="AI Financial Assistant" 
            description="Get personalized financial insights and recommendations."
            tags={['Finance', 'Analysis', 'Reports']}
          />
          <AppCard 
            name="Document Summarizer" 
            description="Automatically generate concise summaries of long documents."
            status="New"
            tags={['Documents', 'Summary', 'NLP']}
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
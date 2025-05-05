import React from 'react';
import AppCard from '../components/AppCard';
import './DepartmentApps.css';

const DepartmentApps = () => {
  return (
    <div className="department-apps-container">
      <h1 className="page-title">Department Applications</h1>
      
      <div className="department-selector">
        <div className="department-label">Select Department:</div>
        <div className="department-tabs">
          <button className="department-tab active">Data Science</button>
          <button className="department-tab">Finance</button>
          <button className="department-tab">Marketing</button>
          <button className="department-tab">Operations</button>
          <button className="department-tab">Human Resources</button>
        </div>
      </div>

      <div className="department-content">
        <div className="department-info">
          <h2>Data Science Department</h2>
          <p>Access specialized AI tools and models designed specifically for data analysis, modeling, and visualization.</p>
        </div>

        <div className="section">
          <h3>Department Apps</h3>
          <div className="app-grid">
            <AppCard 
              name="Predictive Analytics Suite" 
              description="Advanced prediction models and forecasting tools."
              status="Beta"
              tags={['Analytics', 'Prediction', 'Models']}
            />
            <AppCard 
              name="Data Cleaner Pro" 
              description="Automated tools for cleaning and preprocessing data."
              tags={['Data', 'Preprocessing', 'Automation']}
            />
            <AppCard 
              name="Neural Network Builder" 
              description="Visual tool for building and training neural networks without coding."
              status="New"
              tags={['Neural Networks', 'No-Code', 'ML']}
            />
          </div>
        </div>

        <div className="section">
          <h3>Department Dashboards</h3>
          <div className="dashboard-list">
            <div className="dashboard-item">
              <div className="dashboard-info">
                <h4>Project Performance Dashboard</h4>
                <p>Track and analyze all current data science projects and their KPIs.</p>
              </div>
              <button className="view-button">View</button>
            </div>
            <div className="dashboard-item">
              <div className="dashboard-info">
                <h4>Model Monitoring</h4>
                <p>Track the performance of deployed models in production.</p>
              </div>
              <button className="view-button">View</button>
            </div>
            <div className="dashboard-item">
              <div className="dashboard-info">
                <h4>Resource Allocation</h4>
                <p>Overview of compute resources and utilization across projects.</p>
              </div>
              <button className="view-button">View</button>
            </div>
          </div>
        </div>

        <div className="section">
          <h3>Recent Documents</h3>
          <div className="documents-list">
            <div className="document-item">
              <div className="document-icon">📄</div>
              <div className="document-info">
                <h4>Q2 Data Science Strategy</h4>
                <p>Updated 2 days ago</p>
              </div>
            </div>
            <div className="document-item">
              <div className="document-icon">📊</div>
              <div className="document-info">
                <h4>Model Evaluation Results - April 2025</h4>
                <p>Updated 1 week ago</p>
              </div>
            </div>
            <div className="document-item">
              <div className="document-icon">📁</div>
              <div className="document-info">
                <h4>Training Data Repository Guidelines</h4>
                <p>Updated 3 weeks ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DepartmentApps;
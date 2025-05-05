import { Component } from '@angular/core';

@Component({
  selector: 'app-department-apps',
  template: `
    <div class="department-apps">
      <h1 class="page-title">Department Applications</h1>
      
      <div class="department-selector">
        <div class="department-label">Select Department:</div>
        <div class="department-tabs">
          <button class="department-tab active">Data Science</button>
          <button class="department-tab">Finance</button>
          <button class="department-tab">Marketing</button>
          <button class="department-tab">Operations</button>
          <button class="department-tab">Human Resources</button>
        </div>
      </div>

      <div class="department-content">
        <div class="department-info">
          <h2>Data Science Department</h2>
          <p>Access specialized AI tools and models designed specifically for data analysis, modeling, and visualization.</p>
        </div>

        <div class="section">
          <h3>Department Apps</h3>
          <div class="app-grid">
            <app-card 
              name="Predictive Analytics Suite" 
              description="Advanced prediction models and forecasting tools."
              status="Beta"
              [tags]="['Analytics', 'Prediction', 'Models']"
            ></app-card>
            <app-card 
              name="Data Cleaner Pro" 
              description="Automated tools for cleaning and preprocessing data."
              status=""
              [tags]="['Data', 'Preprocessing', 'Automation']"
            ></app-card>
            <app-card 
              name="Neural Network Builder" 
              description="Visual tool for building and training neural networks without coding."
              status="New"
              [tags]="['Neural Networks', 'No-Code', 'ML']"
            ></app-card>
          </div>
        </div>

        <div class="section">
          <h3>Department Dashboards</h3>
          <div class="dashboard-list">
            <div class="dashboard-item">
              <div class="dashboard-info">
                <h4>Project Performance Dashboard</h4>
                <p>Track and analyze all current data science projects and their KPIs.</p>
              </div>
              <button class="view-button">View</button>
            </div>
            <div class="dashboard-item">
              <div class="dashboard-info">
                <h4>Model Monitoring</h4>
                <p>Track the performance of deployed models in production.</p>
              </div>
              <button class="view-button">View</button>
            </div>
            <div class="dashboard-item">
              <div class="dashboard-info">
                <h4>Resource Allocation</h4>
                <p>Overview of compute resources and utilization across projects.</p>
              </div>
              <button class="view-button">View</button>
            </div>
          </div>
        </div>

        <div class="section">
          <h3>Recent Documents</h3>
          <div class="documents-list">
            <div class="document-item">
              <div class="document-icon">📄</div>
              <div class="document-info">
                <h4>Q2 Data Science Strategy</h4>
                <p>Updated 2 days ago</p>
              </div>
            </div>
            <div class="document-item">
              <div class="document-icon">📊</div>
              <div class="document-info">
                <h4>Model Evaluation Results - April 2025</h4>
                <p>Updated 1 week ago</p>
              </div>
            </div>
            <div class="document-item">
              <div class="document-icon">📁</div>
              <div class="document-info">
                <h4>Training Data Repository Guidelines</h4>
                <p>Updated 3 weeks ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .department-apps {
      padding: 20px 0;
    }
    .page-title {
      margin-bottom: 30px;
      font-size: 2rem;
      color: #2c3e50;
    }
    .department-selector {
      margin-bottom: 30px;
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      align-items: center;
    }
    .department-label {
      font-weight: bold;
      color: #555;
    }
    .department-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .department-tab {
      padding: 8px 16px;
      background-color: #f0f0f0;
      border: none;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .department-tab.active, .department-tab:hover {
      background-color: #3498db;
      color: white;
    }
    .department-content {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 25px;
    }
    .department-info {
      margin-bottom: 30px;
    }
    .department-info h2 {
      margin: 0 0 10px 0;
      color: #2c3e50;
    }
    .department-info p {
      color: #555;
      margin: 0;
    }
    .section {
      margin-bottom: 30px;
    }
    .section h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 1.3rem;
      color: #2c3e50;
      border-bottom: 1px solid #eee;
      padding-bottom: 8px;
    }
    .app-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    .dashboard-list, .documents-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .dashboard-item, .document-item {
      display: flex;
      align-items: center;
      background-color: white;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    .dashboard-info, .document-info {
      flex: 1;
    }
    .dashboard-info h4, .document-info h4 {
      margin: 0 0 5px 0;
      font-size: 1.1rem;
    }
    .dashboard-info p, .document-info p {
      margin: 0;
      color: #777;
      font-size: 0.9rem;
    }
    .view-button {
      background-color: #3498db;
      color: white;
      border: none;
      padding: 6px 15px;
      border-radius: 4px;
      cursor: pointer;
    }
    .view-button:hover {
      background-color: #2980b9;
    }
    .document-icon {
      font-size: 1.5rem;
      margin-right: 15px;
    }
  `]
})
export class DepartmentAppsComponent {}
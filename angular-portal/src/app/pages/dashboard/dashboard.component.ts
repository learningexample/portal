import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  template: `
    <div class="dashboard">
      <h1 class="page-title">AI Portal Dashboard</h1>
      
      <div class="dashboard-stats">
        <div class="stat-card">
          <h3>Total Apps</h3>
          <p class="stat-value">24</p>
        </div>
        <div class="stat-card">
          <h3>Recent Activity</h3>
          <p class="stat-value">12</p>
        </div>
        <div class="stat-card">
          <h3>Most Popular</h3>
          <p class="stat-value">Text AI</p>
        </div>
      </div>

      <div class="section">
        <div class="section-header">
          <h2>Recent Apps</h2>
          <a routerLink="/app-store" class="view-all">View All</a>
        </div>
        <div class="app-grid">
          <app-card 
            name="Text Generation AI" 
            description="Generate creative and professional text content using our advanced language model."
            status="New"
            [tags]="['Text', 'Generation', 'GPT']"
          ></app-card>
          <app-card 
            name="Image Analysis Tool" 
            description="Analyze and extract insights from images with our computer vision system."
            status="Beta"
            [tags]="['Vision', 'Analysis', 'Recognition']"
          ></app-card>
          <app-card 
            name="Data Visualization App" 
            description="Create interactive charts and graphs from your data."
            status=""
            [tags]="['Data', 'Charts', 'Visualization']"
          ></app-card>
        </div>
      </div>

      <div class="section">
        <div class="section-header">
          <h2>Recommended for You</h2>
        </div>
        <div class="app-grid">
          <app-card 
            name="AI Financial Assistant" 
            description="Get personalized financial insights and recommendations."
            status=""
            [tags]="['Finance', 'Analysis', 'Reports']"
          ></app-card>
          <app-card 
            name="Document Summarizer" 
            description="Automatically generate concise summaries of long documents."
            status="New"
            [tags]="['Documents', 'Summary', 'NLP']"
          ></app-card>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard {
      padding: 20px 0;
      max-width: 1200px;
      margin: 0 auto;
    }
    .page-title {
      margin-bottom: 30px;
      font-size: 2rem;
      color: #2c3e50;
    }
    .dashboard-stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .stat-card {
      background-color: #f8f9fa;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
      text-align: center;
    }
    .stat-card h3 {
      margin: 0;
      font-size: 1rem;
      color: #555;
      margin-bottom: 10px;
    }
    .stat-value {
      font-size: 1.8rem;
      font-weight: bold;
      color: #2c3e50;
      margin: 0;
    }
    .section {
      margin-bottom: 40px;
    }
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .section-header h2 {
      margin: 0;
      font-size: 1.5rem;
      color: #2c3e50;
    }
    .view-all {
      color: #3498db;
      text-decoration: none;
    }
    .view-all:hover {
      text-decoration: underline;
    }
    .app-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
  `]
})
export class DashboardComponent {}
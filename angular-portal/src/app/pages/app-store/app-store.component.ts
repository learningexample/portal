import { Component } from '@angular/core';

@Component({
  selector: 'app-app-store',
  template: `
    <div class="app-store">
      <div class="app-store-banner">
        <div class="banner-content">
          <h1>AI App Store</h1>
          <p>Discover and access all available AI tools and applications</p>
          <div class="search-bar">
            <input type="text" placeholder="Search apps..." />
            <button class="search-button">Search</button>
          </div>
        </div>
      </div>

      <div class="app-categories">
        <button class="category-button active">All</button>
        <button class="category-button">Natural Language</button>
        <button class="category-button">Computer Vision</button>
        <button class="category-button">Data Analysis</button>
        <button class="category-button">Automation</button>
      </div>

      <div class="filter-options">
        <div class="filter-group">
          <label>Sort by:</label>
          <select>
            <option>Newest</option>
            <option>Most Popular</option>
            <option>Alphabetical</option>
          </select>
        </div>
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
        <app-card 
          name="Voice Transcription" 
          description="Convert speech to text with high accuracy."
          status=""
          [tags]="['Audio', 'Transcription', 'Speech']"
        ></app-card>
        <app-card 
          name="Sentiment Analyzer" 
          description="Analyze text to determine sentiment and emotional tone."
          status="Beta"
          [tags]="['NLP', 'Sentiment', 'Analysis']"
        ></app-card>
        <app-card 
          name="Code Generator" 
          description="Generate code snippets from natural language descriptions."
          status="New"
          [tags]="['Code', 'Generation', 'Programming']"
        ></app-card>
      </div>
    </div>
  `,
  styles: [`
    .app-store {
      padding-bottom: 40px;
    }
    .app-store-banner {
      background-color: #3498db;
      background-image: linear-gradient(135deg, #3498db, #2c3e50);
      color: white;
      border-radius: 8px;
      padding: 50px;
      margin-bottom: 30px;
      position: relative;
      overflow: hidden;
    }
    .banner-content {
      position: relative;
      z-index: 1;
    }
    .app-store-banner h1 {
      margin: 0;
      margin-bottom: 10px;
      font-size: 2.5rem;
    }
    .app-store-banner p {
      margin: 0;
      margin-bottom: 20px;
      font-size: 1.1rem;
      opacity: 0.9;
    }
    .search-bar {
      display: flex;
      max-width: 500px;
    }
    .search-bar input {
      flex: 1;
      padding: 12px 15px;
      border: none;
      border-radius: 4px 0 0 4px;
      font-size: 1rem;
      outline: none;
    }
    .search-button {
      background-color: #2ecc71;
      color: white;
      border: none;
      border-radius: 0 4px 4px 0;
      padding: 0 20px;
      font-weight: bold;
      cursor: pointer;
    }
    .search-button:hover {
      background-color: #27ae60;
    }
    .app-categories {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }
    .category-button {
      background-color: #f0f0f0;
      border: none;
      border-radius: 20px;
      padding: 8px 16px;
      font-size: 0.9rem;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .category-button.active, .category-button:hover {
      background-color: #3498db;
      color: white;
    }
    .filter-options {
      display: flex;
      justify-content: flex-end;
      margin-bottom: 20px;
    }
    .filter-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .filter-group select {
      padding: 8px;
      border-radius: 4px;
      border: 1px solid #ddd;
    }
    .app-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
  `]
})
export class AppStoreComponent {}
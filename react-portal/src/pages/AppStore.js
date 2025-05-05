import React from 'react';
import AppCard from '../components/AppCard';
import './AppStore.css';

const AppStore = () => {
  return (
    <div className="app-store-container">
      <div className="app-store-banner">
        <div className="banner-content">
          <h1>AI App Store</h1>
          <p>Discover and access all available AI tools and applications</p>
          <div className="search-bar">
            <input type="text" placeholder="Search apps..." />
            <button className="search-button">Search</button>
          </div>
        </div>
      </div>

      <div className="app-categories">
        <button className="category-button active">All</button>
        <button className="category-button">Natural Language</button>
        <button className="category-button">Computer Vision</button>
        <button className="category-button">Data Analysis</button>
        <button className="category-button">Automation</button>
      </div>

      <div className="filter-options">
        <div className="filter-group">
          <label>Sort by:</label>
          <select>
            <option>Newest</option>
            <option>Most Popular</option>
            <option>Alphabetical</option>
          </select>
        </div>
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
        <AppCard 
          name="Voice Transcription" 
          description="Convert speech to text with high accuracy."
          tags={['Audio', 'Transcription', 'Speech']}
        />
        <AppCard 
          name="Sentiment Analyzer" 
          description="Analyze text to determine sentiment and emotional tone."
          status="Beta"
          tags={['NLP', 'Sentiment', 'Analysis']}
        />
        <AppCard 
          name="Code Generator" 
          description="Generate code snippets from natural language descriptions."
          status="New"
          tags={['Code', 'Generation', 'Programming']}
        />
      </div>
    </div>
  );
};

export default AppStore;
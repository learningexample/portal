import axios from 'axios';

// API endpoint for configuration data
const CONFIG_ENDPOINT = '/api/config';

/**
 * Fetches the portal configuration from the backend
 * @returns {Promise<Object>} The configuration object
 */
export const fetchConfig = async () => {
  try {
    // In a real implementation, this would fetch from your API
    // For now, we'll use a mock implementation that can later connect to your backend
    
    // Option 1: Connect to your existing Dash backend via proxy
    // const response = await axios.get(CONFIG_ENDPOINT);
    // return response.data;
    
    // Option 2: Mock data for development
    return {
      company: {
        name: 'Enterprise',
        logo_url: '/assets/images/logo.svg',
        theme_color: '#4a6fa5',
        copyright_year: '2025'
      },
      title: 'AI Portal',
      description: 'Central portal for departmental AI applications',
      departments: [
        {
          name: 'Finance',
          icon: 'fa-solid fa-chart-line',
          description: 'Financial AI tools and applications',
          apps: [
            {
              name: 'Financial Analysis',
              description: 'AI-powered financial analysis tool that provides insights into company performance',
              icon: 'fa-solid fa-money-bill-trend-up',
              url: '#',
              contact: 'finance-support@example.com'
            },
            {
              name: 'Risk Management',
              description: 'Evaluate financial risks using advanced machine learning algorithms',
              icon: 'fa-solid fa-shield-halved',
              url: '#',
              contact: 'risk@example.com'
            }
          ]
        },
        {
          name: 'Marketing',
          icon: 'fa-solid fa-bullhorn',
          description: 'Marketing automation and analytics tools',
          apps: [
            {
              name: 'Campaign Optimizer',
              description: 'AI-driven marketing campaign optimization that increases conversion rates',
              icon: 'fa-solid fa-rocket',
              url: '#',
              contact: 'marketing@example.com'
            },
            {
              name: 'Customer Segmentation',
              description: 'Intelligent customer segmentation based on behavior patterns',
              icon: 'fa-solid fa-users-gear',
              url: '#'
            }
          ]
        },
        {
          name: 'IT',
          icon: 'fa-solid fa-network-wired',
          description: 'IT infrastructure and support applications',
          apps: [
            {
              name: 'Network Monitor',
              description: 'AI-powered network monitoring and anomaly detection',
              icon: 'fa-solid fa-wifi',
              url: '#',
              contact: 'support@example.com'
            },
            {
              name: 'Security Scanner',
              description: 'Automated security scanning and vulnerability assessment',
              icon: 'fa-solid fa-shield-virus',
              url: '#'
            }
          ]
        }
      ],
      app_store: {
        title: 'AI App Store',
        icon: 'fa-solid fa-store',
        description: 'Discover and install the latest AI applications',
        banner_image: '/assets/images/app-store-banner.svg',
        apps: [
          {
            name: 'Document AI',
            description: 'Extract insights from documents with our advanced OCR and NLP',
            icon: 'fa-solid fa-file-lines',
            url: '#',
            contact: 'docai@example.com'
          },
          {
            name: 'Chatbot Assistant',
            description: 'Customer service automation with AI-powered chatbots',
            icon: 'fa-solid fa-comments',
            url: '#'
          },
          {
            name: 'Data Visualization',
            description: 'Advanced data visualization with AI-powered insights',
            icon: 'fa-solid fa-chart-pie',
            url: '#',
            contact: 'datavis@example.com'
          }
        ]
      },
      user: {
        name: 'John Doe',
        role: 'Administrator',
        avatar_url: '/assets/images/user-avatar.svg'
      }
    };
  } catch (error) {
    console.error('Error fetching configuration:', error);
    throw error;
  }
};
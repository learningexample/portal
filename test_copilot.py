"""
Test file to validate GitHub Copilot instructions.

This file is meant to test if GitHub Copilot correctly understands
the global instructions we've set up for the portal project.
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import os
import yaml
import logging
import sys

# Configure logging similar to app_bytab.py
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('test_copilot')

# Load configuration using the standard pattern in our project
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Config loaded successfully with {len(config.keys())} top level keys")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}

# Initialize a test Dash app with our project patterns
def create_test_app():
    # Load configuration
    config = load_config()
    company_info = config.get('company', {})
    
    # Create app with standard settings
    app_title = f"{company_info.get('name', 'Enterprise')} AI Portal (Test)" 
    app = dash.Dash(
        __name__, 
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        ],
        meta_tags=[
            {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'},
            {'name': 'description', 'content': 'Test app for Copilot instructions'}
        ],
        title=app_title,
        url_base_pathname="/test/"
    )
    
    # Create a basic layout
    app.layout = html.Div([
        dbc.Container([
            html.H1("Copilot Instructions Test"),
            html.P("This application tests if Copilot correctly understands our project structure"),
            dbc.Button("Test Button", color="primary")
        ])
    ])
    
    # Expose server for Gunicorn
    server = app.server
    
    return app

# Main entry point
if __name__ == "__main__":
    # Get port from environment variable with default as per our guidelines
    port = int(os.environ.get('PORT', 8050))
    
    # Create the test app
    app = create_test_app()
    
    # Run server with standard settings for Docker
    app.run_server(debug=False, host='0.0.0.0', port=port)
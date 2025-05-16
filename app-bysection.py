"""
Enterprise AI Portal - Collapsible Sections Version (app-bysection.py)

A Dash-based web application that provides a centralized portal for accessing
various AI applications organized by department/category. Features collapsible
sections and responsive design.

Uses Flask server exposed as 'server' for Gunicorn integration
with multiple workers in production.
"""

import os
import sys
import json
import yaml
import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc
import time
from datetime import datetime

# Import logging utilities
from utils.log import get_logger, log_activity, log_performance, log_button_click

# Set up logger for this application
logger = get_logger('app_bysection')
logger.info("Starting Enterprise AI Portal - Collapsible Sections Version")

# --- Configuration Management ---

def load_config():
    """
    Load configuration from YAML file with fallbacks for missing sections.
    Returns a dictionary with configuration settings.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    start_time = time.time()
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # Validate essential configuration sections
        required_sections = ['company', 'departments']
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            logger.warning(f"Missing required sections in config.yaml: {', '.join(missing_sections)}")
            logger.warning("Using default values for missing sections.")
            
            # Add default values for missing sections
            if 'company' not in config:
                config['company'] = {'name': 'Enterprise', 'logo_url': 'assets/images/logo.svg', 'theme_color': '#4a6fa5'}
            if 'departments' not in config:
                config['departments'] = []
        
        execution_time = time.time() - start_time
        log_performance("load_config", execution_time)
        logger.info(f"Configuration loaded successfully in {execution_time:.4f}s")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        logger.warning("Using default configuration.")
        return {
            'company': {'name': 'Enterprise', 'logo_url': 'assets/images/logo.svg', 'theme_color': '#4a6fa5'},
            'departments': []
        }
    except yaml.YAMLError as e:
        logger.critical(f"Error parsing YAML configuration: {e}")
        sys.exit(1)  # Exit if YAML is malformed - critical error
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        return {}

# Load and validate configuration
config = load_config()

# Company and user information with fallbacks to ensure UI won't break
company_info = config.get('company', {})
user_info = config.get('user', {})

# Initialize the app with a Bootstrap theme and Font Awesome icons
app_title = f"{company_info.get('name', 'Enterprise')} AI Portal" 
dash_app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
                ],
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'},
                    {'name': 'description', 'content': f"{company_info.get('name', 'Enterprise')} AI Portal for accessing departmental AI applications"}
                ],
                title=app_title,
                update_title=f"Loading {app_title}...",
                url_base_pathname="/AppStore/",  # Add trailing slash back
                suppress_callback_exceptions=True)  # Add this to suppress callback exceptions

# Add favicon - explicitly set to override Dash default
dash_app._favicon = None  # Disable default Dash favicon

# Add our own favicon and localStorage script to the index template
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg">
        <link rel="shortcut icon" type="image/x-icon" href="/assets/favicon.ico">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

dash_app.index_string = index_string
server = dash_app.server  # for deployment purposes

# Get departments from config
categories = [dept['name'] for dept in config.get('departments', [])]

# Create a dictionary of apps for each department/category
apps = {}
for dept in config.get('departments', []):
    dept_name = dept['name']
    apps[dept_name] = dept.get('apps', [])

# Add app store apps
app_store = config.get('app_store', {})
app_store_title = app_store.get('title', "AI App Store")
app_store_icon = app_store.get('icon', "fa-solid fa-store")
app_store_description = app_store.get('description', "Discover and install the latest AI applications")
apps['App Store'] = app_store.get('apps', [])

# Get department descriptions
dept_descriptions = {}
for dept in config.get('departments', []):
    dept_descriptions[dept['name']] = dept.get('description', "")

# Icon color mapping for different departments
# Get department colors from config
icon_colors = config.get('department_colors', {})
# Set default fallback color
default_color = icon_colors.get('default', '#4a6fa5')

# App-specific icon color mapping
app_icon_colors = {
    # Business Operations
    'Financial Analysis': '#43A047',
    'Supply Chain Optimizer': '#1B5E20',
    'Process Automation': '#388E3C',
    'Predictive Analytics': '#2E7D32',
    'Risk Management': '#1E8449',
    
    # Software Development
    'Code Generator': '#D32F2F',
    'Bug Predictor': '#B71C1C',
    'API Designer': '#C62828',
    'DevOps Automator': '#D81B60',
    'Performance Analyzer': '#AD1457',
    
    # IT Operations
    'Network Monitor': '#1976D2',
    'Security Scanner': '#0D47A1',
    'Cloud Cost Optimizer': '#1565C0',
    'Incident Responder': '#0288D1',
    'System Health Dashboard': '#0097A7',
    
    # Individual Productivity
    'Meeting Summarizer': '#8E24AA',
    'Smart Calendar': '#4A148C',
    'Email Assistant': '#6A1B9A',
    'Document Generator': '#7B1FA2',
    'Knowledge Assistant': '#9C27B0',
    
    # HR
    'Candidate Matcher': '#F57C00',
    'Employee Sentiment Analyzer': '#EF6C00',
    'Training Recommender': '#E65100',
    'Performance Predictor': '#FF8F00',
    'Retention Analyzer': '#F9A825',
    
    # App Store
    'Document AI': '#00ACC1',
    'Chatbot Assistant': '#00838F',
    'Data Visualization': '#00695C',
    'Text Analyzer': '#1E88E5',
    'Image Generator': '#039BE5',
    'Voice Assistant': '#0277BD',
}

# Helper functions for handling contact information
def has_contact_info(app):
    """
    Check if an app has any type of contact information.
    
    Args:
        app (dict): The application configuration dictionary
        
    Returns:
        bool: True if any contact information exists, False otherwise
    """
    return app.get('contact_url') or app.get('contact') or app.get('contact_email') or app.get('email')

def get_contact_href(app):
    """
    Get the appropriate href value for the contact button.
    
    Handles different types of contact information with proper formatting:
    - URLs are used directly
    - Email addresses get mailto: prefix
    - Other contact info is used as-is
    
    Args:
        app (dict): The application configuration dictionary
        
    Returns:
        str: Formatted contact href value for the button
    """
    # First check for the combined contact field
    if app.get('contact'):
        if app.get('contact').startswith(('http://', 'https://', 'mailto:')):
            return app.get('contact')
        elif '@' in app.get('contact', '') and '.' in app.get('contact', '').split('@')[1]:
            return f"mailto:{app.get('contact')}"
        return app.get('contact')
    
    # Fallback to separate fields for backward compatibility
    if app.get('contact_url'):
        return app.get('contact_url')
    if app.get('contact_email'):
        return f"mailto:{app.get('contact_email')}"
    if app.get('email'):
        return f"mailto:{app.get('email')}"    
    return "#"

def get_contact_display(app):
    """
    Get a display-friendly representation of contact information for an app.
    
    Args:
        app (dict): The application configuration dictionary
        
    Returns:
        str: Human-readable contact information for display
    """
    if app.get('contact_email'):
        return app.get('contact_email')
    elif app.get('email'):
        return app.get('email')
    elif app.get('contact') and '@' in app.get('contact', ''):
        return app.get('contact')
    elif app.get('contact'):
        return app.get('contact')
    elif app.get('contact_url'):
        # Get domain from URL for display
        from urllib.parse import urlparse
        parsed_url = urlparse(app.get('contact_url'))
        return parsed_url.netloc or "Support Portal"
    
    return "Unknown"

# Create the app cards with colorful icons
def create_app_cards(dept):
    """
    Create application cards for a specific department.
    
    Args:
        dept (str): Department name to generate cards for
        
    Returns:
        list: List of dbc.Card components for the specified department
    """
    cards = []
    for app in apps.get(dept, []):
        icon = app.get('icon', 'fa-solid fa-cube')  # Default icon if none specified
        business_area = app.get('business_area', 'All')  # Get business area or default to 'All'
        
        # Set icon color based on app name or fall back to department color
        icon_color = app_icon_colors.get(app['name'], icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5')))
        
        # Define business area badge styling based on the area
        badge_styles = {
            'All': {
                'icon': 'fa-solid fa-globe',
                'bg': '#0D47A1',
                'color': '#FFFFFF'
            },
            'IA': {
                'icon': 'fa-solid fa-piggy-bank',
                'bg': '#7B1FA2',
                'color': '#FFFFFF'
            },
            'Direct': {
                'icon': 'fa-solid fa-arrow-right',
                'bg': '#1B5E20',
                'color': '#FFFFFF'
            },
            'GMAD': {
                'icon': 'fa-solid fa-chart-line',
                'bg': '#E65100',
                'color': '#FFFFFF'
            },
            'Marketing': {
                'icon': 'fa-solid fa-bullhorn',
                'bg': '#C62828',
                'color': '#FFFFFF'
            },
            'Cross-NYLI': {
                'icon': 'fa-solid fa-shuffle',
                'bg': '#00695C',
                'color': '#FFFFFF'
            }
        }
        
        # Get the badge style for the current business area
        badge_style = badge_styles.get(business_area, badge_styles['All'])
        
        # Create enhanced business area badge with icon
        business_badge = html.Div(
            html.Span([
                html.I(className=f"{badge_style['icon']} me-1"),
                business_area
            ], className="badge rounded-pill"),
            className="position-absolute top-0 end-0 m-2",
            style={
                "zIndex": "1", 
                "backgroundColor": badge_style['bg'], 
                "color": badge_style['color'], 
                "fontWeight": "500",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.15)",
                "padding": "0.35em 0.6em",
                "fontSize": "0.8rem",
                "display": "flex",
                "alignItems": "center",
                "gap": "4px"
            }
        )
        
        # Check if the app has a valid URL and contact information
        has_url = 'url' in app and app.get('url') and app.get('url').strip()
        has_contact = has_contact_info(app)
        
        # Create the button(s) based on what information is available
        buttons = []
        
        # Add Launch App button if URL is available, otherwise show a "Coming Soon" greyed out button
        if has_url:
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-external-link-alt me-2"),
                    "Launch App"
                ], color="primary", href=app['url'], className="me-2 flex-grow-1", target="_blank", 
                   style={"borderRadius": "6px", "fontWeight": "500", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"})
            )
        else:
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-hourglass-half me-2"),
                    "Coming Soon"
                ], color="secondary", disabled=True, className="me-2 flex-grow-1",
                   style={"borderRadius": "6px", "fontWeight": "500", "opacity": "0.65"})
            )
        
        # Always add Contact button - active if contact info is available, disabled if not
        if has_contact:
            contact_href = get_contact_href(app)
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-comment me-2"),
                    "Contact"
                ], color="info", href=contact_href, className="flex-grow-1", target="_blank",
                   style={"borderRadius": "6px", "fontWeight": "500", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"})
            )
        else:
            # Disabled Contact button when no contact info is available
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-comment me-2"),
                    "Contact"
                ], color="secondary", disabled=True, className="flex-grow-1",
                   style={"borderRadius": "6px", "fontWeight": "500", "opacity": "0.65"})
            )
          # Create the card with all components
        card = dbc.Card([
            # Add business area badge
            business_badge,
              dbc.CardBody([
                # Card content container with flex display                html.Div([
                    # Header section with app icon and name
                    html.Div([
                        html.Div([html.I(className=f"{icon} fa-2x", style={"color": icon_color})], 
                                 className="me-3", 
                                 style={"width": "45px", "height": "45px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                        html.H5(app['name'], className="card-title mb-0", style={"fontWeight": "600"})
                    ], className="d-flex align-items-center mb-3"),
                      # Description section - will stretch to fill available space
                    html.Div([
                        html.P(app['description'], className="card-text", style={"fontSize": "0.95rem", "lineHeight": "1.5"})
                    ], className="mb-3"),                    # App details unordered list
                    html.Div([
                        html.H6("App Details", className="mt-1 mb-2", style={"fontSize": "0.9rem", "fontWeight": "600", "color": "#555"}),
                        html.Ul([
                            html.Li([
                                html.Strong("Category: ", style={"color": "#555"}), 
                                html.Span(dept)
                            ], style={"fontSize": "0.85rem", "marginBottom": "4px"}),
                            html.Li([
                                html.Strong("Business: ", style={"color": "#555"}), 
                                html.Span(business_area)
                            ], style={"fontSize": "0.85rem", "marginBottom": "4px"}),                            html.Li([
                                html.Strong("Contact: ", style={"color": "#555"}), 
                                html.Span(get_contact_display(app) if has_contact else "Not Available")
                            ], style={"fontSize": "0.85rem", "marginBottom": "4px"}),                            html.Li([
                                html.Strong("Phase: ", style={"color": "#555"}), 
                                html.Span(app.get('phase', "Production" if has_url else "Development"))
                            ], style={"fontSize": "0.85rem"})                        ], className="ps-3 mb-3", style={
                            "listStyleType": "disc", 
                            "backgroundColor": "#f8f9fa", 
                            "padding": "8px 10px 8px 25px", 
                            "borderRadius": "6px", 
                            "borderLeft": "3px solid #dee2e6",
                            "marginTop": "5px",
                            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"
                        })
                    ], className="flex-grow-1"),
                    
                    # Button section - always at the bottom
                    html.Div([
                        # Display buttons in a row, if any
                        html.Div(buttons, className="d-flex")
                    ])                ], className="d-flex flex-column h-100") # Make the div take full height of card
            ])
        ], className="mb-4 h-100 position-relative shadow-sm", 
           style={
               "transition": "all 0.2s ease-in-out",
               "borderRadius": "8px",
               "overflow": "hidden", 
               "border": "1px solid #e9ecef",
               "minHeight": "380px"  # Set minimum height to accommodate the new list
           })  
        cards.append(card)
    return cards

# User profile dropdown
user_dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem([
            html.Div([
                html.Img(src=user_info.get('avatar_url', ''), className="rounded-circle me-2", width=30, height=30),
                html.Span(user_info.get('name', 'User')),
            ], className="d-flex align-items-center")
        ], header=True),
        dbc.DropdownMenuItem(user_info.get('role', 'User'), header=True),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem([html.I(className="fas fa-user me-2"), "Profile"]),
        dbc.DropdownMenuItem([html.I(className="fas fa-cog me-2"), "Settings"]),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem([html.I(className="fas fa-sign-out-alt me-2"), "Sign Out"]),
    ],
    nav=True,
    in_navbar=True,
    label="",
    toggle_style={"color": "transparent", "background": "transparent", "border": "none"},
    toggleClassName="p-0",
    align_end=True,
)

# Define business area styles for consistent appearance
business_area_styles = {
    'Direct': {
        'icon': 'fa-solid fa-handshake',
        'bg': '#1B5E20',
        'color': '#FFFFFF'
    },
    'GBS': {
        'icon': 'fa-solid fa-globe',
        'bg': '#0D47A1',
        'color': '#FFFFFF'
    },
    'GMAD': {
        'icon': 'fa-solid fa-industry',
        'bg': '#E65100',
        'color': '#FFFFFF'
    },
    'IA': {
        'icon': 'fa-solid fa-piggy-bank',
        'bg': '#7B1FA2',
        'color': '#FFFFFF'
    },
    'NYLIM': {
        'icon': 'fa-solid fa-chart-line',
        'bg': '#00695C',
        'color': '#FFFFFF'
    }
}

# Extract all unique business areas from the apps
business_areas = set()
for dept_name, dept_apps in apps.items():
    for app in dept_apps:
        if 'business_area' in app:
            business_areas.add(app['business_area'])

# Convert to sorted list
business_areas = sorted(list(business_areas))

# Top Navigation Bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Company Logo and Brand
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=company_info.get('logo_url', ''), height="40px"), className="me-2"),
                        dbc.Col(dbc.NavbarBrand(company_info.get('name', config.get('title', "AI Portal")), 
                                               className="ms-2", 
                                               style={"fontWeight": "600", "color": "#1565C0"})),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", style={"border": "none", "boxShadow": "none"}),
            dbc.Collapse(
                dbc.Nav(
                    [
                        # Hello User greeting
                        dbc.NavItem(
                            html.Div(
                                [
                                    html.I(className="fa-solid fa-user-circle me-2"),
                                    html.Span(f"Hello {user_info.get('name', 'User')}"),
                                ],
                                className="nav-link",
                                style={"fontWeight": "500", "color": "#4a6fa5"},
                            ),
                            className="d-flex align-items-center me-3"
                        ),
                        # Category navigation menu with properly formatted href links
                        dbc.DropdownMenu(
                            [dbc.DropdownMenuItem(
                                [html.I(className=f"{config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')} me-2"), dept], 
                                href=f"#{dept.lower().replace(' ', '-')}",  # Ensure spaces are replaced with hyphens
                                style={"transition": "background-color 0.2s ease", "padding": "0.6rem 1rem"}
                             ) for i, dept in enumerate(categories)],
                            label=html.Span([html.I(className="fa-solid fa-th-large me-2"), "Categories"]),
                            nav=True,
                            className="mx-2",
                            style={"fontWeight": "500"},
                            toggle_style={"borderRadius": "6px", "padding": "0.5rem 1rem"}
                        ),
                        # User profile dropdown
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem([
                                    html.Div([
                                        html.Img(src=user_info.get('avatar_url', ''), className="rounded-circle me-2", width=30, height=30),
                                        html.Span(user_info.get('name', 'User')),
                                    ], className="d-flex align-items-center")
                                ], header=True),
                                dbc.DropdownMenuItem(user_info.get('role', 'User'), header=True),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem([html.I(className="fas fa-user me-2"), "Profile"], 
                                                   style={"transition": "background-color 0.2s ease", "padding": "0.6rem 1rem"}),
                                dbc.DropdownMenuItem([html.I(className="fas fa-cog me-2"), "Settings"],
                                                   style={"transition": "background-color 0.2s ease", "padding": "0.6rem 1rem"}),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem([html.I(className="fas fa-sign-out-alt me-2"), "Sign Out"],
                                                   style={"transition": "background-color 0.2s ease", "padding": "0.6rem 1rem"}),
                            ],
                            nav=True,
                            in_navbar=True,
                            label=html.Img(src=user_info.get('avatar_url', 'assets/images/user-avatar.svg'), className="rounded-circle", width=36, height=36),
                            toggle_style={"padding": "0", "border": "none"},
                            align_end=True,
                        ),
                    ],
                    className="ms-auto align-items-center",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="white",
    dark=False,
    className="mb-4 shadow-sm",
    sticky="top",
    style={"boxShadow": "0 2px 10px rgba(0,0,0,0.075)", "borderBottom": "1px solid #f0f0f0"}
)

# Create section header with toggle button
def create_section_header(title, icon, section_id, color, description=None):
    """
    Create a collapsible section header with toggle functionality.
    
    Args:
        title (str): The title of the section
        icon (str): FontAwesome icon class for the section
        section_id (str): Unique identifier for the section
        color (str): Base color for the section header (hex or rgba)
        description (str, optional): Description text to display below the header
        
    Returns:
        html.Div: The complete section header component
    """
    # Create a unique HTML ID for the section itself
    html_id = f"{section_id}"
    
    # Parse the color to create a softer version by reducing opacity
    # If the color is in hex format, convert it to rgba with reduced opacity
    if color.startswith('#'):
        # Make base color slightly softer
        softer_color = color + "cc"  # 80% opacity
        gradient_end = color + "88"  # 53% opacity
    else:
        # If it's already in rgba or other format, just use it
        softer_color = color
        gradient_end = color
    
    # Create a chevron with consistent styling
    chevron = html.I(
        id={"type": "section-chevron", "index": section_id},
        className="fas fa-chevron-down",
        style={
            "transition": "transform 0.3s, background-color 0.2s",
            "fontSize": "1.4rem",
            "color": "white",
            "backgroundColor": "rgba(255, 255, 255, 0.25)",
            "borderRadius": "50%",
            "width": "36px",
            "height": "36px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            "backdropFilter": "blur(2px)"
        }
    )
    
    # Make the entire header clickable for toggle functionality
    header = html.Div(
        [
            # Left section with icon and title in a properly aligned container
            html.Div([
                # Container for icon to ensure vertical alignment
                html.Div([
                    html.I(className=f"{icon} fa-lg", style={"color": "white"})
                ], 
                style={
                    "display": "flex", 
                    "alignItems": "center",
                    "background": "rgba(255, 255, 255, 0.25)",
                    "borderRadius": "50%",
                    "width": "45px",
                    "height": "45px",
                    "justifyContent": "center",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.08)",
                    "backdropFilter": "blur(5px)"
                }),
                
                # Title with proper margin
                html.H3(title, 
                    className="ms-3 m-0", 
                    id=f"{section_id}-title", 
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "textShadow": "0 1px 2px rgba(0, 0, 0, 0.1)"
                    })
            ], className="d-flex align-items-center"),
            
            # Right section with chevron
            html.Div([
                chevron
            ], className="ms-auto")
        ],
        id={"type": "section-header", "index": section_id},
        className="d-flex align-items-center justify-content-between section-header p-3 rounded",
        style={
            "cursor": "pointer", 
            "userSelect": "none",
            "transition": "all 0.3s ease",
            "background": f"linear-gradient(135deg, {softer_color}, {gradient_end})",
            "boxShadow": "0 3px 6px rgba(0, 0, 0, 0.08), inset 0 -1px 0 rgba(0, 0, 0, 0.05)",
            "borderLeft": "4px solid rgba(255, 255, 255, 0.9)",
            "position": "relative",
            "overflow": "hidden",
            "margin": "16px 0 8px 0"
        }
    )
    
    # Container for header and description
    return html.Div([
        header,
        # Show description if provided, with consistent margins
        html.P(description, 
               className="mt-2 mb-3 text-muted", 
               style={"fontSize": "0.95rem", "lineHeight": "1.5", "paddingLeft": "10px"}) if description else None
    ], id=html_id, className="mb-4")  # Add spacing after the entire section header component

# Create a regular section header without collapse functionality
def create_regular_header(title, icon, color):
    """
    Create a non-collapsible section header with appropriate styling.
    
    Args:
        title (str): The title of the section
        icon (str): FontAwesome icon class for the section
        color (str): Base color for the section header (hex or rgba)
        
    Returns:
        html.Div: The styled header component
    """
    if (title == app_store_title):  # Special styling for AI App Store
        return html.Div([
            html.Div([
                html.Div(
                    html.I(className=f"{icon} fa-3x", style={"color": color}),
                    className="me-3 d-flex align-items-center justify-content-center",
                    style={"width": "72px", "height": "72px"}
                ),
                html.H1(title, className="d-inline m-0", 
                       style={
                           "fontWeight": "700", 
                           "color": "#1565C0", 
                           "letterSpacing": "0.5px",
                           "borderBottom": "3px solid #e0e0e0",
                           "paddingBottom": "8px"
                       })
            ], className="d-flex align-items-center mt-4 mb-4"),
        ], className="pb-2")
    else:  # Regular styling for other headers
        return html.Div([
            html.Div([
                html.Div(
                    html.I(className=f"{icon} fa-2x", style={"color": color}),
                    className="me-3 d-flex align-items-center justify-content-center",
                    style={"width": "50px", "height": "50px"}
                ),
                html.H2(title, className="d-inline m-0", style={"fontWeight": "600"})
            ], className="d-flex align-items-center mt-4 mb-3"),
        ], className="pb-2")

# Create quick navigation links
def create_quick_nav_links():
    # Add department section links
    links = []
    for i, dept in enumerate(categories):
        dept_icon = config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')
        dept_color = icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5'))
        dept_id = dept.lower().replace(' ', '-')
        
        links.append(
            html.A([
                html.Span([
                    html.I(className=f"{dept_icon} me-1"),
                    dept
                ])
            ], 
            id=f"nav-{dept_id}-link",
            className="badge bg-light me-2 mb-2 p-2 text-decoration-none", 
            style={
                "color": dept_color, 
                "borderColor": dept_color, 
                "borderWidth": "1px", 
                "borderStyle": "solid",
                "cursor": "pointer"
            })
        )
    
    return links

# Definition of all section IDs for reference - Removing app-store since it's not collapsible
section_ids = [dept.lower().replace(' ', '-') for dept in categories]

# Main content layout with collapsible sections
content = html.Div(
    [
        # Store to persist section states
        dcc.Store(id="section-states", storage_type="local"),
        
        # App Store section (not collapsible)
        html.Div([
            create_regular_header(app_store_title, app_store_icon, icon_colors.get("App Store")),
            # Banner image - container adjusted to match section width
            html.Div([
                html.Img(src=app_store.get('banner_image', 'assets/images/app-store-banner.svg'), 
                        className="img-fluid rounded",
                        alt="AI App Store Banner",
                        style={"width": "100%"})
            ], className="mb-3"),
            html.P(app_store_description, className="lead mb-3"),
            
            # Department quick links section
            html.Div([
                html.H5("Explore Categories:", className="mb-3 fw-bold"),
                html.Div([
                    html.A([
                        html.I(className=f"{next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder')} me-2", 
                              style={"color": icon_colors.get(dept, '#4a6fa5')}),
                        dept
                    ],
                    href=f"#{dept.lower().replace(' ', '-')}",  # Ensure consistent formatting with section IDs
                    className="btn me-2 mb-2",
                    style={
                        "backgroundColor": "white",
                        "color": icon_colors.get(dept, '#4a6fa5'),
                        "border": f"1px solid {icon_colors.get(dept, '#4a6fa5')}",
                        "borderRadius": "50px",
                        "padding": "8px 16px",
                        "fontWeight": "500",
                        "transition": "all 0.2s ease",
                        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.08)",
                        ":hover": {
                            "backgroundColor": icon_colors.get(dept, '#4a6fa5'),
                            "color": "white"
                        }
                    })
                    for dept in categories
                ], className="d-flex flex-wrap mb-4")
            ], className="bg-light p-4 rounded-3 mb-4 shadow-sm", 
               style={"border": "1px solid #e9ecef"}),
            
        ], className="mb-5 px-0", id="app-store-section"),  # Removed padding to match section headers
        
        # Department sections - no direct app cards outside of these sections
        *[
            html.Div([
                create_section_header(
                    f"{dept} AI Applications",
                    next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder'),
                    dept.lower().replace(' ', '-'),
                    icon_colors.get(dept, '#4a6fa5'),
                    dept_descriptions.get(dept, "")
                ),
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col(card, md=4) for card in create_app_cards(dept)
                    ], className="g-4"),
                ],
                    id={"type": "section-collapse", "index": dept.lower().replace(' ', '-')},
                    is_open=True,  # Initial state - set to True to make sections expanded by default
                )
            ], className="mb-5") for dept in categories
        ]
    ],
    className="container",
    style={"padding": "1rem"}
)

# Footer with company information
footer = html.Footer(
    dbc.Container(
        [
            html.Hr(style={"opacity": "0.15"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Img(src=company_info.get('logo_url', ''), height="32px", className="me-2"),
                        html.Span(company_info.get('name', config.get('title', "AI Portal")), 
                                 className="fw-bold", 
                                 style={"color": "#1565C0"})
                    ], className="d-flex align-items-center mb-3"),
                    html.P("© 2025 All rights reserved.", 
                          className="text-muted small", 
                          style={"fontSize": "0.85rem", "margin": "0"})
                ], md=6),
                dbc.Col([
                    html.Div([
                        dbc.Button([html.I(className="fab fa-github fa-lg")], 
                                  color="link", 
                                  className="text-dark me-3 p-0",
                                  style={"transition": "transform 0.2s", ":hover": {"transform": "translateY(-2px)"}}),
                        dbc.Button([html.I(className="fab fa-linkedin fa-lg")], 
                                  color="link", 
                                  className="text-dark me-3 p-0",
                                  style={"transition": "transform 0.2s", ":hover": {"transform": "translateY(-2px)"}}),
                        dbc.Button([html.I(className="fab fa-twitter fa-lg")], 
                                  color="link", 
                                  className="text-dark p-0",
                                  style={"transition": "transform 0.2s", ":hover": {"transform": "translateY(-2px)"}})
                    ], className="d-flex justify-content-end")
                ], md=6, className="d-flex align-items-center justify-content-end")
            ])
        ],
        fluid=True,
        className="py-4"
    ),
    className="mt-5 bg-light shadow-sm",
    style={"borderTop": "1px solid #e9ecef"}
)

# App layout
dash_app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content,
    footer
])

# --- Callbacks and Interactivity ---

# Callback to toggle the navbar collapse on small screens
@dash_app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    """Toggle the navbar collapse state on mobile screens"""
    if n:
        return not is_open
    return is_open

# Client-side callback to handle anchor links in the Categories dropdown menu
dash_app.clientside_callback(
    """
    function(href) {
        if (href && href.includes('#')) {
            // Get the target ID from the URL hash
            const targetId = href.split('#')[1];
            if (targetId) {
                // Find the element
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    // Scroll to the element
                    setTimeout(() => {
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }, 100);
                } else {
                    console.error('Target element not found:', targetId);
                }
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("url", "search"),  # Dummy output that won't affect the page
    [Input("url", "href")],   # Input is the full URL
    prevent_initial_call=True
)

# Apply default expanded state to all sections when page loads, but allow toggling
@dash_app.callback(
    [Output({"type": "section-collapse", "index": ALL}, "is_open"),
     Output({"type": "section-chevron", "index": ALL}, "style")],
    [Input("url", "pathname"),
     Input({"type": "section-header", "index": ALL}, "n_clicks")],
    [State({"type": "section-collapse", "index": ALL}, "is_open")]
)
def toggle_section_collapse(pathname, n_clicks_list, is_open_list):
    """
    Handle the collapsing/expanding of sections and update chevron styles accordingly.
    
    This function manages both the initial state on page load and user interactions.
    """
    ctx = callback_context
    
    # If there's no trigger yet or the pathname changed (page load)
    if not ctx.triggered or ctx.triggered[0]['prop_id'] == 'url.pathname':
        # On initial page load, ensure all sections are expanded
        default_is_open = [True for _ in section_ids] if section_ids else []
        styles = []
        
        for i, _ in enumerate(default_is_open):
            # Get the color for this section
            section_id = section_ids[i]
            
            # Find corresponding department name
            dept_name = next((dept for dept in categories if dept.lower().replace(' ', '-') == section_id), None)
            color = icon_colors.get(dept_name, company_info.get('theme_color', '#4a6fa5'))
            
            # Create style for expanded state
            styles.append({
                "transition": "transform 0.3s, background-color 0.2s",
                "transform": "rotate(0deg)",  # Expanded state
                "fontSize": "1.6rem",
                "color": "white",
                "backgroundColor": color,
                "borderRadius": "50%",
                "width": "32px",
                "height": "32px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "padding": "4px",
                "opacity": "1.0"
            })
        
        return default_is_open, styles
    
    # Otherwise, handle section toggle clicks
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        # Extract the clicked section ID from the trigger
        trigger_data = json.loads(trigger_id)
        section_index = trigger_data.get('index')
        
        # Get index of the clicked section in our sections list
        clicked_index = section_ids.index(section_index)
        
        # Toggle the clicked section's state
        new_is_open = list(is_open_list)  # Create a copy
        new_is_open[clicked_index] = not new_is_open[clicked_index]
        
        # Update styles for all chevrons
        styles = []
        for i, is_open in enumerate(new_is_open):
            # Get the color for this section
            section_id = section_ids[i]
            
            # Find corresponding department name
            dept_name = next((dept for dept in categories if dept.lower().replace(' ', '-') == section_id), None)
            color = icon_colors.get(dept_name, company_info.get('theme_color', '#4a6fa5'))
            
            # Create style with transform based on state
            styles.append({
                "transition": "transform 0.3s, background-color 0.2s",
                "transform": "rotate(0deg)" if is_open else "rotate(-90deg)",
                "fontSize": "1.6rem",
                "color": "white",
                "backgroundColor": color,
                "borderRadius": "50%",
                "width": "32px",
                "height": "32px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.15)",
                "padding": "4px",
                "opacity": "1.0" if is_open else "0.85"  # Slightly dim when closed
            })
        
        return new_is_open, styles
        
    except Exception as e:
        print(f"Error in toggle_section: {e}")
        # Return unchanged states if there's an error
        return dash.no_update, dash.no_update

# --- Department Navigation Links ---

# First, clear any existing callbacks to avoid conflicts
for dept in categories:
    dept_id = dept.lower().replace(' ', '-')
    try:
        dash_app.callback_map.pop(f"..nav-{dept_id}-link.n_clicks...url.hash", None)
    except:
        pass  # Ignore if callback doesn't exist

# Then create new callbacks with proper closures
for dept in categories:
    dept_id = dept.lower().replace(' ', '-')
    
    # This immediately invoked function creates a proper closure for each department
    def create_callback_for_dept(dept_id=dept_id):  # Capture dept_id in function default parameter
        @dash_app.callback(
            Output("url", "hash", allow_duplicate=True),
            [Input(f"nav-{dept_id}-link", "n_clicks")],
            prevent_initial_call=True
        )
        def navigate_to_department(n_clicks):
            """Navigate to the specified department section"""
            if n_clicks:
                return dept_id
            return dash.no_update
    
    # Execute the function immediately to register the callback with the captured dept_id
    create_callback_for_dept()

# --- Business Areas Navigation ---

# Using a single combined callback instead of individual callbacks
@dash_app.callback(
    [Output(f"business-area-{area.lower().replace(' ', '-').replace('-', '_')}", "style") for area in business_areas] + 
    [Output("business-area-sections", "className")],
    [Input(f"business-area-{area.lower().replace(' ', '-').replace('-', '_')}-link", "n_clicks") for area in business_areas],
    [State("business-area-sections", "className")]
)
def handle_business_area_navigation(*args):
    """
    Handle navigation between different business areas.
    
    Shows the selected business area and hides all others.
    """
    # Get all n_clicks arguments (excluding the last state argument)
    n_clicks_list = args[:-1]
    current_class = args[-1]
    
    # If no clicks happened yet, hide all sections
    if all(n is None for n in n_clicks_list):
        return [{"display": "none"} for _ in business_areas] + [current_class]
    
    # Find which area was clicked by examining the callback context
    ctx = callback_context
    if not ctx.triggered:
        return [{"display": "none"} for _ in business_areas] + [current_class]
    
    # Get the ID of the clicked link
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Find which area corresponds to the clicked link
    area_styles = []
    for area in business_areas:
        area_id = f"business-area-{area.lower().replace(' ', '-').replace('-', '_')}"
        if f"{area_id}-link" == triggered_id:
            # Show this area
            area_styles.append({"display": "block"})
        else:
            # Hide all other areas
            area_styles.append({"display": "none"})
    
    # Return all outputs
    return area_styles + ["business-area-active"]

# --- Main Entry Point ---

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    dash_app.run(debug=True, host='0.0.0.0', port=port)
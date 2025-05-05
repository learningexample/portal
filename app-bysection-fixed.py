"""
Enterprise AI Portal - Collapsible Section Version (app-bysection-fixed.py)
Fixed version that removes the problematic business areas functionality
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc
import yaml
import os
import json
import sys
import time
from datetime import datetime

# Import logging utilities
from utils.log import get_logger, log_activity, log_performance, log_button_click

# Set up logger for this application
logger = get_logger('app_bysection_fixed')
logger.info("Starting Enterprise AI Portal - Collapsible Sections Fixed Version")

# Load configuration from YAML file
def load_config():
    start_time = time.time()
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # Validate essential configuration sections
        required_sections = ['company', 'departments']
        missing_sections = [section for section in required_sections if section not in config]
        
        if (missing_sections):
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

# Create a dictionary of apps for each category
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

# Icon color mapping for different departments and shared apps
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

# Helper functions for handling contact information
def has_contact_info(app):
    """Check if the app has any contact information."""
    return app.get('contact_url') or app.get('contact') or app.get('contact_email') or app.get('email')

def get_contact_href(app):
    """Get the appropriate href value for the contact button."""
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

# Create the app cards with colorful icons
def create_app_cards(dept):
    cards = []
    for app in apps.get(dept, []):
        icon = app.get('icon', 'fa-solid fa-cube')  # Default icon if none specified
        business_area = app.get('business_area', 'All')  # Get business area or default to 'All'
        
        # Set icon color based on app name or fall back to department color
        icon_color = app_icon_colors.get(app.get('name', ''), icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5')))
        
        # Define business area badge styling based on the area
        badge_styles = {
            'All': {
                'icon': 'fa-solid fa-globe',
                'bg': '#0D47A1',
                'color': '#FFFFFF'
            },
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
                "boxShadow": "0 2px 4px rgba(0,0,0,0.15)",
                "padding": "0.35em 0.6em",
                "fontSize": "0.8rem",
                "display": "flex",
                "alignItems": "center",
                "gap": "4px"
            }
        )
        
        # Determine if we should show Launch App button or Contact Me button
        has_url = 'url' in app and app.get('url', '').strip()
        has_contact = app.get('contact_url') or app.get('contact_email') or app.get('email')
        
        # Create the button(s) based on what information is available
        buttons = []
        if has_url:
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-external-link-alt me-2"),
                    "Launch App"
                ], color="primary", href=app.get('url', '#'), className="me-2 flex-grow-1", target="_blank")
            )
        
        # Add Contact button - can be configured to use contact_url or contact_email
        if has_contact:
            contact_href = (
                app.get('contact_url') if app.get('contact_url') and app.get('contact_url').startswith('http') 
                else f"mailto:{app.get('contact_email', app.get('email', ''))}"
            )
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-comment me-2"),
                    "Contact"
                ], color="info", href=contact_href, className="flex-grow-1", target="_blank")
            )
        
        if not buttons:
            # Fallback if neither url nor contact info is provided
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-info-circle me-2"),
                    "No Link Available"
                ], color="secondary", disabled=True, className="w-100")
            )
        
        card = dbc.Card([
            # Add business area badge
            business_badge,
            
            dbc.CardBody([
                # Card content container with flex display
                html.Div([
                    # Header section
                    html.Div([
                        html.I(className=f"{icon} fa-2x me-2", style={"color": icon_color}),
                        html.H5(app.get('name', ''), className="card-title d-inline-block align-middle mb-0")
                    ], className="d-flex align-items-center mb-3"),
                    
                    # Description section - will stretch to fill available space
                    html.Div([
                        html.P(app.get('description', ''), className="card-text")
                    ], className="flex-grow-1 mb-3"),
                    
                    # Button section - always at the bottom
                    html.Div([
                        # Display both buttons in a row if we have both
                        html.Div(buttons, className="d-flex")
                    ])
                ], className="d-flex flex-column h-100") # Make the div take full height of card
            ])
        ], className="mb-4 h-100 position-relative")
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
                        dbc.Col(dbc.NavbarBrand(company_info.get('name', config.get('title', "AI Portal")), className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
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
                            )
                        ),
                        # Category navigation menu
                        dbc.DropdownMenu(
                            [dbc.DropdownMenuItem(
                                [html.I(className=f"{config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')} me-2"), dept], 
                                href=f"#{dept.lower().replace(' ', '-')}"  # Ensure spaces are replaced with hyphens
                             ) for i, dept in enumerate(categories)],
                            label="Categories",
                            nav=True,
                            className="mx-2"
                        ),
                        # User profile dropdown
                        user_dropdown,
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="light",
    dark=False,
    className="mb-4",
    sticky="top",
)

# Create section header with toggle button
def create_section_header(title, icon, section_id, color, description=None):
    # Create a unique HTML ID for the section itself to help with debugging
    html_id = f"{section_id}"
    
    # Create a chevron with professional styling
    chevron = html.I(
        id={"type": "section-chevron", "index": section_id},
        className="fas fa-chevron-down ms-3",
        style={
            "transition": "transform 0.3s, background-color 0.2s",
            "fontSize": "1.8rem",
            "color": "white",
            "backgroundColor": "rgba(255, 255, 255, 0.25)",
            "borderRadius": "50%",
            "width": "36px",
            "height": "36px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.15)",
            "backdropFilter": "blur(5px)"
        }
    )
    
    # Make the entire header clickable with a clear ID pattern and professional styling
    header = html.Div(
        [
            # Icon with glass morphism effect
            html.Div([
                html.I(className=f"{icon} fa-2x", 
                       style={
                           "color": "white",
                           "filter": "drop-shadow(0 2px 3px rgba(0,0,0,0.2))"
                       })
            ],
            style={
                "background": "rgba(255, 255, 255, 0.2)",
                "backdropFilter": "blur(10px)",
                "borderRadius": "50%",
                "width": "50px",
                "height": "50px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "boxShadow": "inset 0 0 0 1px rgba(255, 255, 255, 0.2), 0 4px 8px rgba(0, 0, 0, 0.15)"
            },
            className="me-3"),
            
            # Title with modern typography styling
            html.H2(title, 
                   className="d-inline m-0", 
                   id=f"{section_id}-title", 
                   style={
                       "color": "white",
                       "fontWeight": "600",
                       "textShadow": "0 2px 4px rgba(0, 0, 0, 0.15)",
                       "letterSpacing": "0.5px"
                   }),
            
            # Chevron icon
            chevron
        ],
        id={"type": "section-header", "index": section_id},
        className="d-flex align-items-center mt-4 mb-2 section-header p-3 rounded",
        style={
            "cursor": "pointer", 
            "userSelect": "none",  # Prevent text selection on click
            "transition": "all 0.3s ease",
            "background": f"linear-gradient(135deg, {color}, {color}dd, {color}00)",
            "boxShadow": "0 4px 15px rgba(0, 0, 0, 0.08), inset 0 -1px 0 rgba(255, 255, 255, 0.15)",
            "borderLeft": "5px solid rgba(255, 255, 255, 0.7)",
            "backdropFilter": "blur(10px)",
            "position": "relative",
            "overflow": "hidden"
        }
    )
    
    # Container for header and description
    return html.Div([
        header,
        # Show description if provided
        html.P(description, 
               className="lead mb-3 ps-3",
               style={
                   "borderLeft": f"3px solid {color}50",
                   "paddingLeft": "10px",
                   "color": "#555",
                   "fontSize": "0.95rem"
               }) if description else None
    ], id=html_id)  # Add the HTML ID to the outer container

# Create a regular section header without collapse functionality
def create_regular_header(title, icon, color):
    if (title == app_store_title):  # Special styling for AI App Store
        return html.Div([
            html.Div([
                html.I(className=f"{icon} fa-3x me-3", style={"color": color}),  # Larger icon for app store
                html.H1(title, className="d-inline m-0", 
                       style={"fontWeight": "700", "color": "#1565C0", "letterSpacing": "0.5px"})
            ], className="d-flex align-items-center mt-4 mb-3"),
        ])
    else:  # Regular styling for other headers
        return html.Div([
            html.Div([
                html.I(className=f"{icon} fa-2x me-3", style={"color": color}),  # Increased to fa-2x
                html.H2(title, className="d-inline m-0")
            ], className="d-flex align-items-center mt-4 mb-2"),
        ])

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
            # Banner image
            html.Img(src=app_store.get('banner_image', 'assets/images/app-store-banner.svg'), 
                    className="img-fluid mb-3 rounded",
                    alt="AI App Store Banner",
                    style={"maxWidth": "100%"}),
            html.P(app_store_description, className="lead mb-3"),
            
            # Department quick links section
            html.Div([
                html.H5("Explore Categories:", className="mb-3"),
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
                        "transition": "all 0.3s ease",
                        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
                    })
                    for dept in categories
                ], className="d-flex flex-wrap mb-4")
            ], className="bg-light p-3 rounded mb-4"),
            
        ], className="mb-5", id="app-store-section"),
        
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
                    # Section separator - without icon, consistent with other sections
                    html.Div([
                        html.Hr(style={"borderTop": f"4px solid {icon_colors.get(dept, '#4a6fa5')}", "opacity": "0.8", "borderRadius": "2px"})
                    ], className="text-center mt-5 mb-3")
                ],
                    id={"type": "section-collapse", "index": dept.lower().replace(' ', '-')},
                    is_open=True,  # Initial state - set to True to make sections expanded by default
                )
            ], className="mb-5") for dept in categories
        ]
    ],
    className="container",
    style={"padding": "1rem"},
)

# Footer with company information
footer = html.Footer(
    dbc.Container(
        [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Img(src=company_info.get('logo_url', ''), height="30px", className="me-2"),
                        html.Span(company_info.get('name', config.get('title', "AI Portal")), className="fw-bold")
                    ], className="d-flex align-items-center mb-2"),
                    html.P("© 2025 All rights reserved.", className="text-muted small")
                ], md=6),
                dbc.Col([
                    html.Div([
                        dbc.Button([html.I(className="fab fa-github")], color="link", className="text-dark me-2"),
                        dbc.Button([html.I(className="fab fa-linkedin")], color="link", className="text-dark me-2"),
                        dbc.Button([html.I(className="fab fa-twitter")], color="link", className="text-dark me-2")
                    ], className="d-flex justify-content-end")
                ], md=6, className="d-flex align-items-center")
            ])
        ],
        fluid=True,
        className="py-3"
    ),
    className="mt-5 bg-light"
)

# App layout
dash_app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content,
    footer
])

# Callback to toggle the navbar collapse on small screens
@dash_app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
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
                    // Scroll to the element and expand the section
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

# Initialize section states from localStorage or defaults
@dash_app.callback(
    Output("section-states", "data"),
    Input("url", "pathname"),
)
def initialize_states(pathname):
    if pathname is None:
        raise PreventUpdate
    # Default all sections to open
    default_states = {section_id: True for section_id in section_ids}
    return default_states

# Apply states from the store to all sections
@dash_app.callback(
    [Output(f"{section_id}-section", "className") for section_id in section_ids],
    Input("section-states", "data"),
)
def apply_states_to_sections(states):
    if not states:
        return ["collapsed" for _ in section_ids]
    
    return [
        "" if states.get(section_id, False) else "collapsed"
        for section_id in section_ids
    ]

# Toggle section when header is clicked
@dash_app.callback(
    Output("section-states", "data", allow_duplicate=True),
    Input({"type": "section-header", "index": ALL}, "n_clicks"),
    State("section-states", "data"),
    prevent_initial_call=True
)
def toggle_section(n_clicks_list, current_states):
    ctx = callback_context
    if not ctx.triggered:
        return current_states
    
    # Get the triggered component's id
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        # Extract the section ID from the trigger
        trigger_data = json.loads(trigger_id)
        section_id = trigger_data.get('index')
        
        print(f"Toggle clicked for section: {section_id}")
        
        # Make sure we have a valid states dictionary
        if not current_states:
            current_states = {section_id: section_id == "shared" for section_id in section_ids}
        else:
            # Create a new copy to avoid mutation issues
            current_states = dict(current_states)
        
        # Toggle the specific section's state
        current_states[section_id] = not current_states.get(section_id, False)
        
        print(f"New section states: {current_states}")
        return current_states
        
    except Exception as e:
        print(f"Error in toggle_section: {e}")
        # Return the unchanged states if there's an error
        return current_states

# Department navigation links with proper closures
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
            if n_clicks:
                print(f"Navigating to department: {dept_id}")  # Debug print
                return dept_id
            return dash.no_update
    
    # Execute the function immediately to register the callback with the captured dept_id
    create_callback_for_dept()

# Client-side callback for smooth scrolling and section auto-expand
dash_app.clientside_callback(
    """
    function(hash, sectionStates) {
        if (hash) {
            // Remove the leading # if present
            const targetId = hash.startsWith('#') ? hash.substring(1) : hash;
            console.log("Navigation to section:", targetId);
            
            // Make a copy of the current states
            let updatedStates = {...sectionStates};
            
            // Auto-open the section if it matches one of our collapsible sections
            if (updatedStates && targetId in updatedStates) {
                console.log("Opening section:", targetId);
                updatedStates[targetId] = true;
                
                // Find the element after a small delay to allow React to update the DOM
                setTimeout(() => {
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        console.log("Scrolling to element:", targetId);
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    } else {
                        console.log("Target element not found:", targetId);
                    }
                }, 200);
                
                return updatedStates;
            }
            
            // Just scroll to the element if it's not a collapsible section
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                console.log("Scrolling to non-section element:", targetId);
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            } else {
                console.log("Target element not found:", targetId);
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("section-states", "data", allow_duplicate=True),
    [Input("url", "hash")],
    [State("section-states", "data")],
    prevent_initial_call=True
)

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    dash_app.run(debug=True, host='0.0.0.0', port=port)
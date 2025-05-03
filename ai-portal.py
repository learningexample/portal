"""
Enterprise AI Portal - Main Portal Version (ai-portal.py)

COPILOT INSTRUCTIONS:
- This is the main portal with root URL path
- Uses Flask server exposed as 'server' for Gunicorn integration
- Gunicorn used in production with multiple workers
- Dash design features collapsible sections with jQuery
- Default path is /
"""

import dash
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback_context, ALL
import dash_bootstrap_components as dbc
import yaml
import os
import json
import sys
import gc
from utils.performance_utils import memory_cache, measure_execution_time
from flask import request

# Load configuration from YAML file
@memory_cache(ttl_seconds=600)  # Cache config for 10 minutes
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'ai-portal.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # Validate essential configuration sections
        required_sections = ['company', 'departments']
        missing_sections = [section for section in required_sections if section not in config]
        
        if (missing_sections):
            print(f"Warning: Missing required sections in ai-portal.yaml: {', '.join(missing_sections)}")
            print("Using default values for missing sections.")
            
            # Add default values for missing sections
            if 'company' not in config:
                config['company'] = {'name': 'Enterprise', 'logo_url': 'assets/images/logo.svg', 'theme_color': '#4a6fa5'}
            if 'departments' not in config:
                config['departments'] = []
                
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        print("Using default configuration.")
        return {
            'company': {'name': 'Enterprise', 'logo_url': 'assets/images/logo.svg', 'theme_color': '#4a6fa5'},
            'departments': [
                {
                    'name': 'Internal Tools',
                    'icon': 'fa-solid fa-tools',
                    'description': 'Tools for internal use only',
                    'apps': [
                        {
                            'name': 'Chat with Documents',
                            'description': 'Chat with your documents using AI assistance',
                            'icon': 'fa-solid fa-comments',
                            'url': '/chat-with-documents'
                        },
                        {
                            'name': 'Compare Documents',
                            'description': 'Compare two documents and identify differences',
                            'icon': 'fa-solid fa-file-contract',
                            'url': '/compare-documents'
                        }
                    ]
                },
                {
                    'name': 'License Required',
                    'icon': 'fa-solid fa-key',
                    'description': 'These tools require a valid license to use',
                    'apps': [
                        {
                            'name': 'ChatGPT Enterprise',
                            'description': 'Enterprise-grade AI assistant with advanced capabilities',
                            'icon': 'fa-solid fa-robot',
                            'url': '/chatgpt-enterprise'
                        },
                        {
                            'name': 'Microsoft Copilot',
                            'description': 'AI assistant integrated with Microsoft products',
                            'icon': 'fa-brands fa-microsoft',
                            'url': '/microsoft-copilot'
                        }
                    ]
                }
            ]
        }
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        sys.exit(1)  # Exit if YAML is malformed - critical error
    except Exception as e:
        print(f"Unexpected error loading configuration: {e}")
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
                url_base_pathname="/",  # Root URL path
                suppress_callback_exceptions=True,  # Add this to suppress callback exceptions
                assets_folder="assets",  # Explicitly set assets folder
                include_assets_files=True,
                assets_external_path="/assets/",
                # Disable WebSockets - use HTTP polling instead
                use_pages=False,  
                pages_folder="",
                # Important: These settings configure Dash to NOT use WebSockets
                # and to use HTTP polling for updates instead
                requests_pathname_prefix="/",
                routes_pathname_prefix="/",
                serve_locally=True)

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

# Add cache control headers for static assets
@server.after_request
def add_cache_headers(response):
    if 'assets' in request.path:
        # Cache assets for 24 hours
        response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

# Get departments from config
categories = [dept['name'] for dept in config.get('departments', [])]

# Create a dictionary of apps for each department/category
# Use a global variable to cache results across requests
_apps_cache = {}
@memory_cache(ttl_seconds=300)
def get_apps():
    """Get all apps with caching applied"""
    global _apps_cache
    
    # Return cached data if available
    if _apps_cache:
        return _apps_cache
        
    apps = {}
    for dept in config.get('departments', []):
        dept_name = dept['name']
        apps[dept_name] = dept.get('apps', [])

    # Add app store apps
    app_store = config.get('app_store', {})
    app_store_title = app_store.get('title', "AI Portal")
    app_store_icon = app_store.get('icon', "fa-solid fa-store")
    app_store_description = app_store.get('description', "Access your AI applications in one place")
    apps['App Store'] = app_store.get('apps', [])
    
    # Cache the results
    _apps_cache = apps
    return apps

apps = get_apps()

# Get department descriptions
dept_descriptions = {}
for dept in config.get('departments', []):
    dept_descriptions[dept['name']] = dept.get('description', "")

# Icon color mapping for different departments
# Get department colors from config
icon_colors = config.get('department_colors', {})
# Set default fallback color
default_color = icon_colors.get('default', '#4a6fa5')

# Default icon colors for our departments
if 'Internal Tools' not in icon_colors:
    icon_colors['Internal Tools'] = '#1976D2'  # Blue
if 'License Required' not in icon_colors:
    icon_colors['License Required'] = '#F57C00'  # Orange

# App-specific icon color mapping
app_icon_colors = {
    # Internal Tools
    'Chat with Documents': '#43A047',
    'Compare Documents': '#1B5E20',
    'RFP Assistant': '#00796B',
    
    # License Required
    'ChatGPT Enterprise': '#D32F2F',
    'Microsoft Copilot': '#0066CC',
    'Writer': '#F9A825',
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

# Cache for app cards to avoid rebuilding on every request
app_cards_cache = {}

# Create the app cards with colorful icons
@memory_cache(ttl_seconds=300)
def create_app_cards(dept):
    # Return from cache if available
    if dept in app_cards_cache:
        return app_cards_cache[dept]
        
    cards = []
    for app in apps.get(dept, []):
        icon = app.get('icon', 'fa-solid fa-cube')  # Default icon if none specified
        business_area = app.get('business_area', 'All')  # Get business area or default to 'All'
        
        # Set icon color based on app name or fall back to department color
        icon_color = app_icon_colors.get(app['name'], icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5')))
        
        # Determine if we should show Launch App button or Contact Me button
        has_url = 'url' in app and app['url'] and app['url'].strip()
        has_contact = has_contact_info(app)
        
        # Create the button(s) based on what information is available
        buttons = []
        if has_url:
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-external-link-alt me-2"),
                    "Launch App"
                ], color="primary", href=app['url'], className="me-2 flex-grow-1", target="_blank")
            )
        else:
            # No URL - show "Coming Soon" button with hourglass icon
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-hourglass-half me-2"),
                    "Coming Soon"
                ], color="secondary", className="me-2 flex-grow-1", disabled=True)
            )
        
        # Add Contact button - can be configured to use contact_url or contact_email
        if has_contact:
            contact_href = get_contact_href(app)
            buttons.append(
                dbc.Button([
                    html.I(className="fas fa-comment me-2"),
                    "Contact"
                ], color="info", href=contact_href, className="flex-grow-1", target="_blank")
            )
        
        card = dbc.Card([
            dbc.CardBody([
                # Card content container with flex display
                html.Div([
                    # Header section
                    html.Div([
                        html.I(className=f"{icon} fa-2x me-2", style={"color": icon_color}),
                        html.H5(app['name'], className="card-title d-inline-block align-middle mb-0")
                    ], className="d-flex align-items-center mb-3"),
                    
                    # Description section - will stretch to fill available space
                    html.Div([
                        html.P(app['description'], className="card-text")
                    ], className="flex-grow-1 mb-3"),
                    
                    # Button section - always at the bottom
                    html.Div([
                        # Display both buttons in a row if we have both
                        html.Div(buttons, className="d-flex")
                    ])
                ], className="d-flex flex-column h-100") # Make the div take full height of card
            ])
        ], className="mb-4 h-100")
        cards.append(card)
    
    # Store in cache
    app_cards_cache[dept] = cards
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
    'All': {
        'icon': 'fa-solid fa-globe',
        'bg': '#0D47A1',
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
                        # Category navigation menu with properly formatted href links
                        dbc.DropdownMenu(
                            [dbc.DropdownMenuItem(
                                [html.I(className=f"{config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')} me-2"), dept], 
                                href=f"#{dept.lower().replace(' ', '-')}"  # Ensure spaces are replaced with hyphens
                             ) for i, dept in enumerate(categories)],
                            label="Categories",
                            nav=True,
                            className="mx-2"
                        ),
                        # Feedback link
                        dbc.NavItem(
                            dbc.NavLink(
                                "Feedback",
                                href="mailto:feedback@techcorp.com",
                                className="me-2",
                                style={"fontWeight": "500"},
                            )
                        ),
                        # Logout link
                        dbc.NavItem(
                            dbc.NavLink(
                                "Logout",
                                href="/logout",
                                className="me-3",
                                style={"fontWeight": "500"},
                            )
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
    
    # Create a chevron with clear styling
    chevron = html.I(
        id={"type": "section-chevron", "index": section_id},
        className="fas fa-chevron-down",
        style={
            "transition": "transform 0.3s, background-color 0.2s",
            "fontSize": "1.6rem",
            "color": color,
            "backgroundColor": "transparent",
            "borderRadius": "50%",
            "width": "32px",
            "height": "32px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "4px"
        }
    )
    
    # Make the entire header clickable for toggle functionality
    header = html.Div(
        [
            # Left section with icon and title in a properly aligned container
            html.Div([
                # Container for icon to ensure vertical alignment
                html.Div([
                    html.I(className=f"{icon} fa-lg", style={"color": color})
                ], 
                style={
                    "display": "flex", 
                    "alignItems": "center",
                    "borderRadius": "50%",
                    "width": "40px",
                    "height": "40px",
                    "justifyContent": "center"
                }),
                
                # Title with proper margin
                html.H3(title, 
                    className="ms-3 m-0", 
                    id=f"{section_id}-title", 
                    style={
                        "color": color,
                        "fontWeight": "600"
                    })
            ], className="d-flex align-items-center"),
            
            # Right section with chevron
            html.Div([
                chevron
            ], className="ms-auto")
        ],
        id={"type": "section-header", "index": section_id},
        className="d-flex align-items-center justify-content-between mt-2 mb-1 section-header p-3 rounded",
        style={
            "cursor": "pointer", 
            "userSelect": "none",
            "transition": "all 0.3s ease",
            "background": "transparent",
            "borderBottom": f"1px solid {color}",
            "position": "relative"
        }
    )
    
    # Container for header and description with reduced spacing
    return html.Div([
        header,
        # Show description if provided, with reduced margins
        html.P(description, className="my-3 text-muted", style={"fontSize": "0.9rem"}) if description else None
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
@memory_cache(ttl_seconds=300)
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
                "transition": "transform 0.3s",
                "transform": "rotate(0deg)",  # Expanded state
                "fontSize": "1.6rem",
                "color": color,
                "backgroundColor": "transparent",
                "borderRadius": "50%",
                "width": "32px",
                "height": "32px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "4px"
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
                "transition": "transform 0.3s",
                "transform": "rotate(0deg)" if is_open else "rotate(-90deg)",
                "fontSize": "1.6rem",
                "color": color,
                "backgroundColor": "transparent",
                "borderRadius": "50%",
                "width": "32px",
                "height": "32px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "4px"
            })
        
        return new_is_open, styles
        
    except Exception as e:
        print(f"Error in toggle_section: {e}")
        # Return unchanged states if there's an error
        return dash.no_update, dash.no_update

# Department navigation links - using a more robust approach with correct closures
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
                return dept_id
            return dash.no_update
    
    # Execute the function immediately to register the callback with the captured dept_id
    create_callback_for_dept()

# Memory optimization: Run garbage collection periodically
import threading
def _periodic_gc():
    gc.collect()
    # Schedule next cleanup in 5 minutes
    threading.Timer(300, _periodic_gc).start()

# Start the GC thread if in production mode
if __name__ != '__main__':
    _gc_thread = threading.Timer(300, _periodic_gc)
    _gc_thread.daemon = True
    _gc_thread.start()

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    debug_mode = os.environ.get('DASH_DEBUG_MODE', 'False').lower() == 'true'
    dash_app.run(debug=debug_mode, host='0.0.0.0', port=port)
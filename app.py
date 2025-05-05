"""
Enterprise AI Portal - Original Version (app.py)

Main application entry point for the Enterprise AI Portal, providing a scrolling 
sections-based interface with department-specific AI applications.

COPILOT INSTRUCTIONS:
- This is the original portal version with scrolling sections design
- Uses Flask server exposed as 'server' for Gunicorn integration
- WebSocket connections are handled by Apache reverse proxy
- Not for direct internet exposure - always behind reverse proxy
- Default path is /portal-1/
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import yaml
import os

# Import logging utilities
from utils.log import get_logger, log_activity, setup_logging, log_button_click

# Set up logger for this application
logger = get_logger('app')
logger.info("Starting Enterprise AI Portal - Original Version")

# Load configuration from YAML file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded successfully from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}

config = load_config()

# Company and user information
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
                    {'name': 'description', 'content': 'Enterprise AI Portal for accessing departmental AI applications'}
                ],
                title=app_title,
                update_title=f"Loading {app_title}...",
                url_base_pathname="/portal-1/",  # Add trailing slash back
                suppress_callback_exceptions=True)

# Add favicon - explicitly set to override Dash default
dash_app._favicon = None  # Disable default Dash favicon

# Add our own favicon to the index template
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
departments = [dept['name'] for dept in config.get('departments', [])]

# Create a dictionary of apps for each department
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
    'Financial Forecasting': '#43A047',
    'Expense Analysis': '#1B5E20',
    'Customer Segmentation': '#D32F2F',
    'Campaign Optimizer': '#B71C1C',
    'Supply Chain Prediction': '#1976D2',
    'Quality Control': '#0D47A1',
    'Resume Screening': '#8E24AA',
    'Employee Attrition Model': '#4A148C',
    'Incident Prediction': '#F57C00',
    'Automated Code Review': '#E65100',
    'Document AI': '#00ACC1',
    'Chatbot Assistant': '#00838F',
    'Data Visualization': '#00695C',
    'Text Analyzer': '#1E88E5',
    'Image Generator': '#039BE5',
    'Voice Assistant': '#0277BD',
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
        
        # Set icon color based on app name or fall back to department color
        icon_color = app_icon_colors.get(app['name'], icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5')))
        
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
                        # Create buttons based on available information
                        html.Div([
                            # Launch App button if URL is provided
                            dbc.Button([
                                html.I(className="fas fa-external-link-alt me-2"),
                                "Launch App"
                            ], 
                            color="primary", 
                            href=app['url'], 
                            target="_blank",
                            className="me-2 flex-grow-1") if 'url' in app and app['url'] and app['url'].strip() else None,
                            
                            # Contact button - can be URL or mailto based on contact field value
                            dbc.Button([
                                html.I(className="fas fa-comment me-2"),
                                "Contact"
                            ], 
                            color="info", 
                            href=get_contact_href(app),
                            target="_blank",
                            className="flex-grow-1" if not ('url' in app and app['url'] and app['url'].strip()) else "",
                            disabled=not has_contact_info(app)),
                            
                            # Fallback button if neither URL nor contact info is provided
                            dbc.Button([
                                html.I(className="fas fa-info-circle me-2"),
                                "No Link Available"
                            ], 
                            color="secondary", 
                            disabled=True, 
                            className="w-100") if not (('url' in app and app['url'] and app['url'].strip()) or 
                                                     (app.get('contact_url') or app.get('contact_email') or app.get('email'))) else None
                        ], className="d-flex")
                    ])
                ], className="d-flex flex-column h-100") # Make the div take full height of card
            ])
        ], className="mb-4 h-100")
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
                        # App Store navigation item
                        dbc.NavItem(dbc.NavLink([
                            html.I(className=f"{app_store_icon} me-2"),
                            app_store_title
                        ], href="#app-store")),
                        # Department navigation menu
                        dbc.DropdownMenu(
                            [dbc.DropdownMenuItem(
                                [html.I(className=f"{config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')} me-2"), dept], 
                                href=f"#{dept.lower()}"
                             ) for i, dept in enumerate(departments)],
                            label="Departments",
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

# Section headers with colorful icons
def create_section_header(title, icon, id_name, dept=None):
    # Set icon color based on department
    icon_color = icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5'))
    
    return html.Div([
        html.Div([
            # Icon container with glass-morphism effect
            html.Div([
                html.I(className=f"{icon}", 
                       style={
                           "color": "white", 
                           "fontSize": "1.8rem",
                           "filter": "drop-shadow(0 2px 3px rgba(0,0,0,0.2))"
                       })
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "width": "48px",
                "height": "48px",
                "borderRadius": "50%",
                "background": "rgba(255, 255, 255, 0.2)",
                "backdropFilter": "blur(5px)",
                "boxShadow": "inset 0 0 0 1px rgba(255, 255, 255, 0.2)"
            },
            className="me-3"),
            
            # Title with enhanced typography
            html.H2(title, 
                   style={
                       "color": "white", 
                       "margin": "0",
                       "fontWeight": "600",
                       "textShadow": "0 1px 2px rgba(0, 0, 0, 0.15)",
                       "letterSpacing": "0.5px"
                   })
        ], 
        className="d-flex align-items-center p-3 rounded",
        style={
            "background": f"linear-gradient(135deg, {icon_color}, {icon_color}dd, {icon_color}00)",
            "boxShadow": "0 4px 15px rgba(0, 0, 0, 0.08), inset 0 -1px 0 rgba(255, 255, 255, 0.15)",
            "borderLeft": "5px solid rgba(255, 255, 255, 0.7)",
            "marginBottom": "1rem",
            "position": "relative",
            "overflow": "hidden"
        }),
    ], id=id_name)

# Create quick navigation links
def create_quick_nav_links():
    links = []
    
    # Add department section links
    for i, dept in enumerate(departments):
        dept_icon = config.get('departments', [])[i].get('icon', 'fa-solid fa-folder')
        dept_color = icon_colors.get(dept, company_info.get('theme_color', '#4a6fa5'))
        
        links.append(
            html.A([
                html.Span([
                    html.I(className=f"{dept_icon} me-1"),
                    dept
                ])
            ], 
            id=f"nav-{dept.lower().replace(' ', '-')}-link",
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

# Main content layout - App Store first as a non-section element, then department apps
content = html.Div(
    [
        # AI App Store section (first, but not as a section)
        html.Div([
            # Banner image
            html.Img(src=app_store.get('banner_image', 'assets/images/app-store-banner.svg'), 
                    className="img-fluid mb-3 rounded",
                    alt="AI App Store Banner",
                    style={"maxWidth": "100%"}),
            
            # Title with enhanced styling
            html.Div([
                html.I(className=f"{app_store_icon} me-3", style={"color": icon_colors.get("App Store"), "fontSize": "2.2rem"}),
                html.H1(app_store_title, className="d-inline m-0", 
                      style={"fontWeight": "700", "color": "#1565C0", "letterSpacing": "0.5px"})
            ], className="d-flex align-items-center mb-3"),
            
            # Description and cards
            html.Div([
                html.P(app_store_description, className="lead mb-3"),
                
                dbc.Row([
                    dbc.Col(card, md=4) for card in create_app_cards('App Store')
                ], className="g-4")
            ])
        ], className="mb-5 p-4"),
    ] + [
        # Department apps sections
        html.Div([
            create_section_header(
                f"{dept} AI Applications",
                next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder'),
                f"{dept.lower()}",
                dept
            ),
            html.P(dept_descriptions.get(dept, ""), className="lead mb-4"),
            dbc.Row([
                dbc.Col(card, md=4) for card in create_app_cards(dept)
            ], className="g-4")
        ], 
        className="mb-5 p-4") for dept in departments
    ],
    className="container",
    style={
        "padding": "1rem",
    },
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
    [dash.dependencies.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Department navigation links
for dept in departments:
    # Create a dynamic callback for each department
    @dash_app.callback(
        Output("url", "hash"),
        [Input(f"nav-{dept.lower().replace(' ', '-')}-link", "n_clicks")],
        prevent_initial_call=True
    )
    def navigate_to_department(n_clicks, dept_name=dept):
        if n_clicks:
            return dept_name.lower()
        return dash.no_update

# Add client-side JavaScript for smooth scrolling
dash_app.clientside_callback(
    """
    function(hash) {
        if (hash) {
            // Remove the leading # if present
            const targetId = hash.startsWith('#') ? hash.substring(1) : hash;
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Smooth scroll to the element
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("url", "search"),
    [Input("url", "hash")],
    prevent_initial_call=True
)

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    dash_app.run(debug=False, host='0.0.0.0', port=port)
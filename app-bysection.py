"""
Enterprise AI Portal - Collapsible Section Version (app-bysection.py)

Section-based version of the Enterprise AI Portal with collapsible sections
for each department, providing an organized way to access AI applications.

COPILOT INSTRUCTIONS:
- This is the collapsible sections portal version
- Uses Flask server exposed as 'server' for Gunicorn integration
- WebSocket connections are handled by Apache reverse proxy
- Uses clientside callbacks for persistent section states with localStorage
- Default path is /portal-3/
- Implements more complex UI interaction than other versions
"""

import dash
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback_context, ALL
import dash_bootstrap_components as dbc
import yaml
import os
import json

# Load configuration from YAML file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

config = load_config()

# Company and user information
company_info = config.get('company', {})
user_info = config.get('user', {})

# Initialize the app with a Bootstrap theme and Font Awesome icons
app_title = f"{company_info.get('name', 'Enterprise')} AI Portal" 
app = dash.Dash(__name__, 
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
                url_base_pathname="/portal-3/")

# Add favicon - explicitly set to override Dash default
app._favicon = None  # Disable default Dash favicon

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

app.index_string = index_string
server = app.server  # for deployment purposes

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

# Add shared apps
apps['Shared'] = config.get('shared', {}).get('apps', [])
shared_title = config.get('shared', {}).get('title', "Shared Apps")
shared_icon = config.get('shared', {}).get('icon', "fa-solid fa-share-nodes")
shared_description = config.get('shared', {}).get('description', "Cross-departmental AI tools")

# Get department descriptions
dept_descriptions = {}
for dept in config.get('departments', []):
    dept_descriptions[dept['name']] = dept.get('description', "")

# Icon color mapping for different departments and shared apps
icon_colors = {
    'Finance': '#2E7D32',  # Green
    'Marketing': '#C62828',  # Red
    'Operations': '#0277BD',  # Blue
    'HR': '#6A1B9A',  # Purple
    'IT': '#EF6C00',  # Orange
    'Shared': '#00695C',  # Teal
    'App Store': '#1565C0',  # Blue
}

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
                        dbc.Button([
                            html.I(className="fas fa-external-link-alt me-2"),
                            "Launch App"
                        ], color="primary", href=app['url'], className="w-100")
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
                        # Shared apps menu item
                        dbc.NavItem(dbc.NavLink([
                            html.I(className=f"{shared_icon} me-2"),
                            shared_title
                        ], href="#shared")),
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
    header_elements = [
        html.I(className=f"{icon} me-2", style={"color": color}),
        html.H2(title, className="d-inline m-0"),
        html.I(
            id={"type": "section-chevron", "index": section_id},
            className="fas fa-chevron-down ms-2",
            style={"transition": "transform 0.3s"}
        )
    ]
    
    header = html.Div(
        header_elements,
        id={"type": "section-header", "index": section_id},
        className="d-flex align-items-center mt-4 mb-2",
        style={"cursor": "pointer"}
    )
    
    # Container for header and description
    return html.Div([
        header,
        # Show description if provided
        html.P(description, className="lead mb-3") if description else None
    ])

# Create a regular section header without collapse functionality
def create_regular_header(title, icon, color):
    if title == app_store_title:  # Special styling for AI App Store
        return html.Div([
            html.Div([
                html.I(className=f"{icon} me-3", style={"color": color, "fontSize": "2.2rem"}),
                html.H1(title, className="d-inline m-0", 
                       style={"fontWeight": "700", "color": "#1565C0", "letterSpacing": "0.5px"})
            ], className="d-flex align-items-center mt-4 mb-3"),
        ])
    else:  # Regular styling for other headers
        return html.Div([
            html.Div([
                html.I(className=f"{icon} me-2", style={"color": color}),
                html.H2(title, className="d-inline m-0")
            ], className="d-flex align-items-center mt-4 mb-2"),
        ])

# Definition of all section IDs for reference - Removing app-store since it's not collapsible
section_ids = ["shared"] + [dept.lower().replace(' ', '-') for dept in departments]

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
            dbc.Row([
                dbc.Col(card, md=4) for card in create_app_cards('App Store')
            ], className="g-4")
        ], className="mb-5"),
        
        # Shared apps section
        html.Div([
            create_section_header(shared_title, shared_icon, "shared", icon_colors.get("Shared"), shared_description),
            dbc.Collapse(
                dbc.Row([
                    dbc.Col(card, md=4) for card in create_app_cards('Shared')
                ], className="g-4"),
                id={"type": "section-collapse", "index": "shared"},
                is_open=True,  # Initial state - will be overridden by the callback
            )
        ], className="mb-5"),
    ] + [
        # Department sections
        html.Div([
            create_section_header(
                f"{dept} AI Applications",
                next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder'),
                dept.lower().replace(' ', '-'),
                icon_colors.get(dept, '#4a6fa5'),
                dept_descriptions.get(dept, "")
            ),
            dbc.Collapse(
                dbc.Row([
                    dbc.Col(card, md=4) for card in create_app_cards(dept)
                ], className="g-4"),
                id={"type": "section-collapse", "index": dept.lower().replace(' ', '-')},
                is_open=False,  # Initial state - will be overridden by the callback
            )
        ], className="mb-5") for dept in departments
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
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content,
    footer
])

# Callback to toggle the navbar collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Initialize section states from localStorage or defaults
@app.callback(
    Output("section-states", "data"),
    Input("url", "pathname"),
    State("section-states", "data"),
)
def initialize_states(pathname, current_states):
    # If we have stored states, use them
    if (current_states):
        return current_states
    
    # Otherwise create default states (only shared section is open)
    default_states = {section_id: section_id == "shared" for section_id in section_ids}
    return default_states

# Apply states from the store to all sections
@app.callback(
    [Output({"type": "section-collapse", "index": ALL}, "is_open"),
     Output({"type": "section-chevron", "index": ALL}, "style")],
    Input("section-states", "data"),
)
def apply_states_to_sections(states):
    if not states:
        # Default - only Shared section open
        is_open_list = [section_id == "shared" for section_id in section_ids]
    else:
        # Get values from stored states
        is_open_list = [states.get(section_id, section_id == "shared") for section_id in section_ids]
    
    # Create styles for chevrons based on open/closed state
    styles = [{
        "transition": "transform 0.3s",
        "transform": "rotate(0deg)" if is_open else "rotate(-90deg)"
    } for is_open in is_open_list]
    
    return is_open_list, styles

# Toggle section when header is clicked
@app.callback(
    Output("section-states", "data", allow_duplicate=True),
    Input({"type": "section-header", "index": ALL}, "n_clicks"),
    State({"type": "section-collapse", "index": ALL}, "is_open"),
    State("section-states", "data"),
    prevent_initial_call=True
)
def toggle_section(n_clicks_list, is_open_list, current_states):
    # Find which section was clicked
    ctx = callback_context
    if not ctx.triggered:
        return current_states  # No change
    
    # Get the ID of the clicked section
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    clicked_section = json.loads(trigger_id)["index"]
    
    # Find the position of this section in our list
    try:
        section_idx = section_ids.index(clicked_section)
    except ValueError:
        return current_states  # Can't find it, no change
    
    # Update the states dictionary with new toggle state
    if not current_states:
        current_states = {section_id: section_id == "shared" for section_id in section_ids}
    
    current_states[clicked_section] = not is_open_list[section_idx]
    
    return current_states

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    app.run_server(debug=False, host='0.0.0.0', port=port)
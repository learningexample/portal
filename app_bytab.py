"""
Enterprise AI Portal - Tabbed Version (app_bytab.py)

Tabbed interface version of the Enterprise AI Portal, providing organized access
to departmental AI applications through a tab-based navigation system.

COPILOT INSTRUCTIONS:
- This is the tabbed portal version with tab-based navigation
- Uses Flask server exposed as 'server' for Gunicorn integration
- WebSocket connections are handled by Apache reverse proxy
- Contains additional debug logging compared to other versions
- Default path is /portal-2/
- Prefers f-strings over other string formatting
"""

# Add more comprehensive debug logging
import sys
import traceback
import time
from datetime import datetime
import logging  # Keep this for log levels

# Import logging utilities
from utils.log import get_logger, log_activity, log_performance, log_button_click

# Set up logger for this module
logger = get_logger('app_bytab', level=logging.DEBUG)
logger.info("Starting app_bytab.py")

try:
    import dash
    from dash import dcc, html, Input, Output
    import dash_bootstrap_components as dbc
    from dash.dependencies import Input, Output, State
    import yaml
    import os
    
    logger.info("All modules imported successfully.")
    
    # Load configuration from YAML file
    def load_config():
        logger.debug("Attempting to load config...")
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Config loaded successfully with {len(config.keys()) if config else 0} top level keys")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            traceback.print_exc()
            return {}

    config = load_config()

    # Company and user information
    company_info = config.get('company', {})
    user_info = config.get('user', {})

    # Get portal title from config
    portal_title = config.get('title', "Enterprise AI Portal")
    portal_description = config.get('description', "Central portal for departmental AI applications")

    # Initialize the app with a Bootstrap theme and Font Awesome icons
    app_title = f"{company_info.get('name', 'Enterprise')} {portal_title} (Tabbed)" 
    dash_app = dash.Dash(__name__, 
                    external_stylesheets=[
                        dbc.themes.BOOTSTRAP,
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
                    ],
                    meta_tags=[
                        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'},
                        {'name': 'description', 'content': portal_description}
                    ],
                    title=app_title,
                    update_title=f"Loading {app_title}...",
                    url_base_pathname="/portal-2/",  # Add trailing slash back
                    suppress_callback_exceptions=True)

    # Add favicon
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

    # Theme color from company settings
    theme_color = company_info.get('theme_color', '#4a6fa5')

    # Icon color mapping for different departments
    icon_colors = {
        'Finance': '#2E7D32',  # Green
        'Marketing': '#C62828',  # Red
        'Operations': '#0277BD',  # Blue
        'HR': '#6A1B9A',  # Purple
        'IT': '#EF6C00',  # Orange
        'App Store': '#1565C0',  # Blue
    }

    # App-specific icon color mapping
    app_icon_colors = {}

    # Create app cards with colorful icons
    def create_app_cards(dept):
        cards = []
        for app in apps.get(dept, []):
            icon = app.get('icon', 'fa-solid fa-cube')  # Default icon if none specified
            
            # Set icon color based on app name or fall back to department color
            icon_color = app_icon_colors.get(app['name'], icon_colors.get(dept, theme_color))
            
            # Check if the app has a valid URL and contact information
            has_url = 'url' in app and app.get('url') and app.get('url').strip()
            has_contact = app.get('contact_url') or app.get('contact') or app.get('contact_email') or app.get('email')
            
            # Create the button(s) based on what information is available
            buttons = []
            
            if has_url:
                buttons.append(
                    dbc.Button([
                        html.I(className="fas fa-external-link-alt me-2"),
                        "Launch App"
                    ], color="primary", href=app.get('url', app.get('contact', '#')), className="me-2 flex-grow-1", target="_blank",
                       style={"borderRadius": "var(--border-radius)", "fontWeight": "500", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"})
                )
            else:
                # Show Coming Soon button with hourglass icon
                buttons.append(
                    dbc.Button([
                        html.I(className="fas fa-hourglass-half me-2"),
                        "Coming Soon"
                    ], color="secondary", className="me-2 flex-grow-1", disabled=True,
                       style={"borderRadius": "var(--border-radius)", "fontWeight": "500", "opacity": "0.65"})
                )
                
            # Add Contact button if contact info is available
            if has_contact:
                contact_href = app.get('contact', '#')
                if contact_href.startswith(('http://', 'https://')):
                    pass
                elif '@' in contact_href:
                    contact_href = f"mailto:{contact_href}"
                
                buttons.append(
                    dbc.Button([
                        html.I(className="fas fa-comment me-2"),
                        "Contact"
                    ], color="info", href=contact_href, className="flex-grow-1", target="_blank",
                       style={"borderRadius": "var(--border-radius)", "fontWeight": "500", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"})
                )
            
            card = dbc.Card([
                dbc.CardBody([
                    # Card content container with flex display
                    html.Div([
                        # Header section
                        html.Div([
                            html.I(className=f"{icon} fa-2x me-2", style={"color": icon_color}),
                            html.H5(app['name'], className="card-title d-inline-block align-middle mb-0", style={"fontWeight": "600"})
                        ], className="d-flex align-items-center mb-3"),
                        
                        # Description section - will stretch to fill available space
                        html.Div([
                            html.P(app['description'], className="card-text", style={"fontSize": "0.95rem", "lineHeight": "1.5"})
                        ], className="flex-grow-1 mb-3"),
                        
                        # Button section - always at the bottom
                        html.Div([
                            # Display buttons in a row
                            html.Div(buttons, className="d-flex")
                        ])
                    ], className="d-flex flex-column h-100") # Make the div take full height of card
                ])
            ], className="mb-4 h-100 shadow-sm", 
               style={
                   "transition": "var(--transition)",
                   "borderRadius": "var(--border-radius)",
                   "overflow": "hidden", 
                   "border": "1px solid #e9ecef"
               })
            cards.append(dbc.Col(card, md=4))
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
                            dbc.Col(dbc.NavbarBrand(company_info.get('name', portal_title), 
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
                            # App Store navigation item
                            dbc.NavItem(dbc.NavLink([
                                html.I(className=f"{app_store_icon} me-2"),
                                app_store_title
                            ], href="#", 
                               style={"transition": "var(--transition)", "borderRadius": "var(--border-radius)"})),
                            
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
                        className="ms-auto",
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
        style={"boxShadow": "var(--header-shadow)", "borderBottom": "1px solid #f0f0f0"}
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
                            html.Span(company_info.get('name', portal_title), 
                                     className="fw-bold", 
                                     style={"color": "#1565C0"})
                        ], className="d-flex align-items-center mb-3"),
                        html.P(f"© {company_info.get('copyright_year', '2025')} All rights reserved.", 
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
        className="mt-5 bg-light",
        style={"borderTop": "1px solid #e9ecef", "boxShadow": "0 -1px 3px rgba(15, 23, 42, 0.06)"}
    )

    # ----- SIMPLIFIED TABS IMPLEMENTATION -----
    logger.debug("Creating tabs with simpler implementation")

    # Create tabs content for each department
    tab_contents = {}

    # Create department content
    for dept in departments:
        dept_id = f"tab-{dept.lower().replace(' ', '-')}"

        dept_icon = next((d.get('icon', 'fa-solid fa-folder') 
                        for d in config.get('departments', []) 
                        if d['name'] == dept), 'fa-solid fa-folder')
        
        dept_info = next((d for d in config.get('departments', []) if d['name'] == dept), {})
        dept_description = dept_info.get('description', '')
        
        tab_contents[dept_id] = html.Div([
            html.H3([
                html.I(className=f"{dept_icon} me-3", style={"color": icon_colors.get(dept, theme_color), "fontSize": "1.6rem"}),  # Increased icon size and margin
                f"{dept} AI Applications"
            ]),
            html.P(dept_description, className="lead mb-3") if dept_description else None,
            html.Hr(),
            dbc.Row(create_app_cards(dept), className="g-4")
        ])

    # First department as default active tab or fallback
    default_tab = f"tab-{departments[0].lower().replace(' ', '-')}" if departments else None

    # Create a simple tabs component
    tabs = html.Div([
        dbc.Tabs([
            *[
                dbc.Tab(
                    label=html.Div([
                        html.I(className=f"{next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder')} me-2"),
                        dept
                    ]), 
                    tab_id=f"tab-{dept.lower().replace(' ', '-')}",
                    label_style={
                        "color": icon_colors.get(dept, theme_color),
                        "fontSize": "1.1rem",
                        "fontWeight": "500",
                        "padding": "0.75rem 1rem",
                        "borderRadius": "0",
                        "transition": "var(--transition)"
                    }
                ) for dept in departments
            ]
        ], id="tabs", active_tab=default_tab, className="nav-tabs"),
        html.Div(id="tab-content", className="pt-4")
    ], className="mt-4")

    # Main tab content layout
    tab_content = html.Div(
        dbc.Container(
            [tabs],
            fluid=True,
            className="py-3"
        ),
        className="mb-5"
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
                            html.Span(company_info.get('name', portal_title), className="fw-bold")
                        ], className="d-flex align-items-center mb-2"),
                        html.P(f"© {company_info.get('copyright_year', '2025')} All rights reserved.", className="text-muted small")
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
        # App Store section (always visible, before tabs)
        dbc.Container([
            # Banner image
            html.Img(src=app_store.get('banner_image', 'assets/images/app-store-banner.svg'), 
                    className="img-fluid mb-3 rounded",
                    alt="AI App Store Banner",
                    style={"maxWidth": "100%"}),
            
            # Enhanced title styling for App Store
            html.Div([
                html.I(className=f"{app_store_icon} me-3", style={"color": icon_colors.get("App Store"), "fontSize": "2.2rem"}),
                html.H1(app_store_title, className="d-inline m-0", 
                    style={"fontWeight": "700", "color": "#1565C0", "letterSpacing": "0.5px"})
            ], className="d-flex align-items-center mb-3"),
            
            # Description below banner
            html.P(app_store_description, className="lead mb-3"),
            dbc.Row(create_app_cards('App Store'), className="g-4 mb-5")
        ], fluid=True),
        # Tabbed content (for departments)
        tab_content,
        footer
    ])

    # Callback to update the tab content based on selected tab
    @dash_app.callback(
        Output("tab-content", "children"),
        Input("tabs", "active_tab")
    )
    def render_tab_content(active_tab):
        logger.debug(f"Rendering tab content for tab: {active_tab}")
        # Default to first department if none selected or if selected tab doesn't exist
        if not active_tab or active_tab not in tab_contents:
            default_tab = f"tab-{departments[0].lower().replace(' ', '-')}" if departments else None
            return tab_contents.get(default_tab, html.Div("No departments configured"))
        return tab_contents.get(active_tab)

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

    if __name__ == '__main__':
        # Get port from environment variable or default to 8050
        port = int(os.environ.get('PORT', 8050))
        
        logger.info(f"Starting Dash server on port {port}")
        # Run server, allow connections from any host for Docker
        dash_app.run(debug=True, host='0.0.0.0', port=port)
        
except Exception as e:
    logger.critical(f"Fatal error: {e}")
    traceback.print_exc()
    sys.exit(1)
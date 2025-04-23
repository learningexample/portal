import dash
from dash import dcc, html, clientside_callback, Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import yaml
import os

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

# Get portal title from config
portal_title = config.get('title', "Enterprise AI Portal")
portal_description = config.get('description', "Central portal for departmental AI applications")

# Initialize the app with a Bootstrap theme and Font Awesome icons
app_title = f"{company_info.get('name', 'Enterprise')} {portal_title} (Tabbed)" 
app = dash.Dash(__name__, 
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
                url_base_pathname="/portal-2/")

# Add favicon
app._favicon = None  # Disable default Dash favicon

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
shared = config.get('shared', {})
apps['Shared'] = shared.get('apps', [])
shared_title = shared.get('title', "Shared Apps")
shared_icon = shared.get('icon', "fa-solid fa-share-nodes")
shared_description = shared.get('description', "Applications shared across all departments")

# Theme color from company settings
theme_color = company_info.get('theme_color', '#4a6fa5')

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
app_icon_colors = {}

# Create app cards with colorful icons
def create_app_cards(dept):
    cards = []
    for app in apps.get(dept, []):
        icon = app.get('icon', 'fa-solid fa-cube')  # Default icon if none specified
        
        # Set icon color based on app name or fall back to department color
        icon_color = app_icon_colors.get(app['name'], icon_colors.get(dept, theme_color))
        
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
                        dbc.Col(dbc.NavbarBrand(company_info.get('name', portal_title), className="ms-2")),
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
                        ], href="#")),
                        
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

# Main content layout with tabs
def build_tabs():
    # Create tab items array
    tab_items = []
    
    # First tab for Shared Apps
    tab_items.append({
        "id": "tab-shared",
        "label": shared_title,
        "icon": shared_icon,
        "color": icon_colors.get('Shared', theme_color)
    })
    
    # Tab for each department
    for dept in departments:
        dept_icon = next((d.get('icon', 'fa-solid fa-folder') 
                         for d in config.get('departments', []) 
                         if d['name'] == dept), 'fa-solid fa-folder')
        tab_items.append({
            "id": f"tab-{dept.lower()}",
            "label": dept,
            "icon": dept_icon,
            "color": icon_colors.get(dept, theme_color)
        })
    
    # Last tab for App Store
    tab_items.append({
        "id": "tab-app-store",
        "label": app_store_title,
        "icon": app_store_icon,
        "color": icon_colors.get('App Store', theme_color)
    })
    
    # Create the tab nav items (the clickable tabs themselves)
    tab_nav_items = []
    for item in tab_items:
        tab_nav_items.append(
            html.Li(
                dbc.NavLink(
                    item["label"],
                    id={"type": "tab-link", "index": item["id"]},
                    active=item["id"] == "tab-shared",
                    class_name=f"tab-with-icon {item['icon']}",
                    style={"color": item["color"]},
                ),
                className="nav-item",
                id={"type": "tab-li", "index": item["id"]},
                **{"data-tab-id": item["id"]}  # Store the tab ID as a data attribute
            )
        )
    
    # Create the tabs component
    tabs_component = html.Div([
        # Hidden input to store the current active tab
        dcc.Input(id="active-tab-state", type="hidden", value="tab-shared"),
        # Create the nav tabs container
        html.Ul(
            tab_nav_items,
            className="nav nav-tabs mb-4",
            id="regular-tabs"
        ),
        # Tab content will be rendered here
        html.Div(id="tab-content", className="mt-3")
    ])
    
    return tabs_component

# Replace the original tabs with our simplified version
tabs = build_tabs()

# Main layout container
content_container = html.Div(id="tab-content", className="mt-3")

# Create tab content container
tab_content = html.Div(
    dbc.Container(
        [
            tabs,
            content_container
        ],
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
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    tab_content,
    footer
])

# Callback to update the tab content based on selected tab
@app.callback(
    Output("tab-content", "children"),  # Changed output target to match the correct ID
    Input("active-tab-state", "value")
)
def render_tab_content(active_tab):  # Renamed function for clarity
    if active_tab == "tab-shared":
        # Shared apps tab
        return html.Div([
            html.H3([
                html.I(className=f"{shared_icon} me-2", style={"color": icon_colors.get('Shared', theme_color)}),
                shared_title
            ]),
            html.P(shared_description, className="lead mb-3") if shared_description else None,
            html.Hr(),
            dbc.Row(create_app_cards('Shared'), className="g-4")
        ])
    elif active_tab == "tab-app-store":
        # App Store tab
        return html.Div([
            html.H3([
                html.I(className=f"{app_store_icon} me-2", style={"color": icon_colors.get('App Store', theme_color)}),
                app_store_title
            ]),
            html.P(app_store_description, className="lead mb-3") if app_store_description else None,
            html.Hr(),
            dbc.Row(create_app_cards('App Store'), className="g-4")
        ])
    else:
        # Department tab
        for dept in departments:
            if active_tab == f"tab-{dept.lower()}":
                dept_info = next((d for d in config.get('departments', []) if d['name'] == dept), {})
                dept_icon = dept_info.get('icon', 'fa-solid fa-folder')
                dept_description = dept_info.get('description', '')
                
                return html.Div([
                    html.H3([
                        html.I(className=f"{dept_icon} me-2", style={"color": icon_colors.get(dept, theme_color)}),
                        f"{dept} AI Applications"
                    ]),
                    html.P(dept_description, className="lead mb-3") if dept_description else None,
                    html.Hr(),
                    dbc.Row(create_app_cards(dept), className="g-4")
                ])
    
    # Default to empty div if no match
    return html.Div([])

# Callback to handle tab clicks
@app.callback(
    [Output("active-tab-state", "value"),
     Output({"type": "tab-link", "index": dash.dependencies.ALL}, "active")],
    [Input({"type": "tab-link", "index": dash.dependencies.ALL}, "n_clicks")],
    [dash.dependencies.State("active-tab-state", "value")]
)
def handle_tab_click(n_clicks, active_tab):
    ctx = dash.callback_context
    if not ctx.triggered:
        # Default active tab
        active_states = [tab_id == "tab-shared" for tab_id in ["tab-shared"] + [f"tab-{dept.lower()}" for dept in departments] + ["tab-app-store"]]
        return "tab-shared", active_states
    
    # Get the tab ID that was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    tab_id = eval(triggered_id)["index"]
    
    # Set all tabs to inactive except the clicked one
    all_tab_ids = ["tab-shared"] + [f"tab-{dept.lower()}" for dept in departments] + ["tab-app-store"]
    active_states = [tab_id == current_tab_id for current_tab_id in all_tab_ids]
    
    return tab_id, active_states

# Callback to toggle the navbar collapse on small screens
@app.callback(
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
    
    # Run server, allow connections from any host for Docker
    app.run_server(debug=False, host='0.0.0.0', port=port)
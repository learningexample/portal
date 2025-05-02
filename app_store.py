"""
Enterprise AI Portal - Apple App Store Inspired Version (app_store.py)

This version of the Enterprise AI Portal mimics the Apple App Store design patterns,
featuring horizontal scrolling content collections, featured apps, today section,
and a modern app card design.

COPILOT INSTRUCTIONS:
- This is the Apple App Store inspired portal version
- Uses Flask server exposed as 'server' for Gunicorn integration
- Features horizontal scrolling collections
- Uses featured content and varied card sizes
- Default path is /portal-4/
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yaml
import os
import random
from datetime import datetime

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
app_title = f"{company_info.get('name', 'Enterprise')} AI Portal (App Store)" 
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
                ],
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'},
                    {'name': 'description', 'content': 'AI App Store Portal'}
                ],
                title=app_title,
                update_title=f"Loading {app_title}...",
                url_base_pathname="/portal-4/",
                suppress_callback_exceptions=True)

# Add favicon - explicitly set to override Dash default
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
        <style>
            /* Apple-inspired styles */
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #f8f8f8;
                color: #1d1d1f;
            }
            
            .app-card {
                border-radius: 12px;
                overflow: hidden;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                background-color: white;
                height: 100%;
            }
            
            .app-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            .featured-app {
                height: 340px;
                position: relative;
                border-radius: 12px;
                overflow: hidden;
                background-color: white;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            
            .featured-app:hover {
                transform: translateY(-4px) scale(1.01);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            
            .featured-overlay {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 20px;
                background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
                color: white;
            }
            
            .collection-title {
                font-weight: 700;
                font-size: 22px;
                margin-bottom: 16px;
                margin-top: 20px;
                padding-left: 12px;
                display: flex;
                align-items: center;
            }
            
            .collection-title i {
                margin-right: 10px;
            }
            
            .horizontal-scroll {
                display: flex;
                overflow-x: auto;
                padding-bottom: 20px;
                margin-bottom: 20px;
                -webkit-overflow-scrolling: touch;
                scroll-behavior: smooth;
                scrollbar-width: none;  /* Firefox */
            }
            
            .horizontal-scroll::-webkit-scrollbar {
                display: none;  /* Chrome, Safari, Edge */
            }
            
            .scroll-item {
                flex: 0 0 auto;
                width: 280px;
                margin-right: 16px;
            }
            
            .scroll-item-small {
                flex: 0 0 auto;
                width: 200px;
                margin-right: 16px;
            }
            
            .scroll-item-large {
                flex: 0 0 auto;
                width: 400px;
                margin-right: 16px;
            }
            
            .today-card {
                border-radius: 16px;
                height: 400px;
                background-size: cover;
                background-position: center;
                position: relative;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            }
            
            .today-card:hover {
                transform: scale(1.02);
            }
            
            .today-overlay {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 25px;
                background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.7) 40%, transparent 100%);
                color: white;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }
            
            .tag {
                display: inline-block;
                padding: 4px 12px;
                background-color: rgba(0,122,255,0.1);
                color: #007AFF;
                border-radius: 100px;
                font-weight: 500;
                font-size: 12px;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .nav-tabs {
                border-bottom: none;
                margin-bottom: 20px;
            }
            
            .nav-tabs .nav-link {
                border: none;
                color: #6c757d;
                font-weight: 600;
                padding: 12px 16px;
                transition: color 0.2s ease;
            }
            
            .nav-tabs .nav-link.active {
                color: #007AFF;
                border-bottom: 2px solid #007AFF;
                background-color: transparent;
            }
            
            .nav-tabs .nav-link:hover {
                color: #007AFF;
                border-color: transparent;
            }
            
            .navbar {
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                background-color: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
            
            .btn-get {
                background-color: #007AFF;
                color: white;
                border-radius: 100px;
                padding: 6px 16px;
                font-weight: 600;
                border: none;
                font-size: 14px;
            }
            
            .btn-get:hover {
                background-color: #0056b3;
                color: white;
            }
            
            .app-icon {
                width: 64px;
                height: 64px;
                border-radius: 16px;
                margin-right: 12px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .app-title {
                font-weight: 600;
                margin-bottom: 4px;
            }
            
            .app-subtitle {
                color: #6c757d;
                font-size: 14px;
            }
            
            .footer {
                background-color: #f8f8f8;
                border-top: 1px solid #e1e1e1;
            }

            /* Bottom tab bar styling */
            .bottom-tab-bar {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background-color: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                z-index: 1000;
                padding: 8px 0;
                display: flex;
                justify-content: space-around;
                border-top: 1px solid #e1e1e1;
            }
            
            .tab-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                color: #8e8e93;
                text-decoration: none;
                font-size: 10px;
                transition: color 0.2s ease;
                padding: 5px 0;
            }
            
            .tab-item i {
                font-size: 22px;
                margin-bottom: 4px;
            }
            
            .tab-item.active {
                color: #007AFF;
            }
            
            .tab-item:hover {
                color: #007AFF;
                text-decoration: none;
            }

            /* Add padding to account for the bottom tab bar */
            .content-container {
                padding-bottom: 75px;
            }

            /* App rating stars */
            .rating {
                color: #ff9500;
                font-size: 12px;
                display: flex;
                align-items: center;
            }
            
            .rating-count {
                color: #8e8e93;
                margin-left: 5px;
                font-size: 12px;
            }
        </style>
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
apps_by_dept = {}
for dept in config.get('departments', []):
    dept_name = dept['name']
    apps_by_dept[dept_name] = dept.get('apps', [])

# Add app store apps
app_store = config.get('app_store', {})
app_store_title = app_store.get('title', "AI App Store")
app_store_icon = app_store.get('icon', "fa-solid fa-store")
app_store_description = app_store.get('description', "Discover and install the latest AI applications")
apps_by_dept['App Store'] = app_store.get('apps', [])

# Combine all apps into a single list for "All Apps" tab
all_apps = []
for dept_name, dept_apps in apps_by_dept.items():
    for app_item in dept_apps:
        app_copy = app_item.copy()
        app_copy['department'] = dept_name
        all_apps.append(app_copy)

# Icon color mapping for different departments
icon_colors = {
    'Finance': '#2E7D32',
    'Marketing': '#C62828',
    'Operations': '#0277BD',
    'HR': '#6A1B9A',
    'IT': '#EF6C00',
    'App Store': '#1565C0',
}

# Randomly select featured apps (one from each department)
featured_apps = []
for dept_name, dept_apps in apps_by_dept.items():
    if dept_apps:  # If department has apps
        app_item = random.choice(dept_apps)
        app_copy = app_item.copy()
        app_copy['department'] = dept_name
        featured_apps.append(app_copy)

# Function to generate random rating for demo purposes
def generate_rating():
    return round(random.uniform(3.5, 5.0), 1)

def generate_downloads():
    return random.randint(100, 10000)

# Enhance apps with additional metadata for display
for app_list in apps_by_dept.values():
    for app_item in app_list:
        app_item['rating'] = generate_rating()
        app_item['downloads'] = generate_downloads()
        app_item['release_date'] = datetime.now().strftime("%b %d, %Y")

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

# Top Navigation Bar (simplified Apple style)
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Company Logo and Brand
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=company_info.get('logo_url', ''), height="36px"), className="me-2"),
                        dbc.Col(dbc.NavbarBrand(company_info.get('name', "AI Portal"), className="ms-2")),
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
                        # Search icon
                        dbc.NavItem(dbc.NavLink([
                            html.I(className="fas fa-search")
                        ], href="#", id="search-button")),
                        
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
    className="mb-2",
    sticky="top",
)

# Create app-store inspired card
def create_app_card(app_item, dept=None):
    icon = app_item.get('icon', 'fa-solid fa-cube')
    department = app_item.get('department', dept)
    
    # Set icon color based on department
    icon_color = icon_colors.get(department, company_info.get('theme_color', '#4a6fa5'))
    
    # Determine if we should show Launch App button, Contact Me button, or both
    has_url = 'url' in app_item and app_item.get('url', '').strip()
    has_email = 'email' in app_item and app_item.get('email', '').strip()
    
    # Decide what button(s) to display
    button_content = html.Div(className="d-flex w-100")
    
    if has_url and has_email:
        # If both are available, show both buttons side by side
        button_content = html.Div([
            html.A("LAUNCH", 
                className="btn-get me-2 flex-grow-1 text-center",
                href=app_item['url'],
                target="_blank"
            ),
            html.A("CONTACT", 
                className="btn-contact flex-grow-1 text-center",
                href=f"mailto:{app_item['email']}",
                target="_blank"
            )
        ], className="d-flex w-100")
    elif has_url:
        # If only URL is available
        button_content = html.A("GET", 
                               className="btn-get w-100 text-center", 
                               href=app_item['url'], 
                               target="_blank")
    elif has_email:
        # If only email is available
        button_content = html.A("CONTACT", 
            className="btn-contact w-100 text-center",
            href=f"mailto:{app_item['email']}",
            target="_blank"
        )
    else:
        # Fallback if neither are available
        button_content = html.Button("INFO", 
            className="btn-disabled w-100",
            disabled=True
        )
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    # App icon and info
                    html.Div([
                        html.Div(
                            html.I(className=f"{icon} fa-2x", style={"color": "white"}),
                            className="app-icon d-flex align-items-center justify-content-center",
                            style={"backgroundColor": icon_color}
                        ),
                        html.Div([
                            html.H6(app_item['name'], className="app-title"),
                            html.Div(department, className="app-subtitle"),
                            # Rating stars
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-star"),
                                    html.I(className="fas fa-star"),
                                    html.I(className="fas fa-star"),
                                    html.I(className="fas fa-star"),
                                    html.I(className="fas fa-star-half-alt" if app_item['rating'] % 1 >= 0.5 else "far fa-star"),
                                ], className="rating"),
                                html.Span(f"{app_item['rating']} ({int(app_item['downloads']/100)})", className="rating-count")
                            ], className="d-flex align-items-center")
                        ])
                    ], className="d-flex mb-3"),
                    
                    # Description - limited to 2 lines with ellipsis
                    html.P(app_item['description'].split(' - ')[0], className="mb-3", 
                           style={
                               "overflow": "hidden", 
                               "textOverflow": "ellipsis", 
                               "display": "-webkit-box", 
                               "WebkitLineClamp": "2", 
                               "WebkitBoxOrient": "vertical"
                           }),
                    
                    # Button section
                    button_content
                ])
            ])
        ], className="app-card h-100")
    ], className="scroll-item")

# Create a featured app card
def create_featured_app_card(app_item):
    icon = app_item.get('icon', 'fa-solid fa-cube')
    department = app_item.get('department', 'App')
    
    # Set icon color based on department
    icon_color = icon_colors.get(department, company_info.get('theme_color', '#4a6fa5'))
    
    return html.Div([
        html.Div([
            # Background with gradient overlay
            html.Div(style={
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "backgroundColor": icon_color,
                "opacity": 0.2
            }),
            
            # App icon in large format
            html.Div([
                html.I(className=f"{icon} fa-4x", style={"color": "white"})
            ], className="d-flex align-items-center justify-content-center", 
               style={
                   "height": "150px", 
                   "width": "150px", 
                   "borderRadius": "30px", 
                   "backgroundColor": icon_color,
                   "margin": "30px auto 20px"
               }),
            
            # Content overlay at bottom
            html.Div([
                html.Span("FEATURED APP", className="tag"),
                html.H3(app_item['name'], className="mb-2 text-white"),
                html.P(app_item['description'].split(' - ')[0], className="text-white-50"),
                html.Button("GET", className="btn-get mt-2")
            ], className="featured-overlay")
        ], className="featured-app")
    ], className="scroll-item-large")

# Create today card with dynamic content
def create_today_card(title, subtitle, background_color="#007AFF"):
    return html.Div([
        html.Div([
            html.Div([
                html.Span("TODAY'S PICK", className="tag"),
                html.H3(title, className="mb-2 text-white"),
                html.P(subtitle, className="text-white-50"),
            ], className="today-overlay")
        ], className="today-card", style={"backgroundColor": background_color})
    ], className="scroll-item-large")

# Create Apple-style horizontal scrolling section
def create_app_collection(title, apps_list, icon="fa-solid fa-folder", color="#007AFF", dept=None):
    if not apps_list:  # Handle empty app list
        return html.Div([
            html.H3([
                html.I(className=f"{icon} me-2", style={"color": color})
            ], className="collection-title"),
            html.H3(title, className="collection-title mt-0"),
            html.P("No apps available in this collection", className="text-muted px-2")
        ])
        
    return html.Div([
        html.H3([
            html.I(className=f"{icon} me-2", style={"color": color})
        ], className="collection-title"),
        html.H3(title, className="collection-title mt-0"),
        html.Div([
            create_app_card(app_item, dept) for app_item in apps_list
        ], className="horizontal-scroll px-2")
    ])

# Create tabbed content
def create_tab_content():
    return html.Div([
        # Main tabs
        dbc.Tabs([
            dbc.Tab(label="Today", tab_id="tab-today", labelClassName="px-4"),
            dbc.Tab(label="Apps", tab_id="tab-apps", labelClassName="px-4"),
        ], id="main-tabs", active_tab="tab-today", className="mb-4"),
        
        # Tab content area
        html.Div(id="tab-content", className="mb-5"),
    ])

# Bottom tab bar (Apple App Store style)
bottom_tabs = html.Div([
    html.A([
        html.I(className="far fa-newspaper"),
        html.Span("Today")
    ], href="#", id="tab-link-today", className="tab-item active"),
    
    html.A([
        html.I(className="fas fa-th-large"),
        html.Span("Apps")
    ], href="#", id="tab-link-apps", className="tab-item"),
    
    html.A([
        html.I(className="fas fa-download"),
        html.Span("Updates")
    ], href="#", id="tab-link-updates", className="tab-item"),
    
    html.A([
        html.I(className="fas fa-search"),
        html.Span("Search")
    ], href="#", id="tab-link-search", className="tab-item")
], className="bottom-tab-bar")

# Footer with company information
footer = html.Footer(
    dbc.Container(
        [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Img(src=company_info.get('logo_url', ''), height="30px", className="me-2"),
                        html.Span(company_info.get('name', "AI Portal"), className="fw-bold")
                    ], className="d-flex align-items-center mb-2"),
                    html.P(f"© {datetime.now().year} All rights reserved.", className="text-muted small")
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
    className="footer"
)

# App layout with div container properly set up
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div([  # Content container with padding for bottom bar
        create_tab_content(),
        # Add a store component to keep track of which category is selected
        dcc.Store(id='selected-category', data=None),
    ], className="content-container container"),
    bottom_tabs,
    footer
])

# Callback to populate tab content based on active tab
@app.callback(
    Output("tab-content", "children"),
    [Input("main-tabs", "active_tab"),
     Input("selected-category", "data")]
)
def render_tab_content(active_tab, selected_category):
    ctx = dash.callback_context
    
    # Check if the callback was triggered by a category selection
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'selected-category.data' and selected_category:
        # Show apps for the selected category
        dept = selected_category  # The selected department name
        if dept in departments:
            return html.Div([
                # Back button to return to categories
                html.Button([
                    html.I(className="fas fa-arrow-left me-2"),
                    "Back to Categories"
                ], 
                id="back-to-categories", 
                className="btn btn-light mb-4",
                n_clicks=0),
                # Department header with icon
                html.Div([
                    html.I(className=next((d.get('icon', 'fa-solid fa-folder') 
                                         for d in config.get('departments', []) 
                                         if d['name'] == dept), 
                                         'fa-solid fa-folder'), 
                           style={"color": icon_colors.get(dept, '#4a6fa5'), "fontSize": "2rem", "marginRight": "15px"}),
                    html.H2(f"{dept} Applications", className="mb-0")
                ], className="d-flex align-items-center mb-4"),
                # Show the apps for this category
                html.Div([
                    create_app_card(app_item, dept) for app_item in apps_by_dept[dept]
                ], className="row g-4")
            ])
    
    # Otherwise show the regular tab content
    if active_tab == "tab-today":
        # Today tab - featured content and editorial
        return html.Div([
            # Hero section
            html.Div([
                html.Div([
                    html.Span("WELCOME TO", className="tag"),
                    html.H1(app_store_title, className="display-5 mb-3 text-white"),
                    html.P(app_store_description, className="lead text-white-50"),
                ], className="col-md-8 py-5 px-4")
            ], className="mb-4 rounded-3", style={
                "background": "linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)",
                "borderRadius": "12px"
            }),
            
            # Today's picks
            html.H3("Today's Picks", className="collection-title mb-4"),
            html.Div([
                create_today_card("AI for Finance", "Optimize your financial operations with these AI-powered tools", "#2E7D32"),
                create_today_card("Marketing Intelligence", "Enhance your marketing strategies with AI insights", "#C62828"),
                create_today_card("Smarter Operations", "Streamline your operations with intelligent automation", "#0277BD")
            ], className="horizontal-scroll px-2"),
            
            # Featured apps section
            html.H3("Featured Apps", className="collection-title mb-4 mt-4"),
            html.Div([
                create_featured_app_card(app_item) for app_item in featured_apps[:3]
            ], className="horizontal-scroll px-2"),
            
            # Editor's choice
            create_app_collection("Editor's Choice", random.sample(all_apps, min(6, len(all_apps))), icon="fa-solid fa-award", color="#FF9500"),
            
            # Must-have apps
            create_app_collection("Essential Apps", random.sample(all_apps, min(6, len(all_apps))), icon="fa-solid fa-star", color="#5856D6")
        ])
    
    elif active_tab == "tab-apps":
        # Apps tab - all apps by department
        return html.Div([
            # Department apps
            *[create_app_collection(
                f"{dept} Apps", 
                apps_by_dept[dept], 
                icon=next((d.get('icon', 'fa-solid fa-folder') for d in config.get('departments', []) if d['name'] == dept), 'fa-solid fa-folder'),
                color=icon_colors.get(dept),
                dept=dept
            ) for dept in departments]
        ])
    
    # Default - if no tab selected
    return html.Div("Please select a tab.")

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

# Callback to handle bottom tab bar clicks
@app.callback(
    [Output("main-tabs", "active_tab"),
     Output("tab-link-today", "className"),
     Output("tab-link-apps", "className"),
     Output("tab-link-updates", "className"),
     Output("tab-link-search", "className")],
    [Input("tab-link-today", "n_clicks"),
     Input("tab-link-apps", "n_clicks"),
     Input("tab-link-updates", "n_clicks"),
     Input("tab-link-search", "n_clicks")]
)
def handle_bottom_tabs(today_clicks, apps_clicks, updates_clicks, search_clicks):
    ctx = dash.callback_context
    
    # If no click, default to today tab
    if not ctx.triggered:
        return "tab-today", "tab-item active", "tab-item", "tab-item", "tab-item"
    
    # Get ID of clicked button
    clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Set active tab and classes
    active_tab = "tab-today"  # Default
    classes = ["tab-item", "tab-item", "tab-item", "tab-item"]
    
    if clicked_id == "tab-link-today":
        active_tab = "tab-today"
        classes[0] = "tab-item active"
    elif clicked_id == "tab-link-apps":
        active_tab = "tab-apps"
        classes[1] = "tab-item active"
    elif clicked_id == "tab-link-updates":
        # For demo, we'll just show the apps tab
        active_tab = "tab-apps"
        classes[2] = "tab-item active"
    elif clicked_id == "tab-link-search":
        # For demo, we'll just show the apps tab
        active_tab = "tab-apps"
        classes[3] = "tab-item active"
    
    return active_tab, classes[0], classes[1], classes[2], classes[3]

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    
    # Run server, allow connections from any host for Docker
    app.run_server(debug=True, host='0.0.0.0', port=port)
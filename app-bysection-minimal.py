"""
Minimal version of app-bysection.py to test the core functionality
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
                ],
                url_base_pathname="/AppStore/",
                suppress_callback_exceptions=True)

# Simple top navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/images/logo.svg", height="40px"), className="me-2"),
                        dbc.Col(dbc.NavbarBrand("Enterprise AI Portal", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            )
        ],
        fluid=True,
    ),
    color="light",
    dark=False,
    className="mb-4",
)

# Simple content
content = html.Div(
    [
        # Content section - shared apps removed
        html.Div(className="container")
    ],
    className="container",
    style={"padding": "1rem"},
)

# Footer
footer = html.Footer(
    dbc.Container(
        [
            html.Hr(),
            html.P("© 2025 Enterprise. All rights reserved.", className="text-muted small")
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

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
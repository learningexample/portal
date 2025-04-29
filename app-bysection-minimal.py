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
        # Shared apps section
        html.Div([
            html.Div([
                html.I(className="fa-solid fa-share-nodes fa-2x me-3", style={"color": "#00695C"}),
                html.H2("Shared Apps", className="d-inline m-0")
            ], className="d-flex align-items-center mt-4 mb-3"),
            html.P("Cross-departmental AI tools", className="lead mb-3"),
            
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Chatbot Assistant", className="card-title"),
                            html.P("An AI chatbot that can answer questions about your business.", className="card-text"),
                            dbc.Button("Launch App", color="primary")
                        ])
                    ]), 
                    md=4
                )
            ], className="g-4"),
        ], className="mb-5"),
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
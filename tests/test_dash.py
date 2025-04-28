"""
Simple Dash test script to verify basic functionality
"""
import dash
from dash import html, dcc

# Create a simple Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Test Dash App"),
    html.P("This is a simple test app to verify Dash is working correctly"),
    dcc.Input(value="Test input", type="text")
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
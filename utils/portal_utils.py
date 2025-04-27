"""
Utility functions for the Enterprise AI Portal.

This module provides helper functions that can be used across different
portal versions (app.py, app_bytab.py, app-bysection.py).

COPILOT INSTRUCTIONS:
- Contains reusable utility functions
- Follow PEP 8 style guidelines
- Use Google-style docstrings
- Prefer f-strings for string formatting
- Include proper type hints
"""

import os
import yaml
import logging
from typing import Dict, List, Any, Optional, Union
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file. If None, uses default path.
        
    Returns:
        Dictionary containing the configuration data.
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
    """
    logger = logging.getLogger('portal_utils')
    
    if config_path is None:
        # Use default path relative to project root
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Config loaded successfully with {len(config.keys())} top level keys")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at: {config_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}


def create_app_card(
    app_name: str,
    description: str,
    icon: str,
    url: str,
    icon_color: str = "#4a6fa5"
) -> dbc.Card:
    """
    Create a standard application card for the portal.
    
    Args:
        app_name: Name of the application
        description: Description text for the application
        icon: Icon class (Font Awesome)
        url: URL for the launch button
        icon_color: Hex color code for the icon
        
    Returns:
        A Dash Bootstrap Card component representing the application
    """
    card = dbc.Card([
        dbc.CardBody([
            # Card content container with flex display
            html.Div([
                # Header section
                html.Div([
                    html.I(className=f"{icon} fa-2x me-2", style={"color": icon_color}),
                    html.H5(app_name, className="card-title d-inline-block align-middle mb-0")
                ], className="d-flex align-items-center mb-3"),
                
                # Description section - will stretch to fill available space
                html.Div([
                    html.P(description, className="card-text")
                ], className="flex-grow-1 mb-3"),
                
                # Button section - always at the bottom
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-external-link-alt me-2"),
                        "Launch App"
                    ], color="primary", href=url, className="w-100")
                ])
            ], className="d-flex flex-column h-100")  # Make the div take full height of card
        ])
    ], className="mb-4 h-100")
    
    return card


def calculate_gunicorn_workers() -> int:
    """
    Calculate the recommended number of Gunicorn workers based on CPU count.
    
    Uses the formula (CPU cores × 2 + 1) as recommended by Gunicorn documentation.
    
    Returns:
        Recommended number of worker processes
    """
    import multiprocessing
    cores = multiprocessing.cpu_count()
    workers = cores * 2 + 1
    return workers


def create_standard_navbar(
    company_info: Dict[str, Any],
    app_store_title: str,
    app_store_icon: str,
    departments: List[str],
    shared_title: str,
    shared_icon: str,
    user_info: Dict[str, Any]
) -> dbc.Navbar:
    """
    Create a standard navigation bar used across portal versions.
    
    Args:
        company_info: Dictionary with company information
        app_store_title: Title for the app store section
        app_store_icon: Icon for the app store
        departments: List of department names
        shared_title: Title for shared apps section
        shared_icon: Icon for shared apps
        user_info: Dictionary with user information
        
    Returns:
        A Dash Bootstrap Navbar component
    """
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
    
    # Complete navbar
    navbar = dbc.Navbar(
        dbc.Container(
            [
                # Company Logo and Brand
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=company_info.get('logo_url', ''), height="40px"), className="me-2"),
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
                            # App Store navigation item
                            dbc.NavItem(dbc.NavLink([
                                html.I(className=f"{app_store_icon} me-2"),
                                app_store_title
                            ], href="#app-store")),
                            
                            # Department navigation menu
                            dbc.DropdownMenu(
                                [dbc.DropdownMenuItem(dept, href=f"#{dept.lower()}") for dept in departments],
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
    
    return navbar
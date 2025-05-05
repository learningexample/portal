#!/usr/bin/env python
"""
AI Portal Debug Utility

This script provides a convenient way to run any of the AI Portal versions
for development and debugging purposes.

Usage:
  python debug.py [app_name] [--port PORT] [--no-debug]

Where:
  app_name: One of 'standard', 'tabbed', 'bysection', 'bysection-fixed', 
            'bysection-minimal', or 'appstore'. Default is 'standard'.
  --port:   Port to run the server on. Default is 8050.
  --no-debug: Disables debug mode if specified.

Examples:
  python debug.py bysection --port 8080
  python debug.py appstore
  python debug.py tabbed --no-debug
"""

import sys
import os
import argparse
import importlib
from utils.log import get_logger  # Use the centralized logging module

# Set up logging for debugging
logger = get_logger('ai-portal-debug')

# Available portal versions and their corresponding module names
PORTAL_VERSIONS = {
    'standard': 'app',
    'tabbed': 'app_bytab',
    'bysection': 'app-bysection',
    'bysection-fixed': 'app-bysection-fixed',
    'bysection-minimal': 'app-bysection-minimal',
    'appstore': 'app_store'
}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run AI Portal for debugging')
    parser.add_argument('app_name', nargs='?', default='standard', 
                        choices=PORTAL_VERSIONS.keys(),
                        help='Portal version to run')
    parser.add_argument('--port', type=int, default=8050,
                        help='Port to run the server on')
    parser.add_argument('--no-debug', action='store_true',
                        help='Disable debug mode')
    return parser.parse_args()

def run_app(app_name, port, debug_mode):
    """
    Import and run the specified portal version.
    
    Args:
        app_name: Name of the portal version to run
        port: Port number to run on
        debug_mode: Whether to run in debug mode
    """
    module_name = PORTAL_VERSIONS[app_name]
    
    try:
        # Dynamically import the module
        logger.info(f"Importing {module_name}...")
        module = importlib.import_module(module_name)
        
        # Get the Dash app instance
        # Most modules use dash_app, but check for app as fallback
        app = getattr(module, 'dash_app', None)
        if app is None:
            app = getattr(module, 'app', None)
        
        if app is None:
            logger.error(f"Could not find a Dash app in {module_name}")
            sys.exit(1)
        
        # Override any existing port settings in the environment
        os.environ['PORT'] = str(port)
        
        # Print startup information
        logger.info(f"Starting {app_name} portal in {'debug' if debug_mode else 'production'} mode")
        logger.info(f"Server will be available at http://localhost:{port}/")
        logger.info("Press Ctrl+C to stop the server")
        
        # Start the app
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
        
    except ModuleNotFoundError:
        logger.error(f"Could not import {module_name}. Make sure the file exists.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running {app_name}: {e}")
        # Print more detailed error information
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    args = parse_args()
    run_app(args.app_name, args.port, not args.no_debug)
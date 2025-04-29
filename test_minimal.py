"""
Test the minimal version of app-bysection.py
"""

import dash
import importlib.util
import os
import sys

try:
    # Import the app variable from the minimal app file
    script_path = os.path.join(os.path.dirname(__file__), 'app-bysection-minimal.py')
    spec = importlib.util.spec_from_file_location('app_minimal', script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Check if app exists and is a Dash instance
    app = getattr(module, 'app')
    
    print("✓ SUCCESS: The minimal app was successfully imported.")
    print(f"  - app is of type: {type(app)}")
    print(f"  - app is a Dash instance: {isinstance(app, dash.Dash)}")
    sys.exit(0)
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__} occurred: {e}")
    sys.exit(1)
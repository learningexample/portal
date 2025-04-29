"""
Simple test script to check if app-bysection.py loads correctly
"""

import dash
import sys
import importlib.util
import os

try:
    # Import the app variable from the app-bysection.py file using importlib
    script_path = os.path.join(os.path.dirname(__file__), 'app-bysection.py')
    spec = importlib.util.spec_from_file_location('app_bysection', script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Check if app exists and is a Dash instance
    app = getattr(module, 'app')
    
    print("✓ SUCCESS: The app was successfully imported.")
    print(f"  - app is of type: {type(app)}")
    print(f"  - app is a Dash instance: {isinstance(app, dash.Dash)}")
    sys.exit(0)
except AttributeError as e:
    print(f"✗ ERROR: AttributeError occurred: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ ERROR: Unexpected error: {e}")
    print(f"  Error type: {type(e).__name__}")
    sys.exit(1)
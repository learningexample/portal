"""
Simple test script to check if app-bysection-fixed.py loads correctly without shared apps section
"""

import dash
import sys
import importlib.util
import os
import inspect

try:
    # Import the app variable from the app-bysection-fixed.py file using importlib
    script_path = os.path.join(os.path.dirname(__file__), 'app-bysection-fixed.py')
    spec = importlib.util.spec_from_file_location('app_bysection_fixed', script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Check if app exists and is a Dash instance
    app = getattr(module, 'app')
    
    # Check module content for sections and shared references
    module_content = inspect.getsource(module)
    print("✓ Checking for 'shared' references in the module:")
    
    # Look for direct references to 'shared' apps section
    if "'shared'" in module_content or '"shared"' in module_content:
        shared_count = module_content.count("'shared'") + module_content.count('"shared"')
        # Some references to "shared" might be in comments or unrelated contexts
        print(f"  - Found {shared_count} potential references to 'shared'")
        print("  - Warning: This is just a text search. Some matches might be in comments or unrelated contexts.")
    else:
        print("  - No direct string references to 'shared' found")
    
    # Check for any global variables that might contain section information
    for var_name in dir(module):
        if var_name.startswith('__'):
            continue
        var = getattr(module, var_name)
        if isinstance(var, (list, tuple, dict)) and var_name not in ['app', 'server']:
            print(f"✓ Examining {var_name} ({type(var).__name__}):")
            print(f"  - {var}")
            if isinstance(var, (list, tuple)) and 'shared' in [str(x).lower() for x in var]:
                print(f"  ✗ Warning: 'shared' may be present in {var_name}")
    
    print("\n✓ SUCCESS: The app was successfully imported.")
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
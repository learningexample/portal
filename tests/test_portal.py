"""
Enterprise AI Portal - Comprehensive Test Suite

This file contains tests for both versions of the Enterprise AI Portal 
(app.py and app_bytab.py), covering configuration loading, initialization,
UI components, routing, and callbacks.
"""

import unittest
import os
import sys
import yaml
from unittest.mock import patch, MagicMock

# Add additional imports for testing Dash apps
from dash.testing.application_runners import import_app


class BasePortalTestCase(unittest.TestCase):
    """Base test case with common utility methods for portal testing."""
    
    def setUp(self):
        # Ensure we're in the right directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, 'config.yaml')
        
        # Load the config file for testing
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config = {}
    
    def load_app(self, module_name):
        """Helper to load an app module for testing"""
        sys.path.insert(0, self.base_dir)
        try:
            # This approach avoids actually starting the app server
            app_module = __import__(module_name)
            return app_module
        except ImportError as e:
            self.fail(f"Failed to import {module_name}: {str(e)}")


class ConfigurationTests(BasePortalTestCase):
    """Tests for configuration loading and validation."""
    
    def test_config_file_exists(self):
        """Test that config.yaml exists."""
        self.assertTrue(os.path.exists(self.config_path), 
                       "config.yaml file should exist")
    
    def test_config_has_required_sections(self):
        """Test that config has all required top-level sections."""
        required_sections = ['title', 'company', 'departments', 'shared', 'app_store']
        for section in required_sections:
            self.assertIn(section, self.config, 
                         f"Config should have '{section}' section")
    
    def test_company_config(self):
        """Test company configuration section."""
        company = self.config.get('company', {})
        required_fields = ['name', 'logo_url']
        for field in required_fields:
            self.assertIn(field, company,
                         f"Company config should have '{field}' field")
    
    def test_departments_config(self):
        """Test departments configuration section."""
        departments = self.config.get('departments', [])
        self.assertGreater(len(departments), 0, "Should have at least one department")
        
        # Check first department for required structure
        first_dept = departments[0]
        required_fields = ['name', 'icon', 'description', 'apps']
        for field in required_fields:
            self.assertIn(field, first_dept,
                         f"Department should have '{field}' field")
        
        # Check apps in first department
        apps = first_dept.get('apps', [])
        self.assertGreater(len(apps), 0, "Department should have at least one app")
        
        # Check first app for required structure
        first_app = apps[0]
        app_required_fields = ['name', 'url', 'description']
        for field in app_required_fields:
            self.assertIn(field, first_app,
                         f"App should have '{field}' field")


class OriginalAppTests(BasePortalTestCase):
    """Tests for the original app.py version."""
    
    def setUp(self):
        super().setUp()
        # Mock the Flask app to avoid actually starting the server
        self.server_patch = patch('dash.Dash.run_server')
        self.server_mock = self.server_patch.start()
        
        # Import app without running the server
        with patch('dash.Dash.run_server'):
            self.app_module = self.load_app('app')
            self.app = self.app_module.app
    
    def tearDown(self):
        self.server_patch.stop()
    
    def test_app_initialization(self):
        """Test that app initializes correctly."""
        self.assertIsNotNone(self.app, "App should be initialized")
        self.assertEqual(self.app.title, 
                        f"{self.config['company']['name']} AI Portal",
                        "App title should be set correctly")
    
    def test_server_exposed(self):
        """Test that Flask server is exposed for Gunicorn."""
        self.assertIsNotNone(self.app_module.server, 
                            "Flask server should be exposed")
    
    def test_layout_components(self):
        """Test that main layout components exist."""
        layout = self.app.layout
        self.assertIsNotNone(layout, "App should have a layout")
        
        # Check for key components by their IDs
        component_ids = self.get_component_ids(layout)
        expected_ids = ['url', 'navbar-toggler', 'navbar-collapse']
        for component_id in expected_ids:
            self.assertIn(component_id, component_ids, 
                         f"Layout should contain component with id '{component_id}'")
    
    def get_component_ids(self, layout):
        """Helper method to extract component IDs from layout."""
        ids = []
        
        # Check if the component has an ID
        if hasattr(layout, 'id') and layout.id is not None:
            ids.append(layout.id)
        
        # Check if the component has children
        if hasattr(layout, 'children'):
            children = layout.children
            if children is not None:
                if isinstance(children, list):
                    for child in children:
                        ids.extend(self.get_component_ids(child))
                else:
                    ids.extend(self.get_component_ids(children))
        
        return ids
    
    def test_callback_registration(self):
        """Test that callbacks are registered."""
        callbacks = self.app._callback_list
        self.assertGreater(len(callbacks), 0, "App should have callbacks registered")


class TabbedAppTests(BasePortalTestCase):
    """Tests for the tabbed app_bytab.py version."""
    
    def setUp(self):
        super().setUp()
        # Mock the Flask app to avoid actually starting the server
        self.server_patch = patch('dash.Dash.run')
        self.server_mock = self.server_patch.start()
        
        # Import app without running the server
        with patch('dash.Dash.run'):
            self.app_module = self.load_app('app_bytab')
            self.app = self.app_module.app
    
    def tearDown(self):
        self.server_patch.stop()
    
    def test_app_initialization(self):
        """Test that tabbed app initializes correctly."""
        self.assertIsNotNone(self.app, "Tabbed app should be initialized")
        company_name = self.config['company']['name']
        portal_title = self.config['title']
        self.assertEqual(self.app.title, 
                        f"{company_name} {portal_title} (Tabbed)",
                        "Tabbed app title should be set correctly")
    
    def test_server_exposed(self):
        """Test that Flask server is exposed for Gunicorn."""
        self.assertIsNotNone(self.app_module.server, 
                            "Flask server should be exposed in tabbed app")
    
    def test_tabs_exist(self):
        """Test that tabs component exists in layout."""
        layout = self.app.layout
        component_ids = self.get_component_ids(layout)
        self.assertIn('tabs', component_ids, "Layout should contain tabs component")
        self.assertIn('tab-content', component_ids, "Layout should contain tab content area")
    
    def get_component_ids(self, layout):
        """Helper method to extract component IDs from layout."""
        ids = []
        
        # Check if the component has an ID
        if hasattr(layout, 'id') and layout.id is not None:
            ids.append(layout.id)
        
        # Check if the component has children
        if hasattr(layout, 'children'):
            children = layout.children
            if children is not None:
                if isinstance(children, list):
                    for child in children:
                        ids.extend(self.get_component_ids(child))
                else:
                    ids.extend(self.get_component_ids(children))
        
        return ids
    
    def test_tab_callback(self):
        """Test that tab callback is registered."""
        callbacks = self.app._callback_list
        tab_callbacks = [c for c in callbacks if 'tab-content' in str(c.output)]
        self.assertGreater(len(tab_callbacks), 0, 
                          "Tabbed app should have tab callback registered")


class PortalUtilitiesTest(BasePortalTestCase):
    """Tests for portal utility functions."""
    
    def setUp(self):
        super().setUp()
        sys.path.insert(0, os.path.join(self.base_dir, 'utils'))
        try:
            import portal_utils
            self.portal_utils = portal_utils
        except ImportError:
            self.skipTest("portal_utils.py not found or couldn't be imported")
    
    def test_utils_imported(self):
        """Test that utils module can be imported."""
        self.assertIsNotNone(self.portal_utils, "Portal utils module should be importable")


class PortalManagerTest(BasePortalTestCase):
    """Tests for portal_manager.py functionality."""
    
    def test_manager_exists(self):
        """Test that portal_manager.py exists."""
        manager_path = os.path.join(self.base_dir, 'portal_manager.py')
        self.assertTrue(os.path.exists(manager_path), 
                       "portal_manager.py file should exist")


if __name__ == '__main__':
    unittest.main()
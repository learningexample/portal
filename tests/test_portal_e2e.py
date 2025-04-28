"""
Enterprise AI Portal - End-to-End Integration Tests

This file contains end-to-end integration tests for the Enterprise AI Portal
using Selenium WebDriver to test the actual rendering and functionality
of the portal in a browser environment.
"""

import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import multiprocessing
import sys
import yaml
import requests


class PortalE2ETests(unittest.TestCase):
    """End-to-end integration tests for the Enterprise AI Portal."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment and start the portal server."""
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load config to get company name for test validation
        try:
            with open(os.path.join(cls.base_dir, 'config.yaml'), 'r') as file:
                cls.config = yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            cls.config = {}
        
        # Set up Chrome options for headless testing
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Start each app server in a separate process
        cls.app_process = cls.start_app_server('app.py', 8050)
        cls.app_bytab_process = cls.start_app_server('app_bytab.py', 8051)
        
        # Wait for servers to start
        time.sleep(2)
        
        # Set up WebDriver
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.set_window_size(1280, 800)
        except WebDriverException:
            print("Chrome WebDriver not available, tests will be skipped")
            cls.driver = None
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        # Quit the web driver
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()
        
        # Terminate app processes
        if hasattr(cls, 'app_process') and cls.app_process:
            cls.app_process.terminate()
            cls.app_process.join(timeout=1)
        
        if hasattr(cls, 'app_bytab_process') and cls.app_bytab_process:
            cls.app_bytab_process.terminate()
            cls.app_bytab_process.join(timeout=1)
    
    @classmethod
    def start_app_server(cls, app_file, port):
        """Start a Dash app server in a separate process."""
        def run_server(app_path, port):
            import importlib.util
            import sys
            
            # Use importlib to load the module from file path
            spec = importlib.util.spec_from_file_location("app_module", app_path)
            app_module = importlib.util.module_from_spec(spec)
            sys.modules["app_module"] = app_module
            spec.loader.exec_module(app_module)
            
            # Find the app instance - could be named app or dash_app
            app = getattr(app_module, "app", None)
            if app is None:
                app = getattr(app_module, "dash_app", None)
            
            # Run the server
            if app:
                app.run_server(debug=False, host='localhost', port=port)
        
        # Create and start the process
        app_path = os.path.join(cls.base_dir, app_file)
        process = multiprocessing.Process(
            target=run_server, 
            args=(app_path, port)
        )
        process.daemon = True
        process.start()
        return process
    
    def setUp(self):
        """Set up for each test."""
        if not self.driver:
            self.skipTest("WebDriver not available")
    
    def test_original_app_loads(self):
        """Test that the original app loads correctly."""
        # Check if server is responding
        try:
            response = requests.get("http://localhost:8050/portal-1/", timeout=1)
            if response.status_code != 200:
                self.skipTest(f"App server not responding: {response.status_code}")
        except requests.exceptions.RequestException:
            self.skipTest("App server not responding to HTTP requests")
            
        # Load the original portal
        self.driver.get("http://localhost:8050/portal-1/")
        
        try:
            # Wait for page to load (logo to appear)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='logo']"))
            )
            
            # Check that the company name appears in the navbar
            company_name = self.config.get('company', {}).get('name', 'TechCorp')
            navbar_text = self.driver.find_element(By.CSS_SELECTOR, ".navbar").text
            self.assertIn(company_name, navbar_text, f"Company name '{company_name}' should appear in navbar")
            
            # Check that department sections exist
            departments = [dept['name'] for dept in self.config.get('departments', [])]
            for dept in departments:
                try:
                    section_id = dept.lower()
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, section_id))
                    )
                    self.assertIsNotNone(element, f"Section for {dept} should exist")
                except TimeoutException:
                    self.fail(f"Section for department '{dept}' not found")
        except Exception as e:
            self.fail(f"Error testing original app: {str(e)}")
    
    def test_tabbed_app_loads(self):
        """Test that the tabbed app loads correctly."""
        # Check if server is responding
        try:
            response = requests.get("http://localhost:8051/portal-2/", timeout=1)
            if response.status_code != 200:
                self.skipTest(f"Tabbed app server not responding: {response.status_code}")
        except requests.exceptions.RequestException:
            self.skipTest("Tabbed app server not responding to HTTP requests")
            
        # Load the tabbed portal
        self.driver.get("http://localhost:8051/portal-2/")
        
        try:
            # Wait for page to load (tabs to appear)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "tabs"))
            )
            
            # Check that the company name appears in the navbar
            company_name = self.config.get('company', {}).get('name', 'TechCorp')
            navbar_text = self.driver.find_element(By.CSS_SELECTOR, ".navbar").text
            self.assertIn(company_name, navbar_text, f"Company name '{company_name}' should appear in navbar in tabbed app")
            
            # Check that tabs work by clicking on one
            first_dept_tab = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#tabs .nav-link:nth-child(2)"))
            )
            first_dept_tab.click()
            
            # Wait for tab content to update
            time.sleep(1)
            
            # Check that tab content contains department apps
            tab_content = self.driver.find_element(By.ID, "tab-content").text
            self.assertNotEqual(tab_content.strip(), "", "Tab content should not be empty after tab click")
        except Exception as e:
            self.fail(f"Error testing tabbed app: {str(e)}")
    
    def test_app_cards_render(self):
        """Test that application cards render correctly in both apps."""
        # Test original app
        self.driver.get("http://localhost:8050/portal-1/")
        
        try:
            # Wait for page to load and check for app cards
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
            )
            
            cards = self.driver.find_elements(By.CSS_SELECTOR, ".card")
            self.assertGreater(len(cards), 0, "Original app should display app cards")
            
            # Check card elements
            first_card = cards[0]
            self.assertIsNotNone(first_card.find_element(By.CSS_SELECTOR, ".card-title"), 
                               "Card should have a title")
            self.assertIsNotNone(first_card.find_element(By.CSS_SELECTOR, ".btn-primary"), 
                               "Card should have a launch button")
        except Exception as e:
            self.fail(f"Error testing app cards in original app: {str(e)}")
        
        # Test tabbed app
        self.driver.get("http://localhost:8051/portal-2/")
        
        try:
            # Wait for page to load and check for app cards
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
            )
            
            cards = self.driver.find_elements(By.CSS_SELECTOR, ".card")
            self.assertGreater(len(cards), 0, "Tabbed app should display app cards")
            
            # Check card elements
            first_card = cards[0]
            self.assertIsNotNone(first_card.find_element(By.CSS_SELECTOR, ".card-title"), 
                               "Card should have a title in tabbed app")
            self.assertIsNotNone(first_card.find_element(By.CSS_SELECTOR, ".btn-primary"), 
                               "Card should have a launch button in tabbed app")
        except Exception as e:
            self.fail(f"Error testing app cards in tabbed app: {str(e)}")
    
    def test_responsive_design(self):
        """Test that the portal has responsive design elements."""
        # Test at mobile width
        self.driver.set_window_size(480, 800)
        self.driver.get("http://localhost:8050/portal-1/")
        
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-toggler"))
            )
            
            # Check that navbar toggler is visible at mobile width
            toggler = self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
            self.assertTrue(toggler.is_displayed(), "Navbar toggler should be visible at mobile width")
            
            # Restore window size
            self.driver.set_window_size(1280, 800)
        except Exception as e:
            self.fail(f"Error testing responsive design: {str(e)}")


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python3
"""
Enterprise AI Portal Management Script
A GUI tool to manage the Enterprise AI Portal with tabs for shared apps and departments
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import yaml
import webbrowser
from datetime import datetime

class PortalManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise AI Portal Manager")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Set icon if available
        try:
            self.root.iconphoto(False, tk.PhotoImage(file="assets/images/favicon.png"))
        except:
            pass  # If icon isn't available, just continue
            
        # Load config
        self.config = self.load_config()
        
        # Company info from config
        company_name = self.config.get('company', {}).get('name', 'Enterprise')
        self.portal_title = f"{company_name} AI Portal"
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        title_label = ttk.Label(header_frame, text=self.portal_title, font=("Helvetica", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Date display
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%B %d, %Y"))
        date_label = ttk.Label(header_frame, textvariable=self.date_var, font=("Helvetica", 12))
        date_label.pack(side=tk.RIGHT)
        
        # Create notebook with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Management tab
        self.management_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.management_tab, text="Management")
        self.setup_management_tab()
        
        # Create tab for shared apps
        self.shared_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.shared_tab, text="Shared Apps")
        self.setup_apps_tab(self.shared_tab, "shared")
        
        # Create tabs for each department
        self.department_tabs = {}
        for dept in self.config.get('departments', []):
            dept_name = dept['name']
            dept_tab = ttk.Frame(self.notebook)
            self.notebook.add(dept_tab, text=dept_name)
            self.setup_apps_tab(dept_tab, dept_name)
            self.department_tabs[dept_name] = dept_tab
            
        # Add App Store tab
        self.app_store_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.app_store_tab, text="App Store")
        self.setup_apps_tab(self.app_store_tab, "App Store")
            
    def load_config(self):
        """Load configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return {}
            
    def setup_management_tab(self):
        """Setup the management tab with portal control buttons"""
        # Container for control buttons
        control_frame = ttk.LabelFrame(self.management_tab, text="Portal Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Control buttons
        btn_width = 15
        
        build_btn = ttk.Button(control_frame, text="Build", width=btn_width, 
                               command=lambda: self.run_command("build"))
        build_btn.grid(row=0, column=0, padx=5, pady=5)
        
        run_btn = ttk.Button(control_frame, text="Run", width=btn_width, 
                             command=lambda: self.run_command("run"))
        run_btn.grid(row=0, column=1, padx=5, pady=5)
        
        stop_btn = ttk.Button(control_frame, text="Stop", width=btn_width, 
                              command=lambda: self.run_command("stop"))
        stop_btn.grid(row=0, column=2, padx=5, pady=5)
        
        restart_btn = ttk.Button(control_frame, text="Restart", width=btn_width, 
                                 command=lambda: self.run_command("restart"))
        restart_btn.grid(row=1, column=0, padx=5, pady=5)
        
        local_run_btn = ttk.Button(control_frame, text="Run Locally", width=btn_width, 
                                   command=self.run_locally)
        local_run_btn.grid(row=1, column=1, padx=5, pady=5)
        
        open_browser_btn = ttk.Button(control_frame, text="Open in Browser", width=btn_width, 
                                      command=self.open_in_browser)
        open_browser_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Status section
        status_frame = ttk.LabelFrame(self.management_tab, text="Portal Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Text widget for command output
        self.output_text = tk.Text(status_frame, height=20, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for text widget
        scrollbar = ttk.Scrollbar(self.output_text, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Initial status display
        self.update_status()
        
    def setup_apps_tab(self, tab, category_name):
        """Setup a tab for app categories with app cards"""
        # Create a canvas with scrollbar
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Apps container
        apps_container = ttk.Frame(scrollable_frame)
        apps_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get apps for this category
        apps = []
        if category_name.lower() == "shared":
            apps = self.config.get('shared', {}).get('apps', [])
        elif category_name.lower() == "app store":
            apps = self.config.get('app_store', {}).get('apps', [])
        else:
            # Find the department in the config
            for dept in self.config.get('departments', []):
                if dept['name'] == category_name:
                    apps = dept.get('apps', [])
                    break
        
        # Create app cards
        row = 0
        col = 0
        max_cols = 3
        
        if not apps:
            no_apps_label = ttk.Label(apps_container, text=f"No applications found for {category_name}")
            no_apps_label.grid(row=0, column=0, padx=10, pady=10)
        
        for app in apps:
            # Create a card frame for each app
            card = ttk.LabelFrame(apps_container, text=app['name'])
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # App description
            desc_text = tk.Text(card, wrap=tk.WORD, height=4, width=30)
            desc_text.insert(tk.END, app.get('description', 'No description available.'))
            desc_text.config(state=tk.DISABLED)
            desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # URL label
            url_var = tk.StringVar(value=app.get('url', ''))
            url_label = ttk.Label(card, textvariable=url_var)
            url_label.pack(padx=5, pady=2)
            
            # Launch button
            launch_btn = ttk.Button(card, text="Launch App", 
                                   command=lambda u=app.get('url', ''): self.launch_app(u))
            launch_btn.pack(padx=5, pady=5)
            
            # Move to next grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
        # Make grid cells expandable
        for i in range(max_cols):
            apps_container.columnconfigure(i, weight=1)
            
    def run_command(self, command):
        """Run a command from the run.bat script"""
        self.update_status(f"Running command: {command}...")
        self.output_text.delete(1.0, tk.END)
        
        # Run in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._execute_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _execute_command(self, command):
        """Execute the command in a separate thread"""
        if os.name == 'nt':  # Windows
            cmd = f"cmd.exe /c run.bat {command}"
        else:  # Unix/Linux/Mac
            cmd = f"./run.sh {command}"
            
        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
            
            # Stream output
            while True:
                output_line = process.stdout.readline()
                if output_line == '' and process.poll() is not None:
                    break
                if output_line:
                    self.output_text.insert(tk.END, output_line)
                    self.output_text.see(tk.END)
                    self.root.update_idletasks()
            
            # Get any remaining output
            remaining_stdout, remaining_stderr = process.communicate()
            if remaining_stdout:
                self.output_text.insert(tk.END, remaining_stdout)
            if remaining_stderr:
                self.output_text.insert(tk.END, f"\nERROR: {remaining_stderr}")
                
            self.output_text.see(tk.END)
            
            # Update status
            if process.returncode == 0:
                self.update_status(f"Command '{command}' completed successfully")
            else:
                self.update_status(f"Command '{command}' failed with exit code {process.returncode}")
                
        except Exception as e:
            error_msg = f"Error executing command: {e}"
            self.output_text.insert(tk.END, f"\n{error_msg}")
            self.update_status(error_msg)
            
    def run_locally(self):
        """Run the app locally using Python"""
        self.update_status("Starting application locally...")
        self.output_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self._run_local_process)
        thread.daemon = True
        thread.start()
        
    def _run_local_process(self):
        """Run the Python app process in a thread"""
        try:
            cmd = [sys.executable, "app.py"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Show initial message
            self.output_text.insert(tk.END, "Starting local server...\n")
            self.output_text.see(tk.END)
            
            # Stream output
            while True:
                output_line = process.stdout.readline()
                if output_line == '' and process.poll() is not None:
                    break
                if output_line:
                    self.output_text.insert(tk.END, output_line)
                    self.output_text.see(tk.END)
                    
                    # If we see the "Running on" message, open the browser
                    if "Running on" in output_line and "http" in output_line:
                        self.root.after(1000, self.open_in_browser)
                    
                    self.root.update_idletasks()
            
            # Get any remaining output
            remaining_stdout, remaining_stderr = process.communicate()
            if remaining_stdout:
                self.output_text.insert(tk.END, remaining_stdout)
            if remaining_stderr:
                self.output_text.insert(tk.END, f"\nERROR: {remaining_stderr}")
                
            self.output_text.see(tk.END)
            
            if process.returncode == 0:
                self.update_status("Local server stopped")
            else:
                self.update_status(f"Local server failed with exit code {process.returncode}")
                
        except Exception as e:
            error_msg = f"Error running local server: {e}"
            self.output_text.insert(tk.END, f"\n{error_msg}")
            self.update_status(error_msg)
            
    def open_in_browser(self):
        """Open the application in a web browser"""
        # Add dropdown menu to select which portal version to open
        portal_window = tk.Toplevel(self.root)
        portal_window.title("Select Portal Version")
        portal_window.geometry("300x200")
        portal_window.resizable(False, False)
        
        # Center the window
        portal_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50))
        
        # Add instructions
        ttk.Label(portal_window, text="Select a portal version to open:").pack(pady=10)
        
        # Create radio buttons for selection
        portal_var = tk.StringVar(value="portal-1")
        
        ttk.Radiobutton(portal_window, text="Original Portal", 
                       variable=portal_var, value="portal-1").pack(anchor=tk.W, padx=20, pady=5)
        ttk.Radiobutton(portal_window, text="Tabbed Portal", 
                       variable=portal_var, value="portal-2").pack(anchor=tk.W, padx=20, pady=5)
        ttk.Radiobutton(portal_window, text="Section Portal", 
                       variable=portal_var, value="portal-3").pack(anchor=tk.W, padx=20, pady=5)
        ttk.Radiobutton(portal_window, text="App Store Style", 
                       variable=portal_var, value="portal-4").pack(anchor=tk.W, padx=20, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(portal_window)
        btn_frame.pack(pady=10)
        
        # Open button
        open_btn = ttk.Button(btn_frame, text="Open", 
                             command=lambda: self._open_selected_portal(portal_var.get(), portal_window))
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                               command=portal_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def _open_selected_portal(self, portal_path, window=None):
        """Open the selected portal version"""
        if window:
            window.destroy()
            
        url = f"http://localhost:8050/{portal_path}/"
        try:
            webbrowser.open(url)
            self.update_status(f"Opening {url} in browser")
        except Exception as e:
            self.update_status(f"Error opening browser: {e}")
            
    def launch_app(self, url_path):
        """Launch a specific app by its URL path"""
        # If the portal is running
        if url_path.startswith('/'):
            # Open a dialog to select which portal version to use
            portal_window = tk.Toplevel(self.root)
            portal_window.title("Select Portal Version")
            portal_window.geometry("300x200")
            portal_window.resizable(False, False)
            
            # Center the window
            portal_window.geometry("+%d+%d" % (
                self.root.winfo_rootx() + 50,
                self.root.winfo_rooty() + 50))
            
            # Add instructions
            ttk.Label(portal_window, text="Select a portal version:").pack(pady=10)
            
            # Create radio buttons for selection
            portal_var = tk.StringVar(value="portal-1")
            
            ttk.Radiobutton(portal_window, text="Original Portal", 
                           variable=portal_var, value="portal-1").pack(anchor=tk.W, padx=20, pady=5)
            ttk.Radiobutton(portal_window, text="Tabbed Portal", 
                           variable=portal_var, value="portal-2").pack(anchor=tk.W, padx=20, pady=5)
            ttk.Radiobutton(portal_window, text="Section Portal", 
                           variable=portal_var, value="portal-3").pack(anchor=tk.W, padx=20, pady=5)
            ttk.Radiobutton(portal_window, text="App Store Style", 
                           variable=portal_var, value="portal-4").pack(anchor=tk.W, padx=20, pady=5)
            
            # Button frame
            btn_frame = ttk.Frame(portal_window)
            btn_frame.pack(pady=10)
            
            # Open button
            open_btn = ttk.Button(
                btn_frame, 
                text="Open", 
                command=lambda: self._launch_app_in_portal(url_path, portal_var.get(), portal_window)
            )
            open_btn.pack(side=tk.LEFT, padx=5)
            
            # Cancel button
            cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                                   command=portal_window.destroy)
            cancel_btn.pack(side=tk.LEFT, padx=5)
        else:
            url = url_path
            try:
                webbrowser.open(url)
                self.update_status(f"Opening {url} in browser")
            except Exception as e:
                self.update_status(f"Error opening app: {e}")
    
    def _launch_app_in_portal(self, url_path, portal_version, window=None):
        """Launch an app in the selected portal version"""
        if window:
            window.destroy()
            
        url = f"http://localhost:8050/{portal_version}{url_path}"
        try:
            webbrowser.open(url)
            self.update_status(f"Opening {url} in browser")
        except Exception as e:
            self.update_status(f"Error opening app: {e}")
            
    def update_status(self, message=None):
        """Update the status bar message"""
        if message:
            self.status_var.set(message)
        else:
            # Check if container is running
            if os.name == 'nt':  # Windows
                cmd = "docker ps | findstr \"ai-portal\""
            else:  # Unix/Linux/Mac
                cmd = "docker ps | grep ai-portal"
                
            try:
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    self.status_var.set("Portal is running")
                else:
                    self.status_var.set("Portal is stopped")
            except:
                self.status_var.set("Status unknown")

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = PortalManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
Enterprise AI Portal - Logging Utility Module

This module provides centralized logging functionality for the AI Portal application.
It includes:
- Setup for file and console logging with rotation
- Activity logging for user interactions
- Performance logging
- Helper functions for common logging patterns

Usage:
    from utils.log import get_logger, log_activity, setup_logging
    
    # Get a logger for a specific module
    logger = get_logger('my_module')
    
    # Log regular messages
    logger.info("Operation completed successfully")
    logger.error("An error occurred")
    
    # Log user activity
    log_activity("user_name", "launch_app", "ChatGPT", "/chatgpt")
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


# Default log directory
DEFAULT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

# Log formats
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
ACTIVITY_LOG_FORMAT = '%(asctime)s - %(message)s'

# Create logs directory if it doesn't exist
if not os.path.exists(DEFAULT_LOG_DIR):
    try:
        os.makedirs(DEFAULT_LOG_DIR)
    except Exception as e:
        print(f"Warning: Could not create logs directory: {e}")


def setup_logging(module_name='ai_portal', level=logging.INFO, log_dir=None,
                  log_format=None, max_bytes=10485760, backup_count=5):
    """
    Setup logging with rotation to prevent large files.
    
    Args:
        module_name (str): Name of the module (used for the logger and log file name)
        level (int): Logging level (default: logging.INFO)
        log_dir (str): Directory to store log files (default: '<project_root>/logs')
        log_format (str): Format string for log messages
        max_bytes (int): Maximum size of each log file before rotation (default: 10MB)
        backup_count (int): Number of backup log files to keep (default: 5)
        
    Returns:
        logging.Logger: Configured logger object
    """
    if log_dir is None:
        log_dir = DEFAULT_LOG_DIR
        
    if log_format is None:
        log_format = DEFAULT_LOG_FORMAT
        
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception as e:
            print(f"Warning: Could not create logs directory: {e}")
    
    # Set up the logger
    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates when called multiple times
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create rotating file handler
    log_file_path = os.path.join(log_dir, f'{module_name}.log')
    try:
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")
    
    return logger


def get_logger(module_name='ai_portal', level=None):
    """
    Get a logger for the specified module. If the logger doesn't exist,
    create it with default settings.
    
    Args:
        module_name (str): Name of the module
        level (int): Optional logging level override
        
    Returns:
        logging.Logger: Logger object
    """
    logger = logging.getLogger(module_name)
    
    # If logger has no handlers, set it up
    if not logger.handlers:
        logger = setup_logging(module_name=module_name)
    
    # Override level if specified
    if level is not None:
        logger.setLevel(level)
        
    return logger


def setup_activity_logging():
    """
    Set up a dedicated logger for user activity tracking.
    
    Returns:
        logging.Logger: Logger configured for activity logging
    """
    activity_logger = logging.getLogger('ai_portal_activity')
    activity_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for handler in activity_logger.handlers[:]:
        activity_logger.removeHandler(handler)
    
    # Create formatter with simpler format for activity logs
    formatter = logging.Formatter(ACTIVITY_LOG_FORMAT)
    
    # Create rotating file handler for activity logs
    log_file_path = os.path.join(DEFAULT_LOG_DIR, 'ai_portal_activity.log')
    try:
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        activity_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up activity logging: {e}")
        
    return activity_logger


def log_activity(user_name, action_type, target, url=None, details=None):
    """
    Log user activity in a standardized format.
    
    Args:
        user_name (str): Name or ID of the user
        action_type (str): Type of action (e.g., 'launch_app', 'contact', 'login')
        target (str): Target of the action (e.g., app name, feature)
        url (str, optional): URL associated with the action
        details (dict, optional): Additional details about the action
    """
    activity_logger = get_logger('ai_portal_activity')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url_part = f" | URL: {url}" if url else ""
    details_part = f" | Details: {details}" if details else ""
    
    activity_logger.info(f"User Activity: {timestamp} | User: {user_name} | Action: {action_type} | Target: {target}{url_part}{details_part}")


def log_button_click(app_name, button_type, url, user_info=None):
    """
    Log when a user clicks on a Launch App or Contact button.
    
    Args:
        app_name (str): Name of the application
        button_type (str): Type of button ('Launch App', 'Contact', etc.)
        url (str): URL the button links to
        user_info (dict, optional): Dictionary containing user information
    """
    if user_info is None:
        user_info = {}
        
    user_name = user_info.get('name', 'Unknown User')
    user_role = user_info.get('role', 'Unknown Role')
    user_dept = user_info.get('department', 'Unknown Department')
    
    logger = get_logger('ai_portal')
    logger.info(f"Button Click | User: {user_name} ({user_role}, {user_dept}) | App: {app_name} | Action: {button_type} | URL: {url}")


def log_performance(operation, execution_time, success=True, details=None):
    """
    Log performance metrics for operations.
    
    Args:
        operation (str): Name of the operation being measured
        execution_time (float): Execution time in seconds
        success (bool): Whether the operation was successful
        details (dict, optional): Additional details about the operation
    """
    perf_logger = get_logger('ai_portal_performance')
    
    status = "Success" if success else "Failed"
    details_part = f" | Details: {details}" if details else ""
    
    perf_logger.info(f"Performance | Operation: {operation} | Time: {execution_time:.4f}s | Status: {status}{details_part}")


# Initialize default loggers
default_logger = setup_logging()
activity_logger = setup_activity_logging()

# Set up logging for the main application
logging.basicConfig(
    level=logging.INFO,
    format=DEFAULT_LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
        # File handlers are added by setup_logging
    ]
)
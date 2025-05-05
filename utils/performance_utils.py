"""
Performance optimization utilities for the Enterprise AI Portal.

This module provides caching and optimization helpers to reduce
resource consumption when running on the server.
"""

import functools
import time
import gc
from typing import Dict, Any, Callable, Optional
import logging
from utils.log import get_logger

# Get logger for this module from the centralized logging module
logger = get_logger('performance_utils')

# Simple memory cache
_cache: Dict[str, Dict[str, Any]] = {}

def memory_cache(ttl_seconds: int = 300):
    """
    Simple memory cache decorator to avoid redundant computations.
    
    Args:
        ttl_seconds: Time-to-live in seconds for cached items
    
    Returns:
        Decorated function with caching
    """
    def decorator(func):
        cache_key = func.__name__
        if cache_key not in _cache:
            _cache[cache_key] = {'items': {}, 'timestamps': {}}
            
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a hash from arguments
            arg_key = str(args) + str(sorted(kwargs.items()))
            cache = _cache[cache_key]
            
            # Check if we have a valid cached value
            current_time = time.time()
            if arg_key in cache['items'] and current_time - cache['timestamps'][arg_key] < ttl_seconds:
                logger.debug(f"Cache hit for {func.__name__}")
                return cache['items'][arg_key]
                
            # Compute and store result
            result = func(*args, **kwargs)
            cache['items'][arg_key] = result
            cache['timestamps'][arg_key] = current_time
            logger.debug(f"Cache miss for {func.__name__}, stored new result")
            return result
            
        return wrapper
    return decorator

def cleanup_cache():
    """
    Clean expired cache entries to free up memory.
    """
    current_time = time.time()
    cleanup_count = 0
    
    for cache_key, cache in _cache.items():
        expired_keys = []
        for arg_key, timestamp in cache['timestamps'].items():
            # Default TTL of 10 minutes if not otherwise specified
            if current_time - timestamp > 600:
                expired_keys.append(arg_key)
                
        # Remove expired entries
        for key in expired_keys:
            del cache['items'][key]
            del cache['timestamps'][key]
            cleanup_count += 1
            
    logger.info(f"Cleaned up {cleanup_count} expired cache entries")
    
    # Force garbage collection
    gc.collect()
    
def measure_execution_time(func):
    """
    Decorator to measure function execution time.
    Useful for identifying performance bottlenecks.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {execution_time:.4f} seconds to execute")
        return result
    return wrapper

# Periodic cache cleanup on module load
import threading
def _schedule_cache_cleanup():
    cleanup_cache()
    # Schedule next cleanup in 5 minutes
    threading.Timer(300, _schedule_cache_cleanup).start()

# Start the cache cleanup thread
_cleanup_thread = threading.Timer(300, _schedule_cache_cleanup)
_cleanup_thread.daemon = True  # Allow the thread to exit when the program does
_cleanup_thread.start()
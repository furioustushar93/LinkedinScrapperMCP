"""
Utility functions for the LinkedIn scraper.
"""

import os
import time
import random
from typing import Optional, Dict, Any
from datetime import datetime
from functools import wraps
from loguru import logger
from fake_useragent import UserAgent


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
    """
    logger.remove()  # Remove default handler
    
    # Console logging
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    
    # File logging if specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(
            log_file,
            rotation="10 MB",
            retention="7 days",
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
        )
    
    logger.info(f"Logging initialized at {log_level} level")


def rate_limit(delay: float = 2.0):
    """
    Decorator to add rate limiting to functions.
    
    Args:
        delay: Minimum seconds to wait between calls
    """
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < delay:
                sleep_time = delay - elapsed + random.uniform(0, 0.5)
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator


def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    
    Returns:
        A random user agent string
    """
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        # Fallback to a default user agent
        return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def sanitize_url(url: str) -> str:
    """
    Sanitize and validate LinkedIn URLs.
    
    Args:
        url: The URL to sanitize
        
    Returns:
        Sanitized URL
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    url = url.strip()
    
    # Ensure it's a LinkedIn URL
    if "linkedin.com" not in url:
        raise ValueError("URL must be a LinkedIn URL")
    
    # Add https if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    return url


def extract_linkedin_id(url: str) -> Optional[str]:
    """
    Extract LinkedIn profile ID from URL.
    
    Args:
        url: LinkedIn profile URL
        
    Returns:
        Profile ID or None if not found
    """
    try:
        # Example: https://www.linkedin.com/in/john-doe-123456/
        if "/in/" in url:
            parts = url.split("/in/")
            if len(parts) > 1:
                profile_id = parts[1].strip("/").split("/")[0].split("?")[0]
                return profile_id
        return None
    except Exception as e:
        logger.error(f"Error extracting LinkedIn ID: {e}")
        return None


def parse_experience_duration(duration_text: str) -> Dict[str, Any]:
    """
    Parse experience duration text into structured data.
    
    Args:
        duration_text: Text like "2 yrs 3 mos"
        
    Returns:
        Dictionary with years and months
    """
    result = {"years": 0, "months": 0, "total_months": 0}
    
    try:
        duration_text = duration_text.lower()
        
        # Extract years
        if "yr" in duration_text:
            parts = duration_text.split("yr")
            years = int("".join(filter(str.isdigit, parts[0])))
            result["years"] = years
        
        # Extract months
        if "mo" in duration_text:
            parts = duration_text.split("mo")
            # Get the part before "mo"
            month_part = parts[0].split()[-1] if " " in parts[0] else parts[0]
            months = int("".join(filter(str.isdigit, month_part)))
            result["months"] = months
        
        result["total_months"] = result["years"] * 12 + result["months"]
        
    except Exception as e:
        logger.warning(f"Could not parse duration: {duration_text} - {e}")
    
    return result


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
            
        return wrapper
    return decorator


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    Format a timestamp for logging or display.
    
    Args:
        timestamp: Datetime object, or None for current time
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove common unwanted characters
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    
    return text.strip()


def validate_config(config: Dict[str, Any], required_keys: list) -> bool:
    """
    Validate that all required configuration keys are present.
    
    Args:
        config: Configuration dictionary
        required_keys: List of required key names
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    missing_keys = [key for key in required_keys if key not in config or not config[key]]
    
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
    
    return True


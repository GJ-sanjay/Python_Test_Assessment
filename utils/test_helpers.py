import time
import functools
from typing import Callable, Any
from selenium.common.exceptions import WebDriverException, TimeoutException
from config.config import config


def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a test function on failure
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retry attempts in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (WebDriverException, TimeoutException, AssertionError) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:  # Don't wait on the last attempt
                        print(f"Attempt {attempt + 1} failed: {str(e)}")
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {max_attempts} attempts failed")
            
            # If we get here, all attempts failed
            raise last_exception
        
        return wrapper
    return decorator


def wait_for_condition(condition: Callable[[], bool], timeout: int = 10, poll_frequency: float = 0.5) -> bool:
    """
    Wait for a condition to become true
    
    Args:
        condition: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to check the condition in seconds
    
    Returns:
        True if condition is met within timeout, False otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(poll_frequency)
    
    return False


def take_screenshot_on_failure(test_name: str) -> None:
    """
    Take a screenshot when a test fails
    
    Args:
        test_name: Name of the test for the screenshot filename
    """
    if config.screenshot_on_failure:
        try:
            from utils.driver_manager import DriverManager
            driver = DriverManager.get_driver()
            screenshot_path = f"screenshots/{test_name}_failure.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")


def log_test_step(step_description: str) -> None:
    """
    Log a test step for better readability
    
    Args:
        step_description: Description of the test step
    """
    print(f"[TEST STEP] {step_description}")


def validate_page_load(page_object, timeout: int = 15) -> bool:
    """
    Validate that a page has loaded correctly
    
    Args:
        page_object: Page object instance
        timeout: Maximum time to wait for page load
    
    Returns:
        True if page loaded successfully, False otherwise
    """
    try:
        if hasattr(page_object, 'wait_for_page_to_load'):
            page_object.wait_for_page_to_load(timeout)
            return True
        elif hasattr(page_object, 'is_page_loaded'):
            return wait_for_condition(page_object.is_page_loaded, timeout)
        else:
            # Generic validation - check if page title is not empty
            return len(page_object.get_page_title()) > 0
    except Exception as e:
        print(f"Page load validation failed: {e}")
        return False


def compare_lists_ignore_case(list1: list, list2: list) -> bool:
    """
    Compare two lists ignoring case sensitivity
    
    Args:
        list1: First list to compare
        list2: Second list to compare
    
    Returns:
        True if lists are equal (case-insensitive), False otherwise
    """
    if len(list1) != len(list2):
        return False
    
    normalized_list1 = [item.lower() if isinstance(item, str) else item for item in list1]
    normalized_list2 = [item.lower() if isinstance(item, str) else item for item in list2]
    
    return normalized_list1 == normalized_list2


def find_text_in_list(text: str, text_list: list, case_sensitive: bool = False) -> bool:
    """
    Find if text exists in a list of strings
    
    Args:
        text: Text to search for
        text_list: List of strings to search in
        case_sensitive: Whether to perform case-sensitive search
    
    Returns:
        True if text is found, False otherwise
    """
    if not case_sensitive:
        text = text.lower()
        text_list = [item.lower() if isinstance(item, str) else str(item).lower() for item in text_list]
    
    return any(text in item for item in text_list)


def get_test_data_path(filename: str) -> str:
    """
    Get the path to a test data file
    
    Args:
        filename: Name of the test data file
    
    Returns:
        Full path to the test data file
    """
    import os
    return os.path.join(os.path.dirname(__file__), '..', 'test_data', filename)


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    return ' '.join(text.split()).strip()
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Tuple, Optional, Union
from utils.driver_manager import DriverManager
from config.config import config
import time


class BasePage:
    """Base page class with common functionality for all pages"""
    
    def __init__(self):
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, config.implicit_wait)
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL"""
        self.driver.get(url)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Find a single element"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {locator}")
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find multiple elements"""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def click(self, locator: Tuple[str, str]) -> None:
        """Click on an element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator: Tuple[str, str], text: str) -> None:
        """Enter text into an input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get text content of an element"""
        element = self.find_element(locator)
        return element.text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Get attribute value of an element"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if an element is present on the page"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if an element is visible on the page"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Wait for an element to be present"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_to_be_clickable(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Wait for an element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll to an element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Allow time for scrolling
    
    def get_page_title(self) -> str:
        """Get the current page title"""
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get the current URL"""
        return self.driver.current_url
    
    def refresh_page(self) -> None:
        """Refresh the current page"""
        self.driver.refresh()
    
    def take_screenshot(self, filename: str) -> None:
        """Take a screenshot and save it"""
        self.driver.save_screenshot(filename)
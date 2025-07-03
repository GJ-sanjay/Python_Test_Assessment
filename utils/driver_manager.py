from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from config.config import config
from typing import Optional


class DriverManager:
    """Manages WebDriver instances with proper configuration"""
    
    _instance: Optional[webdriver.Remote] = None
    
    @classmethod
    def get_driver(cls) -> webdriver.Remote:
        """Get or create WebDriver instance"""
        if cls._instance is None:
            cls._instance = cls._create_driver()
        return cls._instance
    
    @classmethod
    def _create_driver(cls) -> webdriver.Remote:
        """Create WebDriver instance based on configuration"""
        browser = config.browser.lower()
        
        if browser == 'chrome':
            return cls._create_chrome_driver()
        elif browser == 'firefox':
            return cls._create_firefox_driver()
        elif browser == 'edge':
            return cls._create_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @classmethod
    def _create_chrome_driver(cls) -> webdriver.Chrome:
        """Create Chrome WebDriver instance"""
        options = ChromeOptions()
        
        if config.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        cls._configure_driver(driver)
        return driver
    
    @classmethod
    def _create_firefox_driver(cls) -> webdriver.Firefox:
        """Create Firefox WebDriver instance"""
        options = FirefoxOptions()
        
        if config.headless:
            options.add_argument('--headless')
        
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        cls._configure_driver(driver)
        return driver
    
    @classmethod
    def _create_edge_driver(cls) -> webdriver.Edge:
        """Create Edge WebDriver instance"""
        options = EdgeOptions()
        
        if config.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        cls._configure_driver(driver)
        return driver
    
    @classmethod
    def _configure_driver(cls, driver: webdriver.Remote) -> None:
        """Configure WebDriver with timeouts and settings"""
        driver.implicitly_wait(config.implicit_wait)
        driver.set_page_load_timeout(config.page_load_timeout)
        driver.maximize_window()
    
    @classmethod
    def quit_driver(cls) -> None:
        """Quit WebDriver instance"""
        if cls._instance:
            cls._instance.quit()
            cls._instance = None
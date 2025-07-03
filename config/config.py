import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class TestConfig:
    """Configuration class for test settings"""
    base_url: str
    api_base_url: str
    browser: str
    headless: bool
    implicit_wait: int
    page_load_timeout: int
    screenshot_on_failure: bool
    
    @classmethod
    def from_env(cls) -> 'TestConfig':
        """Create configuration from environment variables"""
        return cls(
            base_url=os.getenv('BASE_URL', 'http://localhost:3000'),
            api_base_url=os.getenv('API_BASE_URL', 'https://swapi.dev/api'),
            browser=os.getenv('BROWSER', 'chrome'),
            headless=os.getenv('HEADLESS', 'false').lower() == 'true',
            implicit_wait=int(os.getenv('IMPLICIT_WAIT', '10')),
            page_load_timeout=int(os.getenv('PAGE_LOAD_TIMEOUT', '30')),
            screenshot_on_failure=os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
        )


# Global configuration instance
config = TestConfig.from_env()
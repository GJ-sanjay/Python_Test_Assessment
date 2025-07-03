import pytest
import os
from utils.driver_manager import DriverManager
from config.config import config
from api.star_wars_api import StarWarsAPI


@pytest.fixture(scope="session")
def driver():
    """Session-scoped WebDriver fixture"""
    driver = DriverManager.get_driver()
    yield driver
    DriverManager.quit_driver()


@pytest.fixture(scope="session")
def api_client():
    """Session-scoped API client fixture"""
    return StarWarsAPI()


@pytest.fixture(autouse=True)
def setup_test_environment(request):
    """Setup test environment before each test"""
    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)
    
    # Handle test failures
    def fin():
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            if config.screenshot_on_failure:
                try:
                    driver = DriverManager.get_driver()
                    test_name = request.node.name
                    screenshot_path = f"screenshots/{test_name}_failure.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"Failed to take screenshot: {e}")
    
    request.addfinalizer(fin)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def movie_list_page():
    """Fixture for movie list page"""
    from pages.movie_list_page import MovieListPage
    return MovieListPage()


@pytest.fixture
def movie_detail_page():
    """Fixture for movie detail page"""
    from pages.movie_detail_page import MovieDetailPage
    return MovieDetailPage()
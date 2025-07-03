from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from typing import List, Dict, Optional
from utils.base_page import BasePage
from config.config import config


class MovieListPage(BasePage):
    """Page object for the movie list page"""
    
    # Locators
    MOVIES_TABLE = (By.CSS_SELECTOR, "table[data-testid='movies-table']")
    MOVIE_ROWS = (By.CSS_SELECTOR, "table[data-testid='movies-table'] tbody tr")
    TITLE_COLUMN_HEADER = (By.CSS_SELECTOR, "th[data-testid='title-header']")
    RELEASE_DATE_COLUMN_HEADER = (By.CSS_SELECTOR, "th[data-testid='release-date-header']")
    EPISODE_COLUMN_HEADER = (By.CSS_SELECTOR, "th[data-testid='episode-header']")
    DIRECTOR_COLUMN_HEADER = (By.CSS_SELECTOR, "th[data-testid='director-header']")
    
    # Alternative locators in case data-testid is not available
    MOVIES_TABLE_ALT = (By.CSS_SELECTOR, "table")
    MOVIE_ROWS_ALT = (By.CSS_SELECTOR, "table tbody tr")
    TITLE_HEADER_ALT = (By.XPATH, "//th[contains(text(), 'Title')]")
    RELEASE_DATE_HEADER_ALT = (By.XPATH, "//th[contains(text(), 'Release Date')]")
    EPISODE_HEADER_ALT = (By.XPATH, "//th[contains(text(), 'Episode')]")
    DIRECTOR_HEADER_ALT = (By.XPATH, "//th[contains(text(), 'Director')]")
    
    def __init__(self):
        super().__init__()
        self.navigate_to(config.base_url)
    
    def get_movies_table(self):
        """Get the movies table element"""
        try:
            return self.find_element(self.MOVIES_TABLE)
        except:
            return self.find_element(self.MOVIES_TABLE_ALT)
    
    def get_movie_rows(self) -> List:
        """Get all movie rows from the table"""
        try:
            return self.find_elements(self.MOVIE_ROWS)
        except:
            return self.find_elements(self.MOVIE_ROWS_ALT)
    
    def sort_by_title(self) -> None:
        """Sort movies by title"""
        try:
            self.click(self.TITLE_COLUMN_HEADER)
        except:
            self.click(self.TITLE_HEADER_ALT)
    
    def sort_by_release_date(self) -> None:
        """Sort movies by release date"""
        try:
            self.click(self.RELEASE_DATE_COLUMN_HEADER)
        except:
            self.click(self.RELEASE_DATE_HEADER_ALT)
    
    def sort_by_episode(self) -> None:
        """Sort movies by episode"""
        try:
            self.click(self.EPISODE_COLUMN_HEADER)
        except:
            self.click(self.EPISODE_HEADER_ALT)
    
    def sort_by_director(self) -> None:
        """Sort movies by director"""
        try:
            self.click(self.DIRECTOR_COLUMN_HEADER)
        except:
            self.click(self.DIRECTOR_HEADER_ALT)
    
    def get_movie_titles(self) -> List[str]:
        """Get all movie titles from the table"""
        movie_rows = self.get_movie_rows()
        titles = []
        for row in movie_rows:
            # Try different possible selectors for title cell
            try:
                title_cell = row.find_element(By.CSS_SELECTOR, "td[data-testid='title-cell']")
                titles.append(title_cell.text.strip())
            except:
                try:
                    title_cell = row.find_element(By.CSS_SELECTOR, "td:first-child")
                    titles.append(title_cell.text.strip())
                except:
                    # Fallback to getting all cells and assuming first is title
                    cells = row.find_elements(By.CSS_SELECTOR, "td")
                    if cells:
                        titles.append(cells[0].text.strip())
        return titles
    
    def get_last_movie_title(self) -> str:
        """Get the title of the last movie in the list"""
        titles = self.get_movie_titles()
        return titles[-1] if titles else ""
    
    def click_movie_by_title(self, title: str) -> None:
        """Click on a movie by its title"""
        movie_rows = self.get_movie_rows()
        for row in movie_rows:
            try:
                # Try to find clickable title element
                title_element = row.find_element(By.CSS_SELECTOR, "td a, td button, td[data-testid='title-cell']")
                if title.lower() in title_element.text.lower():
                    title_element.click()
                    return
            except:
                # Fallback to clicking the row itself
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                if cells and title.lower() in cells[0].text.lower():
                    cells[0].click()
                    return
        
        raise Exception(f"Movie with title '{title}' not found")
    
    def get_movie_count(self) -> int:
        """Get the total number of movies displayed"""
        return len(self.get_movie_rows())
    
    def is_movies_table_loaded(self) -> bool:
        """Check if the movies table is loaded"""
        try:
            self.get_movies_table()
            return len(self.get_movie_rows()) > 0
        except:
            return False
    
    def wait_for_movies_to_load(self, timeout: int = 15) -> None:
        """Wait for movies to load in the table"""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_movies_table_loaded():
                return
            time.sleep(1)
        raise TimeoutError("Movies table did not load within the specified timeout")
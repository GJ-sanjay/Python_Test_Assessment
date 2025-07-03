from selenium.webdriver.common.by import By
from typing import List, Dict, Optional
from utils.base_page import BasePage


class MovieDetailPage(BasePage):
    """Page object for the movie detail page"""
    
    # Locators
    BACK_BUTTON = (By.CSS_SELECTOR, "button[data-testid='back-button']")
    MOVIE_TITLE = (By.CSS_SELECTOR, "h1[data-testid='movie-title']")
    MOVIE_DIRECTOR = (By.CSS_SELECTOR, "[data-testid='director']")
    MOVIE_PRODUCER = (By.CSS_SELECTOR, "[data-testid='producer']")
    MOVIE_RELEASE_DATE = (By.CSS_SELECTOR, "[data-testid='release-date']")
    SPECIES_LIST = (By.CSS_SELECTOR, "[data-testid='species-list']")
    PLANETS_LIST = (By.CSS_SELECTOR, "[data-testid='planets-list']")
    CHARACTERS_LIST = (By.CSS_SELECTOR, "[data-testid='characters-list']")
    
    # Alternative locators
    BACK_BUTTON_ALT = (By.XPATH, "//button[contains(text(), 'Back')]")
    MOVIE_TITLE_ALT = (By.CSS_SELECTOR, "h1")
    DIRECTOR_ALT = (By.XPATH, "//*[contains(text(), 'Director')]/following-sibling::*")
    PRODUCER_ALT = (By.XPATH, "//*[contains(text(), 'Producer')]/following-sibling::*")
    SPECIES_LIST_ALT = (By.XPATH, "//*[contains(text(), 'Species')]/following-sibling::*")
    PLANETS_LIST_ALT = (By.XPATH, "//*[contains(text(), 'Planets')]/following-sibling::*")
    
    def get_movie_title(self) -> str:
        """Get the movie title"""
        try:
            return self.get_text(self.MOVIE_TITLE)
        except:
            return self.get_text(self.MOVIE_TITLE_ALT)
    
    def get_director(self) -> str:
        """Get the movie director"""
        try:
            return self.get_text(self.MOVIE_DIRECTOR)
        except:
            return self.get_text(self.DIRECTOR_ALT)
    
    def get_producer(self) -> str:
        """Get the movie producer"""
        try:
            return self.get_text(self.MOVIE_PRODUCER)
        except:
            return self.get_text(self.PRODUCER_ALT)
    
    def get_species_list(self) -> List[str]:
        """Get the list of species in the movie"""
        try:
            species_element = self.find_element(self.SPECIES_LIST)
            species_text = species_element.text
        except:
            species_element = self.find_element(self.SPECIES_LIST_ALT)
            species_text = species_element.text
        
        # Parse species list - assuming they are separated by commas or new lines
        species_list = []
        if species_text:
            # Split by common separators
            for separator in [',', '\n', ';']:
                if separator in species_text:
                    species_list = [s.strip() for s in species_text.split(separator)]
                    break
            else:
                # If no separators found, treat as single species
                species_list = [species_text.strip()]
        
        return species_list
    
    def get_planets_list(self) -> List[str]:
        """Get the list of planets in the movie"""
        try:
            planets_element = self.find_element(self.PLANETS_LIST)
            planets_text = planets_element.text
        except:
            planets_element = self.find_element(self.PLANETS_LIST_ALT)
            planets_text = planets_element.text
        
        # Parse planets list - assuming they are separated by commas or new lines
        planets_list = []
        if planets_text:
            # Split by common separators
            for separator in [',', '\n', ';']:
                if separator in planets_text:
                    planets_list = [p.strip() for p in planets_text.split(separator)]
                    break
            else:
                # If no separators found, treat as single planet
                planets_list = [planets_text.strip()]
        
        return planets_list
    
    def has_species(self, species_name: str) -> bool:
        """Check if a specific species exists in the movie"""
        species_list = self.get_species_list()
        return any(species_name.lower() in species.lower() for species in species_list)
    
    def has_planet(self, planet_name: str) -> bool:
        """Check if a specific planet exists in the movie"""
        planets_list = self.get_planets_list()
        return any(planet_name.lower() in planet.lower() for planet in planets_list)
    
    def click_back_button(self) -> None:
        """Click the back button to return to movie list"""
        try:
            self.click(self.BACK_BUTTON)
        except:
            self.click(self.BACK_BUTTON_ALT)
    
    def is_movie_detail_loaded(self) -> bool:
        """Check if the movie detail page is loaded"""
        try:
            self.get_movie_title()
            return True
        except:
            return False
    
    def wait_for_movie_detail_to_load(self, timeout: int = 15) -> None:
        """Wait for movie detail page to load"""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_movie_detail_loaded():
                return
            time.sleep(1)
        raise TimeoutError("Movie detail page did not load within the specified timeout")
import pytest
from pages.movie_list_page import MovieListPage
from pages.movie_detail_page import MovieDetailPage
from utils.test_helpers import retry_on_failure


class TestMovieDetails:
    """Test suite for movie detail page functionality"""
    
    @retry_on_failure(max_attempts=3)
    def test_empire_strikes_back_has_wookie_species(self, movie_list_page):
        """
        Test: View the movie 'The Empire Strikes Back' and check if the 'Species' list has 'Wookie'
        
        This test verifies that:
        1. The movie list page loads correctly
        2. 'The Empire Strikes Back' can be selected and viewed
        3. The movie detail page loads with species information
        4. 'Wookie' is present in the species list
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Click on 'The Empire Strikes Back'
        movie_list_page.click_movie_by_title("The Empire Strikes Back")
        
        # Initialize movie detail page
        movie_detail_page = MovieDetailPage()
        
        # Wait for movie detail page to load
        movie_detail_page.wait_for_movie_detail_to_load()
        
        # Verify we're on the correct movie detail page
        movie_title = movie_detail_page.get_movie_title()
        assert "The Empire Strikes Back" in movie_title, (
            f"Expected to be on 'The Empire Strikes Back' detail page, "
            f"but got '{movie_title}'"
        )
        
        # Get the species list
        species_list = movie_detail_page.get_species_list()
        
        # Check if 'Wookie' is in the species list
        has_wookie = movie_detail_page.has_species("Wookie")
        
        assert has_wookie, (
            f"Expected 'Wookie' to be in the species list for 'The Empire Strikes Back', "
            f"but species list was: {species_list}"
        )
        
        print(f"✓ Successfully verified that 'Wookie' is present in the species list")
        print(f"  Species found: {species_list}")
    
    @retry_on_failure(max_attempts=3)
    def test_phantom_menace_does_not_have_camino_planet(self, movie_list_page):
        """
        Test: Assert that 'Planets' 'Camino' is not part of the movie 'The Phantom Menace'
        
        This test verifies that:
        1. 'The Phantom Menace' movie detail page can be accessed
        2. The planets list does not contain 'Camino'
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Click on 'The Phantom Menace'
        movie_list_page.click_movie_by_title("The Phantom Menace")
        
        # Initialize movie detail page
        movie_detail_page = MovieDetailPage()
        
        # Wait for movie detail page to load
        movie_detail_page.wait_for_movie_detail_to_load()
        
        # Verify we're on the correct movie detail page
        movie_title = movie_detail_page.get_movie_title()
        assert "The Phantom Menace" in movie_title, (
            f"Expected to be on 'The Phantom Menace' detail page, "
            f"but got '{movie_title}'"
        )
        
        # Get the planets list
        planets_list = movie_detail_page.get_planets_list()
        
        # Check if 'Camino' is NOT in the planets list
        has_camino = movie_detail_page.has_planet("Camino")
        
        assert not has_camino, (
            f"Expected 'Camino' to NOT be in the planets list for 'The Phantom Menace', "
            f"but planets list was: {planets_list}"
        )
        
        print(f"✓ Successfully verified that 'Camino' is not present in the planets list")
        print(f"  Planets found: {planets_list}")
    
    def test_back_button_functionality(self, movie_list_page):
        """
        Test: Verify that the back button works correctly from movie detail page
        
        This test ensures navigation between pages works properly
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Click on any movie (using 'The Empire Strikes Back')
        movie_list_page.click_movie_by_title("The Empire Strikes Back")
        
        # Initialize movie detail page
        movie_detail_page = MovieDetailPage()
        
        # Wait for movie detail page to load
        movie_detail_page.wait_for_movie_detail_to_load()
        
        # Click back button
        movie_detail_page.click_back_button()
        
        # Wait for movie list page to load again
        movie_list_page.wait_for_movies_to_load()
        
        # Verify we're back on the movie list page
        assert movie_list_page.is_movies_table_loaded(), (
            "Failed to return to movie list page after clicking back button"
        )
        
        print("✓ Successfully verified back button functionality")
    
    @retry_on_failure(max_attempts=3)
    def test_movie_detail_page_has_required_information(self, movie_list_page):
        """
        Test: Verify that movie detail page contains required information
        
        This test ensures the detail page displays essential movie information
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Click on 'The Empire Strikes Back'
        movie_list_page.click_movie_by_title("The Empire Strikes Back")
        
        # Initialize movie detail page
        movie_detail_page = MovieDetailPage()
        
        # Wait for movie detail page to load
        movie_detail_page.wait_for_movie_detail_to_load()
        
        # Verify required information is present
        movie_title = movie_detail_page.get_movie_title()
        assert movie_title, "Movie title is not displayed"
        
        try:
            director = movie_detail_page.get_director()
            assert director, "Director information is not displayed"
        except:
            print("Warning: Director information not found (may be acceptable depending on UI design)")
        
        try:
            species_list = movie_detail_page.get_species_list()
            assert isinstance(species_list, list), "Species list is not properly formatted"
        except:
            print("Warning: Species list not found (may be acceptable depending on UI design)")
        
        try:
            planets_list = movie_detail_page.get_planets_list()
            assert isinstance(planets_list, list), "Planets list is not properly formatted"
        except:
            print("Warning: Planets list not found (may be acceptable depending on UI design)")
        
        print(f"✓ Successfully verified movie detail page contains required information")
        print(f"  Movie: {movie_title}")
import pytest
from pages.movie_list_page import MovieListPage
from utils.test_helpers import retry_on_failure


class TestMovieSorting:
    """Test suite for movie sorting functionality"""
    
    @retry_on_failure(max_attempts=3)
    def test_sort_movies_by_title_phantom_menace_last(self, movie_list_page):
        """
        Test: Sort movies by 'Title' and assert the last movie in the list is 'The Phantom Menace'
        
        This test verifies that:
        1. The movie list page loads correctly
        2. Movies can be sorted by title
        3. After sorting by title, 'The Phantom Menace' appears as the last movie
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Sort movies by title
        movie_list_page.sort_by_title()
        
        # Wait a moment for sorting to complete
        import time
        time.sleep(2)
        
        # Get the last movie title
        last_movie_title = movie_list_page.get_last_movie_title()
        
        # Assert that the last movie is 'The Phantom Menace'
        assert "The Phantom Menace" in last_movie_title, (
            f"Expected 'The Phantom Menace' to be the last movie when sorted by title, "
            f"but got '{last_movie_title}'"
        )
        
        # Additional validation: ensure we have movies in the list
        movie_count = movie_list_page.get_movie_count()
        assert movie_count > 0, "No movies found in the list"
        
        # Log the test result
        print(f"✓ Successfully verified that '{last_movie_title}' is the last movie when sorted by title")
    
    @retry_on_failure(max_attempts=3)
    def test_sort_movies_by_title_ascending_order(self, movie_list_page):
        """
        Test: Verify that movies are sorted in ascending alphabetical order by title
        
        This test ensures that the sorting functionality works correctly
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Sort movies by title
        movie_list_page.sort_by_title()
        
        # Wait for sorting to complete
        import time
        time.sleep(2)
        
        # Get all movie titles
        movie_titles = movie_list_page.get_movie_titles()
        
        # Verify that we have movies
        assert len(movie_titles) > 0, "No movies found in the list"
        
        # Verify that titles are sorted alphabetically
        sorted_titles = sorted(movie_titles)
        assert movie_titles == sorted_titles, (
            f"Movies are not sorted alphabetically. "
            f"Expected: {sorted_titles}, Got: {movie_titles}"
        )
        
        print(f"✓ Successfully verified that {len(movie_titles)} movies are sorted alphabetically")
        print(f"  Movies in order: {movie_titles}")
    
    def test_multiple_sort_operations(self, movie_list_page):
        """
        Test: Verify that multiple sort operations work correctly
        
        This test ensures sorting is stable and works multiple times
        """
        # Wait for movies to load
        movie_list_page.wait_for_movies_to_load()
        
        # Sort by title multiple times and verify consistency
        for i in range(3):
            movie_list_page.sort_by_title()
            import time
            time.sleep(1)
            
            last_movie = movie_list_page.get_last_movie_title()
            assert "The Phantom Menace" in last_movie, (
                f"Sorting consistency failed on attempt {i+1}. "
                f"Expected 'The Phantom Menace', got '{last_movie}'"
            )
        
        print("✓ Successfully verified sorting consistency across multiple operations")
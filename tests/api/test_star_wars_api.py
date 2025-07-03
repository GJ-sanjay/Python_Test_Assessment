import pytest
from api.star_wars_api import StarWarsAPI
from utils.test_helpers import retry_on_failure


class TestStarWarsAPI:
    """Test suite for Star Wars API functionality"""
    
    @retry_on_failure(max_attempts=3)
    def test_get_movies_count_is_six(self, api_client):
        """
        Test: Get the list of movies and check if the movies count is 6
        
        This test verifies that:
        1. The API responds correctly
        2. The total count of movies is 6
        """
        # Get the movies count
        movies_count = api_client.get_films_count()
        
        # Assert that the count is 6
        assert movies_count == 6, (
            f"Expected 6 movies in the Star Wars API, but got {movies_count}"
        )
        
        # Additional verification: get the actual list and verify count
        movies_list = api_client.get_films_list()
        assert len(movies_list) == 6, (
            f"Expected 6 movies in the results list, but got {len(movies_list)}"
        )
        
        print(f"✓ Successfully verified that the API returns {movies_count} movies")
        
        # Log movie titles for reference
        for i, movie in enumerate(movies_list, 1):
            print(f"  {i}. {movie.get('title', 'Unknown Title')}")
    
    @retry_on_failure(max_attempts=3)
    def test_third_movie_director_is_richard_marquand(self, api_client):
        """
        Test: Get the 3rd movie and check if the director of the movie is 'Richard Marquand'
        
        This test verifies that:
        1. The 3rd movie can be retrieved (when sorted by episode)
        2. The director of the 3rd movie is 'Richard Marquand'
        """
        # Get the 3rd movie (when sorted by episode ID)
        third_movie = api_client.get_nth_film_by_episode(3)
        
        assert third_movie is not None, "Could not retrieve the 3rd movie"
        
        # Get the director
        director = third_movie.get('director', '')
        
        # Assert that the director is 'Richard Marquand'
        assert director == 'Richard Marquand', (
            f"Expected director of the 3rd movie to be 'Richard Marquand', "
            f"but got '{director}'"
        )
        
        print(f"✓ Successfully verified that the 3rd movie director is 'Richard Marquand'")
        print(f"  Movie: {third_movie.get('title', 'Unknown Title')}")
        print(f"  Director: {director}")
    
    @retry_on_failure(max_attempts=3)
    def test_fifth_movie_producers_are_not_gary_kurtz_george_lucas(self, api_client):
        """
        Test: Get the 5th movie and assert that 'Producers' are not 'Gary Kurtz, George Lucas'
        
        This test verifies that:
        1. The 5th movie can be retrieved (when sorted by episode)
        2. The producers of the 5th movie are NOT 'Gary Kurtz, George Lucas'
        """
        # Get the 5th movie (when sorted by episode ID)
        fifth_movie = api_client.get_nth_film_by_episode(5)
        
        assert fifth_movie is not None, "Could not retrieve the 5th movie"
        
        # Get the producer
        producer = fifth_movie.get('producer', '')
        
        # Assert that the producer is NOT 'Gary Kurtz, George Lucas'
        assert producer != 'Gary Kurtz, George Lucas', (
            f"Expected producer of the 5th movie to NOT be 'Gary Kurtz, George Lucas', "
            f"but got '{producer}'"
        )
        
        print(f"✓ Successfully verified that the 5th movie producer is not 'Gary Kurtz, George Lucas'")
        print(f"  Movie: {fifth_movie.get('title', 'Unknown Title')}")
        print(f"  Producer: {producer}")
    
    def test_api_response_structure(self, api_client):
        """
        Test: Verify that API responses have the expected structure
        
        This test ensures the API returns properly formatted data
        """
        # Get all films
        films_response = api_client.get_films()
        
        # Verify response structure
        assert 'results' in films_response, "API response missing 'results' field"
        assert 'count' in films_response, "API response missing 'count' field"
        
        # Verify each film has required fields
        films = films_response['results']
        required_fields = ['title', 'episode_id', 'director', 'producer', 'release_date']
        
        for film in films:
            for field in required_fields:
                assert field in film, f"Film missing required field: {field}"
            
            # Validate that the film response is properly structured
            assert api_client.validate_api_response(film), (
                f"Film {film.get('title', 'Unknown')} has invalid response structure"
            )
        
        print(f"✓ Successfully verified API response structure for {len(films)} films")
    
    def test_get_films_by_episode_order(self, api_client):
        """
        Test: Verify that films can be retrieved in episode order
        
        This test ensures the episode ordering functionality works correctly
        """
        # Get films sorted by episode
        sorted_films = api_client.get_sorted_films_by_episode()
        
        # Verify we have 6 films
        assert len(sorted_films) == 6, f"Expected 6 films, got {len(sorted_films)}"
        
        # Verify they are sorted by episode ID
        episode_ids = [film.get('episode_id') for film in sorted_films]
        assert episode_ids == sorted(episode_ids), (
            f"Films are not sorted by episode ID. Got: {episode_ids}"
        )
        
        print(f"✓ Successfully verified films are sorted by episode ID")
        print(f"  Episode order: {episode_ids}")
        
        # Log films in episode order
        for i, film in enumerate(sorted_films, 1):
            print(f"  {i}. Episode {film.get('episode_id')}: {film.get('title')}")
    
    def test_individual_film_retrieval(self, api_client):
        """
        Test: Verify that individual films can be retrieved by ID
        
        This test ensures single film retrieval works correctly
        """
        # Test retrieving films by ID (1-6)
        for film_id in range(1, 7):
            try:
                film = api_client.get_film_by_id(film_id)
                assert film is not None, f"Could not retrieve film with ID {film_id}"
                assert 'title' in film, f"Film {film_id} missing title"
                assert 'episode_id' in film, f"Film {film_id} missing episode_id"
                
                print(f"  ✓ Film {film_id}: {film.get('title')}")
            except Exception as e:
                print(f"  ✗ Failed to retrieve film {film_id}: {e}")
                raise
        
        print("✓ Successfully verified individual film retrieval for all 6 films")
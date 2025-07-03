import requests
from typing import Dict, List, Optional, Any
from config.config import config


class StarWarsAPI:
    """API client for Star Wars API interactions"""
    
    def __init__(self):
        self.base_url = config.api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'StarWarsTestAutomation/1.0',
            'Accept': 'application/json'
        })
    
    def get_films(self) -> Dict[str, Any]:
        """Get all Star Wars films"""
        url = f"{self.base_url}/films/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_film_by_id(self, film_id: int) -> Dict[str, Any]:
        """Get a specific film by ID"""
        url = f"{self.base_url}/films/{film_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_films_list(self) -> List[Dict[str, Any]]:
        """Get list of all films"""
        films_data = self.get_films()
        return films_data.get('results', [])
    
    def get_films_count(self) -> int:
        """Get the total count of films"""
        films_data = self.get_films()
        return films_data.get('count', 0)
    
    def get_film_by_episode_id(self, episode_id: int) -> Optional[Dict[str, Any]]:
        """Get film by episode ID"""
        films = self.get_films_list()
        for film in films:
            if film.get('episode_id') == episode_id:
                return film
        return None
    
    def get_film_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get film by title"""
        films = self.get_films_list()
        for film in films:
            if title.lower() in film.get('title', '').lower():
                return film
        return None
    
    def get_film_director(self, film_id: int) -> str:
        """Get director of a specific film"""
        film = self.get_film_by_id(film_id)
        return film.get('director', '')
    
    def get_film_producer(self, film_id: int) -> str:
        """Get producer of a specific film"""
        film = self.get_film_by_id(film_id)
        return film.get('producer', '')
    
    def get_sorted_films_by_episode(self) -> List[Dict[str, Any]]:
        """Get films sorted by episode ID"""
        films = self.get_films_list()
        return sorted(films, key=lambda x: x.get('episode_id', 0))
    
    def get_nth_film_by_episode(self, n: int) -> Optional[Dict[str, Any]]:
        """Get the nth film when sorted by episode ID (1-indexed)"""
        sorted_films = self.get_sorted_films_by_episode()
        if 1 <= n <= len(sorted_films):
            return sorted_films[n - 1]
        return None
    
    def validate_api_response(self, response_data: Dict[str, Any]) -> bool:
        """Validate API response structure"""
        required_fields = ['title', 'episode_id', 'director', 'producer', 'release_date']
        return all(field in response_data for field in required_fields)
    
    def get_film_details_summary(self, film_id: int) -> Dict[str, Any]:
        """Get a summary of film details"""
        film = self.get_film_by_id(film_id)
        return {
            'title': film.get('title', ''),
            'episode_id': film.get('episode_id', 0),
            'director': film.get('director', ''),
            'producer': film.get('producer', ''),
            'release_date': film.get('release_date', ''),
            'opening_crawl': film.get('opening_crawl', ''),
            'characters_count': len(film.get('characters', [])),
            'planets_count': len(film.get('planets', [])),
            'species_count': len(film.get('species', []))
        }
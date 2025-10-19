"""
Unit tests for the LinkedIn scraper.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import LinkedInScraper
from src.utils import (
    sanitize_url,
    extract_linkedin_id,
    clean_text,
    parse_experience_duration,
)


class TestUtils:
    """Test utility functions."""
    
    def test_sanitize_url_valid(self):
        """Test URL sanitization with valid LinkedIn URLs."""
        url = "linkedin.com/in/johndoe"
        result = sanitize_url(url)
        assert result.startswith("https://")
        assert "linkedin.com" in result
    
    def test_sanitize_url_invalid(self):
        """Test URL sanitization with invalid URLs."""
        with pytest.raises(ValueError):
            sanitize_url("https://example.com")
    
    def test_extract_linkedin_id(self):
        """Test LinkedIn ID extraction."""
        url = "https://www.linkedin.com/in/john-doe-123456/"
        profile_id = extract_linkedin_id(url)
        assert profile_id == "john-doe-123456"
    
    def test_extract_linkedin_id_with_params(self):
        """Test ID extraction with query parameters."""
        url = "https://www.linkedin.com/in/john-doe-123456?trk=profile"
        profile_id = extract_linkedin_id(url)
        assert profile_id == "john-doe-123456"
    
    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "  Hello   \n  World  \t  "
        clean = clean_text(dirty_text)
        assert clean == "Hello World"
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        assert clean_text("") == ""
        assert clean_text(None) == ""
    
    def test_parse_experience_duration(self):
        """Test experience duration parsing."""
        result = parse_experience_duration("2 yrs 3 mos")
        assert result["years"] == 2
        assert result["months"] == 3
        assert result["total_months"] == 27


class TestLinkedInScraper:
    """Test LinkedInScraper class."""
    
    @patch('src.scraper.Linkedin')
    def test_init_with_credentials(self, mock_linkedin):
        """Test scraper initialization with credentials."""
        scraper = LinkedInScraper(email="test@example.com", password="password123")
        assert scraper.email == "test@example.com"
        assert scraper.password == "password123"
        assert scraper.session is not None
    
    def test_init_without_credentials(self):
        """Test scraper initialization without credentials."""
        scraper = LinkedInScraper()
        assert scraper.session is not None
    
    @patch('src.scraper.Linkedin')
    def test_scrape_profile_api_success(self, mock_linkedin):
        """Test profile scraping using API."""
        # Mock API client
        mock_api = MagicMock()
        mock_api.get_profile.return_value = {
            "public_id": "john-doe",
            "firstName": "John",
            "lastName": "Doe",
            "headline": "Software Engineer",
        }
        
        scraper = LinkedInScraper(email="test@example.com", password="password123")
        scraper.api_client = mock_api
        
        result = scraper.scrape_profile("https://linkedin.com/in/john-doe")
        
        assert result["profile_id"] == "john-doe"
        assert result["first_name"] == "John"
        assert result["last_name"] == "Doe"
        assert result["method"] == "linkedin_api"
    
    @patch('src.scraper.Linkedin')
    def test_search_jobs(self, mock_linkedin):
        """Test job search."""
        mock_api = MagicMock()
        mock_api.search_jobs.return_value = [
            {
                "entityUrn": "urn:li:job:123456",
                "title": "Python Developer",
                "companyName": "Tech Corp",
                "location": "San Francisco, CA",
            }
        ]
        
        scraper = LinkedInScraper(email="test@example.com", password="password123")
        scraper.api_client = mock_api
        
        results = scraper.search_jobs(keywords="Python", limit=10)
        
        assert len(results) > 0
        assert results[0]["title"] == "Python Developer"
        assert results[0]["company"] == "Tech Corp"
    
    @patch('src.scraper.Linkedin')
    def test_get_company_info(self, mock_linkedin):
        """Test getting company information."""
        mock_api = MagicMock()
        mock_api.get_company.return_value = {
            "universalName": "google",
            "name": "Google",
            "description": "Search engine company",
            "staffCount": 100000,
        }
        
        scraper = LinkedInScraper(email="test@example.com", password="password123")
        scraper.api_client = mock_api
        
        result = scraper.get_company_info("google")
        
        assert result["company_id"] == "google"
        assert result["name"] == "Google"
        assert result["company_size"] == 100000
    
    @patch('src.scraper.Linkedin')
    def test_search_people(self, mock_linkedin):
        """Test people search."""
        mock_api = MagicMock()
        mock_api.search_people.return_value = [
            {
                "public_id": "jane-smith",
                "firstName": "Jane",
                "lastName": "Smith",
                "headline": "Data Scientist",
            }
        ]
        
        scraper = LinkedInScraper(email="test@example.com", password="password123")
        scraper.api_client = mock_api
        
        results = scraper.search_people(keywords="Data Scientist", limit=10)
        
        assert len(results) > 0
        assert results[0]["name"] == "Jane Smith"
        assert results[0]["headline"] == "Data Scientist"


@pytest.fixture
def scraper():
    """Fixture to create a scraper instance."""
    return LinkedInScraper()


def test_session_headers(scraper):
    """Test that session has proper headers."""
    assert "User-Agent" in scraper.session.headers
    assert "Accept-Language" in scraper.session.headers


def test_close(scraper):
    """Test closing the scraper."""
    scraper.close()
    # Should not raise any exceptions


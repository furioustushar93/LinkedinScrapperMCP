"""
LinkedIn scraper implementation.
"""

import os
import sys
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# Add backend directory to path
_backend_dir = Path(__file__).parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

import requests
from bs4 import BeautifulSoup
from loguru import logger

from linkedin_api import Linkedin

# Import utils from backend directory
from utils import (
    rate_limit,
    get_random_user_agent,
    sanitize_url,
    extract_linkedin_id,
    clean_text,
    retry_on_failure,
)


class LinkedInScraper:
    """
    A scraper for extracting data from LinkedIn.
    """
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the LinkedIn scraper.
        
        Args:
            email: LinkedIn account email
            password: LinkedIn account password
        """
        self.email = email or os.getenv("LINKEDIN_EMAIL")
        self.password = password or os.getenv("LINKEDIN_PASSWORD")
        self.session = requests.Session()
        self.api_client = None
        
        # Set up session headers
        self.session.headers.update({
            "User-Agent": get_random_user_agent(),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        })
        
        # Initialize API client if credentials are provided
        if self.email and self.password:
            try:
                logger.info("Initializing LinkedIn API client...")
                self.api_client = Linkedin(self.email, self.password)
                logger.success("LinkedIn API client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize LinkedIn API client: {e}")
                logger.info("Will fallback to web scraping methods")
    
    @rate_limit(delay=2.0)
    @retry_on_failure(max_retries=3)
    def scrape_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Scrape a LinkedIn profile.
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Dictionary containing profile information
        """
        logger.info(f"Scraping profile: {profile_url}")
        
        try:
            profile_url = sanitize_url(profile_url)
            profile_id = extract_linkedin_id(profile_url)
            
            if not profile_id:
                raise ValueError("Could not extract profile ID from URL")
            
            # Try using API client first
            if self.api_client:
                try:
                    logger.debug("Using LinkedIn API client")
                    profile_data = self.api_client.get_profile(profile_id)
                    return self._format_profile_data(profile_data, profile_url)
                except Exception as e:
                    logger.warning(f"API client failed: {e}. Falling back to web scraping.")
            
            # Fallback to web scraping
            return self._scrape_profile_web(profile_url)
            
        except Exception as e:
            logger.error(f"Error scraping profile {profile_url}: {e}")
            raise
    
    def _scrape_profile_web(self, profile_url: str) -> Dict[str, Any]:
        """
        Scrape profile using web scraping (fallback method).
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Profile data dictionary
        """
        logger.debug(f"Web scraping profile: {profile_url}")
        
        response = self.session.get(profile_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # Extract basic information
        profile_data = {
            "url": profile_url,
            "profile_id": extract_linkedin_id(profile_url),
            "scraped_at": datetime.now().isoformat(),
            "method": "web_scraping",
        }
        
        # Note: LinkedIn's structure changes frequently
        # This is a basic example that may need updates
        
        # Try to extract name
        name_elem = soup.find("h1", class_="text-heading-xlarge")
        if name_elem:
            profile_data["name"] = clean_text(name_elem.get_text())
        
        # Try to extract headline
        headline_elem = soup.find("div", class_="text-body-medium")
        if headline_elem:
            profile_data["headline"] = clean_text(headline_elem.get_text())
        
        logger.info(f"Successfully scraped profile (web method): {profile_data.get('name', 'Unknown')}")
        
        return profile_data
    
    def _format_profile_data(self, api_data: Dict, profile_url: str) -> Dict[str, Any]:
        """
        Format profile data from API response.
        
        Args:
            api_data: Raw API response
            profile_url: Profile URL
            
        Returns:
            Formatted profile data
        """
        formatted = {
            "url": profile_url,
            "profile_id": api_data.get("public_id"),
            "first_name": api_data.get("firstName"),
            "last_name": api_data.get("lastName"),
            "headline": api_data.get("headline"),
            "summary": api_data.get("summary"),
            "location": api_data.get("geoLocationName"),
            "industry": api_data.get("industryName"),
            "connections": api_data.get("connections"),
            "follower_count": api_data.get("followerCount"),
            "scraped_at": datetime.now().isoformat(),
            "method": "linkedin_api",
        }
        
        # Clean up None values
        formatted = {k: v for k, v in formatted.items() if v is not None}
        
        logger.success(f"Successfully scraped profile (API): {formatted.get('first_name', '')} {formatted.get('last_name', '')}")
        
        return formatted
    
    @rate_limit(delay=2.0)
    @retry_on_failure(max_retries=3)
    def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            keywords: Search keywords
            location: Job location
            job_type: Job type (full-time, part-time, contract, etc.)
            experience_level: Experience level (entry, mid, senior, etc.)
            limit: Maximum number of results
            
        Returns:
            List of job dictionaries
        """
        logger.info(f"Searching jobs: keywords='{keywords}', location='{location}'")
        
        try:
            if self.api_client:
                logger.debug("Using LinkedIn API client for job search")
                jobs = self.api_client.search_jobs(
                    keywords=keywords,
                    location_name=location,
                    limit=limit
                )
                return [self._format_job_data(job) for job in jobs]
            else:
                logger.warning("API client not available. Job search requires authentication.")
                return []
                
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            raise
    
    def _format_job_data(self, job_data: Dict) -> Dict[str, Any]:
        """
        Format job data from API response.
        
        Args:
            job_data: Raw job data
            
        Returns:
            Formatted job dictionary
        """
        # Extract company name from various possible fields
        company_name = (
            job_data.get("companyName") or
            job_data.get("company", {}).get("name") if isinstance(job_data.get("company"), dict) else job_data.get("company") or
            job_data.get("companyDetails", {}).get("name") if isinstance(job_data.get("companyDetails"), dict) else None or
            "Company Information Available"
        )
        
        # Extract job ID
        entity_urn = job_data.get("entityUrn", "")
        job_id = entity_urn.split(":")[-1] if entity_urn else job_data.get("dashEntityUrn", "").split(":")[-1]
        
        # Format posted time
        posted_time = job_data.get("listedAt") or job_data.get("originalListedAt")
        if posted_time and isinstance(posted_time, (int, float)):
            from datetime import datetime as dt
            posted_date = dt.fromtimestamp(posted_time / 1000).strftime("%Y-%m-%d")
        else:
            posted_date = posted_time or "Recently"
        
        return {
            "job_id": job_id,
            "title": job_data.get("title", "Position Title"),
            "company": company_name,
            "companyName": company_name,  # Include both keys for compatibility
            "location": job_data.get("location", job_data.get("formattedLocation", "Location TBD")),
            "description": clean_text(job_data.get("description", "")),
            "posted_at": posted_date,
            "job_url": f"https://www.linkedin.com/jobs/view/{job_id}/" if job_id else "https://www.linkedin.com/jobs/",
            "scraped_at": datetime.now().isoformat(),
        }
    
    @rate_limit(delay=2.0)
    @retry_on_failure(max_retries=3)
    def get_company_info(self, company_identifier: str) -> Dict[str, Any]:
        """
        Get information about a company.
        
        Args:
            company_identifier: Company name or LinkedIn company ID
            
        Returns:
            Company information dictionary
        """
        logger.info(f"Fetching company info: {company_identifier}")
        
        try:
            if self.api_client:
                logger.debug("Using LinkedIn API client for company info")
                company_data = self.api_client.get_company(company_identifier)
                return self._format_company_data(company_data)
            else:
                logger.warning("API client not available. Company info requires authentication.")
                return {"error": "Authentication required"}
                
        except Exception as e:
            logger.error(f"Error fetching company info: {e}")
            raise
    
    def _format_company_data(self, company_data: Dict) -> Dict[str, Any]:
        """
        Format company data from API response.
        
        Args:
            company_data: Raw company data
            
        Returns:
            Formatted company dictionary
        """
        return {
            "company_id": company_data.get("universalName"),
            "name": company_data.get("name"),
            "description": clean_text(company_data.get("description", "")),
            "industry": company_data.get("industries", []),
            "company_size": company_data.get("staffCount"),
            "headquarters": company_data.get("headquarter"),
            "specialties": company_data.get("specialities", []),
            "website": company_data.get("companyPageUrl"),
            "follower_count": company_data.get("followingInfo", {}).get("followerCount"),
            "scraped_at": datetime.now().isoformat(),
        }
    
    @rate_limit(delay=2.0)
    @retry_on_failure(max_retries=3)
    def search_people(
        self,
        keywords: str,
        location: Optional[str] = None,
        current_company: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for people on LinkedIn.
        
        Args:
            keywords: Search keywords
            location: Location filter
            current_company: Filter by current company
            limit: Maximum number of results
            
        Returns:
            List of people profiles
        """
        logger.info(f"Searching people: keywords='{keywords}'")
        
        try:
            if self.api_client:
                logger.debug("Using LinkedIn API client for people search")
                people = self.api_client.search_people(
                    keywords=keywords,
                    limit=limit
                )
                return [self._format_person_data(person) for person in people]
            else:
                logger.warning("API client not available. People search requires authentication.")
                return []
                
        except Exception as e:
            logger.error(f"Error searching people: {e}")
            raise
    
    def _format_person_data(self, person_data: Dict) -> Dict[str, Any]:
        """
        Format person data from search results.
        
        Args:
            person_data: Raw person data
            
        Returns:
            Formatted person dictionary
        """
        return {
            "profile_id": person_data.get("public_id"),
            "name": f"{person_data.get('firstName', '')} {person_data.get('lastName', '')}".strip(),
            "headline": person_data.get("headline"),
            "location": person_data.get("location"),
            "profile_url": f"https://www.linkedin.com/in/{person_data.get('public_id')}/",
            "scraped_at": datetime.now().isoformat(),
        }
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("LinkedIn scraper session closed")


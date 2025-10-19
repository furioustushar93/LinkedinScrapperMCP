"""
Example usage of the LinkedIn Scraper.

This script demonstrates how to use the LinkedIn scraper
programmatically (outside of MCP context).
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path to import scraper
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import LinkedInScraper
from src.utils import setup_logging
from dotenv import load_dotenv


def main():
    """Main example function."""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging(log_level="INFO")
    
    # Initialize scraper
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    scraper = LinkedInScraper(email=email, password=password)
    
    print("=" * 80)
    print("LinkedIn Scraper - Example Usage")
    print("=" * 80)
    print()
    
    # Example 1: Scrape a profile
    print("Example 1: Scraping a LinkedIn Profile")
    print("-" * 80)
    try:
        # Replace with a real LinkedIn profile URL
        profile_url = "https://www.linkedin.com/in/example"
        print(f"Profile URL: {profile_url}")
        
        # Note: This will only work with proper authentication
        # profile_data = scraper.scrape_profile(profile_url)
        # print(json.dumps(profile_data, indent=2))
        
        print("⚠️  Skipped: Replace with a real profile URL and valid credentials")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Example 2: Search for jobs
    print("Example 2: Searching for Jobs")
    print("-" * 80)
    try:
        jobs = scraper.search_jobs(
            keywords="Python Developer",
            location="San Francisco, CA",
            limit=5
        )
        
        if jobs:
            print(f"Found {len(jobs)} jobs:")
            for i, job in enumerate(jobs, 1):
                print(f"\n{i}. {job.get('title')} at {job.get('company')}")
                print(f"   Location: {job.get('location')}")
                print(f"   URL: {job.get('job_url')}")
        else:
            print("⚠️  No jobs found (requires authentication)")
            
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Example 3: Get company information
    print("Example 3: Getting Company Information")
    print("-" * 80)
    try:
        company_info = scraper.get_company_info("google")
        
        if company_info and "error" not in company_info:
            print(f"Company: {company_info.get('name')}")
            print(f"Industry: {company_info.get('industry')}")
            print(f"Size: {company_info.get('company_size')} employees")
            print(f"Website: {company_info.get('website')}")
        else:
            print("⚠️  Company info not available (requires authentication)")
            
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Example 4: Search for people
    print("Example 4: Searching for People")
    print("-" * 80)
    try:
        people = scraper.search_people(
            keywords="Machine Learning Engineer",
            location="New York, NY",
            limit=5
        )
        
        if people:
            print(f"Found {len(people)} profiles:")
            for i, person in enumerate(people, 1):
                print(f"\n{i}. {person.get('name')}")
                print(f"   Headline: {person.get('headline')}")
                print(f"   Location: {person.get('location')}")
                print(f"   URL: {person.get('profile_url')}")
        else:
            print("⚠️  No people found (requires authentication)")
            
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Close the scraper
    scraper.close()
    
    print("=" * 80)
    print("Examples completed!")
    print()
    print("Note: Many features require valid LinkedIn credentials.")
    print("Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file.")
    print("=" * 80)


if __name__ == "__main__":
    main()


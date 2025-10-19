#!/usr/bin/env python3
"""
FastAPI Backend for LinkedIn Scraper

This provides REST API endpoints for all LinkedIn scraping functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

from src.scraper import LinkedInScraper
from src.utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging(log_level=os.getenv("LOG_LEVEL", "INFO"))

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn Scraper API",
    description="REST API for LinkedIn data extraction",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = None

def get_scraper():
    """Get or initialize the LinkedIn scraper."""
    global scraper
    if scraper is None:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")
        scraper = LinkedInScraper(email=email, password=password)
    return scraper


# Request/Response Models
class JobSearchRequest(BaseModel):
    keywords: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    limit: int = 10

class ProfileSearchRequest(BaseModel):
    profile_url: str

class CompanySearchRequest(BaseModel):
    company_identifier: str

class PeopleSearchRequest(BaseModel):
    keywords: str
    location: Optional[str] = None
    current_company: Optional[str] = None
    limit: int = 10


# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend page."""
    html_file = Path(__file__).parent.parent / "frontend" / "templates" / "index.html"
    if html_file.exists():
        return html_file.read_text()
    return """
    <html>
        <head><title>LinkedIn Scraper</title></head>
        <body>
            <h1>LinkedIn Scraper API</h1>
            <p>API is running! Visit <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "LinkedIn Scraper API",
        "version": "1.0.0"
    }

@app.post("/api/jobs/search")
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs on LinkedIn.
    
    - **keywords**: Search keywords (required)
    - **location**: Location filter (optional)
    - **job_type**: Job type filter (optional)
    - **experience_level**: Experience level (optional)
    - **limit**: Maximum number of results (default: 10, max: 50)
    """
    try:
        scraper_instance = get_scraper()
        
        results = scraper_instance.search_jobs(
            keywords=request.keywords,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            limit=min(request.limit, 50)
        )
        
        # Format results
        formatted_results = []
        for job in results:
            formatted_job = {
                "job_id": job.get("job_id", ""),
                "title": job.get("title", "Position title not available"),
                "company": job.get("company") or job.get("companyName") or "Company not specified",
                "location": job.get("location", "Location not specified"),
                "description": job.get("description", "")[:200],
                "posted_at": job.get("posted_at", ""),
                "job_url": job.get("job_url", ""),
                "scraped_at": job.get("scraped_at", "")
            }
            formatted_results.append(formatted_job)
        
        return {
            "success": True,
            "count": len(formatted_results),
            "jobs": formatted_results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile/scrape")
async def scrape_profile(request: ProfileSearchRequest):
    """
    Scrape a LinkedIn profile.
    
    - **profile_url**: LinkedIn profile URL (required)
    """
    try:
        scraper_instance = get_scraper()
        result = scraper_instance.scrape_profile(request.profile_url)
        
        return {
            "success": True,
            "profile": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/company/info")
async def get_company_info(request: CompanySearchRequest):
    """
    Get company information from LinkedIn.
    
    - **company_identifier**: Company name or LinkedIn company ID (required)
    """
    try:
        scraper_instance = get_scraper()
        result = scraper_instance.get_company_info(request.company_identifier)
        
        return {
            "success": True,
            "company": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/people/search")
async def search_people(request: PeopleSearchRequest):
    """
    Search for people on LinkedIn.
    
    - **keywords**: Search keywords (required)
    - **location**: Location filter (optional)
    - **current_company**: Filter by current company (optional)
    - **limit**: Maximum number of results (default: 10, max: 50)
    """
    try:
        scraper_instance = get_scraper()
        
        results = scraper_instance.search_people(
            keywords=request.keywords,
            location=request.location,
            current_company=request.current_company,
            limit=min(request.limit, 50)
        )
        
        return {
            "success": True,
            "count": len(results),
            "people": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get API usage statistics."""
    return {
        "total_requests": "N/A",
        "uptime": "N/A",
        "status": "operational"
    }


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global scraper
    if scraper:
        scraper.close()


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 80)
    print(" " * 20 + "LinkedIn Scraper - FastAPI Backend")
    print("=" * 80)
    print("\n🚀 Starting server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🌐 Frontend: http://localhost:8000")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


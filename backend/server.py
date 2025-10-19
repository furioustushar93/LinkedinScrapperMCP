#!/usr/bin/env python3
"""
LinkedIn Scraper MCP Server

This server provides LinkedIn scraping capabilities through the Model Context Protocol.
It exposes tools for scraping profiles, searching jobs, getting company info, and searching people.
"""

import os
import sys
import json
import asyncio
from typing import Any, Optional
from pathlib import Path

# Add backend directory to path
_backend_dir = Path(__file__).parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from dotenv import load_dotenv
from loguru import logger

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Import scraper and utils from backend directory
from scraper import LinkedInScraper
from utils import setup_logging


# Load environment variables
load_dotenv()

# Initialize logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "logs/linkedin_scraper.log")
setup_logging(log_level, log_file)

# Initialize the MCP server
app = Server("linkedin-scraper")

# Initialize the LinkedIn scraper
scraper: Optional[LinkedInScraper] = None


def initialize_scraper():
    """Initialize the LinkedIn scraper with credentials from environment."""
    global scraper
    
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        logger.warning(
            "LinkedIn credentials not found in environment variables. "
            "Some features may be limited. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD."
        )
    
    scraper = LinkedInScraper(email=email, password=password)
    logger.info("LinkedIn scraper initialized")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools for the LinkedIn scraper.
    
    Returns:
        List of Tool objects describing available scraping operations
    """
    return [
        Tool(
            name="scrape_linkedin_profile",
            description=(
                "Scrape a LinkedIn profile and extract information such as name, headline, "
                "summary, location, experience, education, and skills. Requires a valid LinkedIn profile URL."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_url": {
                        "type": "string",
                        "description": "The LinkedIn profile URL to scrape (e.g., https://linkedin.com/in/username)",
                    }
                },
                "required": ["profile_url"],
            },
        ),
        Tool(
            name="search_linkedin_jobs",
            description=(
                "Search for jobs on LinkedIn based on keywords, location, job type, and experience level. "
                "Returns a list of job postings with details like title, company, location, and description."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Search keywords (e.g., 'Python developer', 'Data scientist')",
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter (e.g., 'San Francisco, CA', 'Remote')",
                    },
                    "job_type": {
                        "type": "string",
                        "description": "Job type filter (e.g., 'full-time', 'part-time', 'contract')",
                    },
                    "experience_level": {
                        "type": "string",
                        "description": "Experience level (e.g., 'entry', 'mid-senior', 'director')",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (default: 10, max: 50)",
                        "default": 10,
                    },
                },
                "required": ["keywords"],
            },
        ),
        Tool(
            name="get_company_info",
            description=(
                "Get detailed information about a company on LinkedIn, including description, "
                "industry, size, headquarters, specialties, and follower count."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "company_identifier": {
                        "type": "string",
                        "description": "Company name or LinkedIn company ID (e.g., 'google', 'microsoft')",
                    }
                },
                "required": ["company_identifier"],
            },
        ),
        Tool(
            name="search_people",
            description=(
                "Search for people on LinkedIn based on keywords, location, and current company. "
                "Returns a list of profiles with basic information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Search keywords (e.g., 'machine learning engineer', 'product manager')",
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter (e.g., 'New York, NY')",
                    },
                    "current_company": {
                        "type": "string",
                        "description": "Filter by current company (e.g., 'Google', 'Amazon')",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 10, max: 50)",
                        "default": 10,
                    },
                },
                "required": ["keywords"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from the MCP client.
    
    Args:
        name: Name of the tool to execute
        arguments: Arguments for the tool
        
    Returns:
        List of TextContent with the results
    """
    global scraper
    
    if scraper is None:
        initialize_scraper()
    
    try:
        logger.info(f"Executing tool: {name}")
        logger.debug(f"Arguments: {arguments}")
        
        if name == "scrape_linkedin_profile":
            profile_url = arguments.get("profile_url")
            if not profile_url:
                raise ValueError("profile_url is required")
            
            result = scraper.scrape_profile(profile_url)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]
        
        elif name == "search_linkedin_jobs":
            keywords = arguments.get("keywords")
            if not keywords:
                raise ValueError("keywords is required")
            
            location = arguments.get("location")
            job_type = arguments.get("job_type")
            experience_level = arguments.get("experience_level")
            limit = min(arguments.get("limit", 10), 50)
            
            results = scraper.search_jobs(
                keywords=keywords,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                limit=limit,
            )
            
            # Ensure each job has all required fields with fallbacks
            formatted_results = []
            for job in results:
                formatted_job = {
                    "job_id": job.get("job_id", ""),
                    "title": job.get("title", "Position title not available"),
                    "company": job.get("company") or job.get("companyName") or "Company not specified",
                    "location": job.get("location", "Location not specified"),
                    "description": job.get("description", "")[:200],  # Limit description
                    "posted_at": job.get("posted_at", ""),
                    "job_url": job.get("job_url", ""),
                    "scraped_at": job.get("scraped_at", "")
                }
                formatted_results.append(formatted_job)
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(formatted_results, indent=2),
                )
            ]
        
        elif name == "get_company_info":
            company_identifier = arguments.get("company_identifier")
            if not company_identifier:
                raise ValueError("company_identifier is required")
            
            result = scraper.get_company_info(company_identifier)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]
        
        elif name == "search_people":
            keywords = arguments.get("keywords")
            if not keywords:
                raise ValueError("keywords is required")
            
            location = arguments.get("location")
            current_company = arguments.get("current_company")
            limit = min(arguments.get("limit", 10), 50)
            
            results = scraper.search_people(
                keywords=keywords,
                location=location,
                current_company=current_company,
                limit=limit,
            )
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(results, indent=2),
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "tool": name,
                    "arguments": arguments,
                }, indent=2),
            )
        ]


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting LinkedIn Scraper MCP Server")
    logger.info(f"Server name: linkedin-scraper")
    logger.info(f"Python version: {sys.version}")
    
    # Initialize the scraper
    initialize_scraper()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running on stdio")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        if scraper:
            scraper.close()
        logger.info("Server shutdown complete")


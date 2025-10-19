#!/usr/bin/env python3
"""
Gemini Integration for LinkedIn Scraper

This module provides integration between Google's Gemini AI and the LinkedIn scraper.
Since Gemini doesn't support MCP natively, this creates a direct function-calling interface.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add backend directory to path
_backend_dir = Path(__file__).parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

try:
    import google.generativeai as genai
except ImportError:
    print("Please install: pip install google-generativeai")
    genai = None

from dotenv import load_dotenv
from loguru import logger

# Import from backend directory
from scraper import LinkedInScraper
from utils import setup_logging


class GeminiLinkedInAssistant:
    """
    LinkedIn Scraper integrated with Google Gemini.
    Uses Gemini's function calling to provide LinkedIn scraping capabilities.
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize the Gemini-powered LinkedIn assistant.
        
        Args:
            gemini_api_key: Google Gemini API key (or set GEMINI_API_KEY env var)
        """
        load_dotenv()
        setup_logging()
        
        # Initialize Gemini
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable or pass gemini_api_key parameter.\n"
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        
        if genai is None:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize LinkedIn scraper
        self.scraper = LinkedInScraper()
        
        # Define tools for Gemini
        self.tools = self._create_gemini_tools()
        
        # Initialize Gemini model with function calling
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',
            tools=self.tools
        )
        
        logger.info("Gemini LinkedIn Assistant initialized")
    
    def _create_gemini_tools(self) -> List[Dict]:
        """
        Create Gemini function calling tools.
        
        Returns:
            List of tool definitions for Gemini
        """
        return [
            {
                "name": "scrape_linkedin_profile",
                "description": "Scrape a LinkedIn profile and extract information such as name, headline, summary, location, experience, and education.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "profile_url": {
                            "type": "string",
                            "description": "The LinkedIn profile URL to scrape (e.g., https://linkedin.com/in/username)"
                        }
                    },
                    "required": ["profile_url"]
                }
            },
            {
                "name": "search_linkedin_jobs",
                "description": "Search for jobs on LinkedIn based on keywords, location, job type, and experience level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "Search keywords (e.g., 'Python developer', 'Data scientist')"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location filter (e.g., 'San Francisco, CA', 'Remote')"
                        },
                        "job_type": {
                            "type": "string",
                            "description": "Job type filter (e.g., 'full-time', 'part-time', 'contract')"
                        },
                        "experience_level": {
                            "type": "string",
                            "description": "Experience level (e.g., 'entry', 'mid-senior', 'director')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10, max: 50)"
                        }
                    },
                    "required": ["keywords"]
                }
            },
            {
                "name": "get_company_info",
                "description": "Get detailed information about a company on LinkedIn, including description, industry, size, headquarters, and specialties.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_identifier": {
                            "type": "string",
                            "description": "Company name or LinkedIn company ID (e.g., 'google', 'microsoft')"
                        }
                    },
                    "required": ["company_identifier"]
                }
            },
            {
                "name": "search_people",
                "description": "Search for people on LinkedIn based on keywords, location, and current company.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "Search keywords (e.g., 'machine learning engineer', 'product manager')"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location filter (e.g., 'New York, NY')"
                        },
                        "current_company": {
                            "type": "string",
                            "description": "Filter by current company (e.g., 'Google', 'Amazon')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10, max: 50)"
                        }
                    },
                    "required": ["keywords"]
                }
            }
        ]
    
    def _execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a LinkedIn scraper function.
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            Function result
        """
        logger.info(f"Executing function: {function_name}")
        logger.debug(f"Arguments: {arguments}")
        
        try:
            if function_name == "scrape_linkedin_profile":
                result = self.scraper.scrape_profile(arguments["profile_url"])
            
            elif function_name == "search_linkedin_jobs":
                result = self.scraper.search_jobs(
                    keywords=arguments["keywords"],
                    location=arguments.get("location"),
                    job_type=arguments.get("job_type"),
                    experience_level=arguments.get("experience_level"),
                    limit=min(arguments.get("limit", 10), 50)
                )
            
            elif function_name == "get_company_info":
                result = self.scraper.get_company_info(arguments["company_identifier"])
            
            elif function_name == "search_people":
                result = self.scraper.search_people(
                    keywords=arguments["keywords"],
                    location=arguments.get("location"),
                    current_company=arguments.get("current_company"),
                    limit=min(arguments.get("limit", 10), 50)
                )
            
            else:
                result = {"error": f"Unknown function: {function_name}"}
            
            logger.success(f"Function {function_name} executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error executing {function_name}: {e}")
            return {"error": str(e)}
    
    def chat(self, user_message: str) -> str:
        """
        Send a message to Gemini and handle function calls.
        
        Args:
            user_message: User's message/query
            
        Returns:
            Gemini's response
        """
        logger.info(f"User query: {user_message}")
        
        chat = self.model.start_chat()
        response = chat.send_message(user_message)
        
        # Handle function calls
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            logger.info(f"Gemini wants to call: {function_name}")
            
            # Execute the function
            function_result = self._execute_function(function_name, function_args)
            
            # Send result back to Gemini
            response = chat.send_message({
                "function_response": {
                    "name": function_name,
                    "response": function_result
                }
            })
        
        # Return final text response
        return response.text
    
    def close(self):
        """Close the scraper session."""
        self.scraper.close()
        logger.info("Gemini LinkedIn Assistant closed")


def main():
    """Example usage of Gemini LinkedIn Assistant."""
    print("=" * 80)
    print("Gemini LinkedIn Assistant - Interactive Mode")
    print("=" * 80)
    print()
    
    try:
        assistant = GeminiLinkedInAssistant()
        print("✓ Assistant initialized successfully!")
        print()
        print("You can ask questions like:")
        print("  - 'Search for Python developer jobs in San Francisco'")
        print("  - 'Get information about Google as a company'")
        print("  - 'Find machine learning engineers in New York'")
        print()
        print("Type 'exit' to quit")
        print("-" * 80)
        print()
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = assistant.chat(user_input)
                print(f"\nGemini: {response}\n")
                print("-" * 80)
                print()
            except Exception as e:
                print(f"\nError: {e}\n")
        
        assistant.close()
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nTo use Gemini, you need:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Set in .env: GEMINI_API_KEY=your_api_key")
        print("3. Install: pip install google-generativeai")
        print()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()


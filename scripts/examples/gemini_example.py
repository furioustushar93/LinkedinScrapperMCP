#!/usr/bin/env python3
"""
Example: Using LinkedIn Scraper with Google Gemini

This example shows how to use the LinkedIn scraper with Gemini AI
instead of Claude Desktop.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gemini_integration import GeminiLinkedInAssistant


def example_basic_usage():
    """Basic usage example."""
    print("=" * 80)
    print("Example 1: Basic Usage")
    print("=" * 80)
    print()
    
    assistant = GeminiLinkedInAssistant()
    
    # Example query
    response = assistant.chat("Search for Python developer jobs in San Francisco")
    print(response)
    
    assistant.close()
    print()


def example_profile_scraping():
    """Profile scraping example."""
    print("=" * 80)
    print("Example 2: Profile Scraping")
    print("=" * 80)
    print()
    
    assistant = GeminiLinkedInAssistant()
    
    # Ask Gemini to scrape a profile
    response = assistant.chat(
        "Can you scrape the LinkedIn profile at https://linkedin.com/in/example "
        "and tell me about their experience?"
    )
    print(response)
    
    assistant.close()
    print()


def example_company_research():
    """Company research example."""
    print("=" * 80)
    print("Example 3: Company Research")
    print("=" * 80)
    print()
    
    assistant = GeminiLinkedInAssistant()
    
    # Research a company
    response = assistant.chat(
        "Tell me about Google as a company on LinkedIn. "
        "What's their industry and how many employees do they have?"
    )
    print(response)
    
    assistant.close()
    print()


def example_people_search():
    """People search example."""
    print("=" * 80)
    print("Example 4: People Search")
    print("=" * 80)
    print()
    
    assistant = GeminiLinkedInAssistant()
    
    # Search for people
    response = assistant.chat(
        "Find machine learning engineers working in New York. "
        "Show me the top 5 results."
    )
    print(response)
    
    assistant.close()
    print()


def interactive_mode():
    """Interactive chat mode."""
    print("=" * 80)
    print("Gemini LinkedIn Assistant - Interactive Mode")
    print("=" * 80)
    print()
    print("Chat with Gemini about LinkedIn data!")
    print("Type 'exit' to quit")
    print("-" * 80)
    print()
    
    assistant = GeminiLinkedInAssistant()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        
        if not user_input:
            continue
        
        try:
            response = assistant.chat(user_input)
            print(f"\nGemini: {response}\n")
            print("-" * 80)
        except Exception as e:
            print(f"\nError: {e}\n")
    
    assistant.close()
    print("\nGoodbye!")


def main():
    """Main function."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Gemini + LinkedIn Scraper Examples" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    print("Available examples:")
    print("  1. Basic job search")
    print("  2. Profile scraping")
    print("  3. Company research")
    print("  4. People search")
    print("  5. Interactive mode")
    print("  0. Exit")
    print()
    
    while True:
        choice = input("Select an example (0-5): ").strip()
        print()
        
        try:
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                example_basic_usage()
            elif choice == '2':
                example_profile_scraping()
            elif choice == '3':
                example_company_research()
            elif choice == '4':
                example_people_search()
            elif choice == '5':
                interactive_mode()
                break
            else:
                print("Invalid choice. Please select 0-5.")
                print()
        except Exception as e:
            print(f"Error: {e}")
            print()
            print("Make sure you have:")
            print("1. Set GEMINI_API_KEY in .env")
            print("2. Installed: pip install google-generativeai")
            print("3. Set LinkedIn credentials in .env")
            print()
            break


if __name__ == "__main__":
    main()


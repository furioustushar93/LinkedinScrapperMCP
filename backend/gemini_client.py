#!/usr/bin/env python3
"""
Gemini MCP Client for LinkedIn Scraper

This client connects Gemini AI to your MCP server, allowing Gemini to use
all the LinkedIn scraping tools through the Model Context Protocol.

This is the PROPER way to integrate Gemini with MCP - Gemini acts as a client
to your existing MCP server, just like Claude Desktop does.
"""

import asyncio
import os
import sys
import json
from typing import Optional
from contextlib import AsyncExitStack

# MCP client components
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Google's Gen AI SDK
from google import genai
from google.genai import types
from google.genai.types import Tool, FunctionDeclaration, GenerateContentConfig

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiMCPClient:
    """
    Gemini AI client that connects to an MCP server.
    
    This allows Gemini to use any MCP server's tools, including your LinkedIn scraper.
    Supports conversational context and follow-up questions.
    """
    
    def __init__(self, api_key: Optional[str] = None, server_path: Optional[str] = None):
        """
        Initialize the Gemini MCP client.
        
        Args:
            api_key: Gemini API key (or reads from GEMINI_API_KEY env var)
            server_path: Path to MCP server script (optional, can connect later)
        """
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.server_path = server_path
        
        # Get Gemini API key
        gemini_api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please add it to your .env file.\n"
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        
        # Configure Gemini client
        self.genai_client = genai.Client(api_key=gemini_api_key)
        self.function_declarations = []
        
        # Conversation context for follow-up questions
        self.conversation_history = []
        self.last_results = {}  # Store last results for reference
        
        print("✓ Gemini MCP Client initialized")
    
    async def connect(self):
        """Connect to the MCP server using the configured server path."""
        if not self.server_path:
            raise ValueError("No server path configured. Provide server_path in __init__ or call connect_to_server().")
        await self.connect_to_server(self.server_path)
    
    async def connect_to_server(self, server_script_path: str):
        """
        Connect to an MCP server and list available tools.
        
        Args:
            server_script_path: Path to the MCP server script (e.g., src/server.py)
        """
        # Determine command based on file extension
        command = "python" if server_script_path.endswith('.py') else "node"
        
        # Set up server parameters
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path]
        )
        
        # Connect to MCP server via stdio
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # Extract read/write streams
        self.stdio, self.write = stdio_transport
        
        # Initialize MCP client session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        
        # Initialize the session
        await self.session.initialize()
        
        # Get available tools from MCP server
        response = await self.session.list_tools()
        tools = response.tools
        
        print(f"\n✓ Connected to MCP server")
        print(f"✓ Available tools: {[tool.name for tool in tools]}")
        
        # Convert MCP tools to Gemini format
        self.function_declarations = self._convert_mcp_tools_to_gemini(tools)
        print(f"✓ Converted {len(tools)} tools for Gemini\n")
    
    def _clean_schema(self, schema):
        """
        Remove 'title' fields from JSON schema (Gemini doesn't need them).
        
        Args:
            schema: The schema dictionary
            
        Returns:
            Cleaned schema
        """
        if isinstance(schema, dict):
            schema.pop("title", None)
            
            # Recursively clean nested properties
            if "properties" in schema and isinstance(schema["properties"], dict):
                for key in schema["properties"]:
                    schema["properties"][key] = self._clean_schema(schema["properties"][key])
        
        return schema
    
    def _convert_mcp_tools_to_gemini(self, mcp_tools):
        """
        Convert MCP tool definitions to Gemini function declarations.
        
        Args:
            mcp_tools: List of MCP tool objects
            
        Returns:
            List of Gemini Tool objects
        """
        gemini_tools = []
        
        for tool in mcp_tools:
            # Clean the input schema
            parameters = self._clean_schema(tool.inputSchema)
            
            # Create function declaration
            function_declaration = FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=parameters
            )
            
            # Wrap in Tool object
            gemini_tool = Tool(function_declarations=[function_declaration])
            gemini_tools.append(gemini_tool)
        
        return gemini_tools
    
    def _format_results_with_numbers(self, results, result_type="item"):
        """
        Format results with numbered references for follow-up questions.
        
        Args:
            results: List of result dictionaries
            result_type: Type of results (job, profile, company, etc.)
            
        Returns:
            Formatted string with numbered results
        """
        if not results or not isinstance(results, list):
            return None
        
        # Store results for reference
        self.last_results = {
            'type': result_type,
            'data': results,
            'count': len(results)
        }
        
        formatted = f"\n📋 Found {len(results)} {result_type}(s):\n\n"
        
        for i, item in enumerate(results, 1):
            if result_type == "job":
                # Try different possible keys for company name
                company = (item.get('company') or 
                          item.get('companyName') or 
                          item.get('company_name') or 
                          'Company not specified')
                
                title = item.get('title', 'Unknown Position')
                location = item.get('location', 'Location not specified')
                job_url = item.get('job_url', 'N/A')
                
                formatted += f"{i}. **{title}**\n"
                formatted += f"   🏢 Company: {company}\n"
                formatted += f"   📍 Location: {location}\n"
                
                # Add additional details if available
                if item.get('posted_at'):
                    formatted += f"   🕒 Posted: {item.get('posted_at')}\n"
                if item.get('description'):
                    desc = item.get('description', '')[:100]  # First 100 chars
                    if len(item.get('description', '')) > 100:
                        desc += "..."
                    formatted += f"   📝 {desc}\n"
                
                formatted += f"   🔗 Apply: {job_url}\n\n"
            elif result_type == "profile":
                name = item.get('name', f"{item.get('first_name', '')} {item.get('last_name', '')}".strip()) or "Name not available"
                headline = item.get('headline', 'Headline not available')
                location = item.get('location', 'Location not specified')
                profile_url = item.get('profile_url', item.get('url', 'N/A'))
                
                formatted += f"{i}. **{name}**\n"
                formatted += f"   💼 {headline}\n"
                formatted += f"   📍 {location}\n"
                formatted += f"   🔗 Profile: {profile_url}\n\n"
            elif result_type == "company":
                name = item.get('name', 'Company name not available')
                industry = item.get('industry', 'Industry not specified')
                size = item.get('company_size', item.get('staffCount', 'Size not specified'))
                website = item.get('website', item.get('companyPageUrl', 'N/A'))
                
                formatted += f"{i}. **{name}**\n"
                formatted += f"   🏢 Industry: {industry}\n"
                formatted += f"   👥 Size: {size} employees\n"
                formatted += f"   🌐 Website: {website}\n\n"
        
        formatted += "\n💡 You can ask: 'Tell me more about #2' or 'What's the salary for job #3?'\n"
        return formatted
    
    async def process_query(self, query: str) -> str:
        """
        Process a user query using Gemini and execute MCP tool calls if needed.
        Supports conversational context and follow-up questions.
        
        Args:
            query: The user's input query
            
        Returns:
            The response from Gemini
        """
        # Check if this is a follow-up question about previous results
        context_info = ""
        if self.last_results:
            context_info = f"\n\nContext: User has {self.last_results['count']} {self.last_results['type']}(s) from previous query. "
            context_info += "If they refer to numbers (like '#2' or 'the third one'), use that context.\n"
            context_info += f"Previous results summary: {json.dumps(self.last_results['data'][:3], indent=2)}"  # First 3 for context
        
        # Format user input for Gemini with context
        full_query = query + context_info if context_info else query
        
        user_prompt_content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=full_query)]
        )
        
        # Add to conversation history
        self.conversation_history.append(user_prompt_content)
        
        # Send to Gemini with conversation history and available tools
        response = self.genai_client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=self.conversation_history[-10:],  # Keep last 10 messages for context
            config=types.GenerateContentConfig(
                tools=self.function_declarations,
            ),
        )
        
        # Process response and handle function calls
        final_text = []
        tool_results = None
        
        for candidate in response.candidates:
            if candidate.content.parts:
                for part in candidate.content.parts:
                    if isinstance(part, types.Part):
                        if part.function_call:
                            # Gemini wants to call an MCP tool
                            function_call_part = part
                            tool_name = function_call_part.function_call.name
                            tool_args = function_call_part.function_call.args
                            
                            print(f"🔧 Gemini calling: {tool_name}")
                            print(f"📋 Arguments: {json.dumps(dict(tool_args), indent=2)}")
                            
                            # Execute the tool via MCP
                            try:
                                result = await self.session.call_tool(tool_name, dict(tool_args))
                                
                                # Parse MCP result - result.content is a list of TextContent objects
                                parsed_content = []
                                for content_item in result.content:
                                    if hasattr(content_item, 'text'):
                                        try:
                                            # Try to parse JSON from text
                                            parsed_content.append(json.loads(content_item.text))
                                        except json.JSONDecodeError:
                                            # If not JSON, use as-is
                                            parsed_content.append(content_item.text)
                                    else:
                                        parsed_content.append(str(content_item))
                                
                                # If single item, unwrap it
                                if len(parsed_content) == 1:
                                    parsed_content = parsed_content[0]
                                
                                function_response = {"result": parsed_content}
                                tool_results = parsed_content  # Store for formatting
                                print(f"✓ Tool executed successfully\n")
                            except Exception as e:
                                function_response = {"error": str(e)}
                                print(f"❌ Tool execution failed: {e}\n")
                            
                            # Format response for Gemini
                            function_response_part = types.Part.from_function_response(
                                name=tool_name,
                                response=function_response
                            )
                            
                            function_response_content = types.Content(
                                role='tool',
                                parts=[function_response_part]
                            )
                            
                            # Add to conversation history
                            self.conversation_history.append(types.Content(
                                role='model',
                                parts=[function_call_part]
                            ))
                            self.conversation_history.append(function_response_content)
                            
                            # Send tool result back to Gemini with full context
                            response = self.genai_client.models.generate_content(
                                model='gemini-2.0-flash-exp',
                                contents=self.conversation_history[-10:],  # Keep context
                                config=types.GenerateContentConfig(
                                    tools=self.function_declarations,
                                ),
                            )
                            
                            # Extract final response
                            if response.candidates[0].content.parts:
                                response_text = response.candidates[0].content.parts[0].text
                                
                                # Try to parse tool results and format with numbers
                                if tool_results and isinstance(tool_results, list):
                                    # Detect result type
                                    result_type = "item"
                                    if tool_name == "search_linkedin_jobs":
                                        result_type = "job"
                                    elif tool_name == "search_people":
                                        result_type = "profile"
                                    elif tool_name == "get_company_info":
                                        result_type = "company"
                                    
                                    formatted = self._format_results_with_numbers(tool_results, result_type)
                                    if formatted:
                                        response_text += "\n" + formatted
                                
                                final_text.append(response_text)
                        else:
                            # No function call, just text response
                            final_text.append(part.text)
        
        # Add assistant response to conversation history
        if final_text:
            self.conversation_history.append(types.Content(
                role='model',
                parts=[types.Part.from_text(text="\n".join(final_text))]
            ))
        
        return "\n".join(final_text)
    
    async def chat_loop(self):
        """Run an interactive chat session."""
        print("=" * 80)
        print("Gemini MCP Client - Conversational Mode")
        print("=" * 80)
        print("\n💡 Ask questions and follow up naturally!")
        print("\nExamples:")
        print("  • 'Search for Python developer jobs in San Francisco'")
        print("  • 'Tell me more about job #2'")
        print("  • 'What's the salary for the first one?'")
        print("  • 'Get information about Google as a company'")
        print("  • 'Find machine learning engineers in New York'")
        print("\n📝 Commands:")
        print("  • 'clear' - Clear conversation history")
        print("  • 'quit' or 'exit' - Exit the chat")
        print("-" * 80)
        print()
        
        while True:
            try:
                query = input("You: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if query.lower() == 'clear':
                    self.conversation_history = []
                    self.last_results = {}
                    print("\n🔄 Conversation cleared!\n")
                    continue
                
                if not query:
                    continue
                
                # Process query
                print()  # Add blank line before processing
                response = await self.process_query(query)
                print(f"\n💬 Gemini: {response}\n")
                print("-" * 80)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                print("💡 Tip: Try rephrasing your question or type 'clear' to reset\n")
    
    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()
        print("✓ Cleaned up resources")


async def main():
    """Main entry point."""
    # Get server script path
    if len(sys.argv) < 2:
        # Default to the LinkedIn scraper server
        server_script = os.path.join(
            os.path.dirname(__file__),
            "server.py"
        )
        print(f"Using default server: {server_script}")
    else:
        server_script = sys.argv[1]
    
    # Check if server script exists
    if not os.path.exists(server_script):
        print(f"❌ Error: Server script not found: {server_script}")
        print("\nUsage: python gemini_client.py [path_to_server.py]")
        sys.exit(1)
    
    # Initialize and run client
    client = GeminiMCPClient()
    
    try:
        await client.connect_to_server(server_script)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" " * 20 + "Gemini MCP Client for LinkedIn Scraper")
    print("=" * 80 + "\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


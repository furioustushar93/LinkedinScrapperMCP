# Quick Start Guide

Get up and running with the LinkedIn Scraper MCP Server in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- LinkedIn account
- Claude Desktop (optional, for MCP integration)

## Installation

### Option 1: Automated Installation (Recommended)

```bash
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp
bash install.sh
```

### Option 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

## Configuration

Edit the `.env` file with your credentials:

```bash
nano .env
```

Update these values:

```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

**Important**: Keep your credentials secure and never commit them to Git!

## Testing the Installation

### 1. Run the Example Script

```bash
source venv/bin/activate
python examples/example_usage.py
```

This will test the scraper functionality with example queries.

### 2. Run Tests

```bash
make test
# or
pytest tests/ -v
```

## Using with Claude Desktop

### 1. Locate Claude Desktop Config

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Add Server Configuration

Open the config file and add:

```json
{
  "mcpServers": {
    "linkedin-scraper": {
      "command": "python",
      "args": [
        "/Users/tusharaggarwal/Documents/Self-Learning/mcp/src/server.py"
      ],
      "env": {
        "LINKEDIN_EMAIL": "your.email@example.com",
        "LINKEDIN_PASSWORD": "your_password"
      }
    }
  }
}
```

**Note**: Use absolute paths, not relative paths.

### 3. Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

### 4. Verify Connection

In Claude Desktop, you should see the LinkedIn Scraper server listed in the available MCP servers.

## Basic Usage

### In Claude Desktop

Once connected, you can ask Claude to use the LinkedIn scraper:

```
"Can you scrape the LinkedIn profile at https://linkedin.com/in/example?"

"Search for Python developer jobs in San Francisco"

"Get information about Google as a company on LinkedIn"

"Search for machine learning engineers in New York"
```

### Standalone Python

```python
from src.scraper import LinkedInScraper
from dotenv import load_dotenv

load_dotenv()

scraper = LinkedInScraper()

# Scrape a profile
profile = scraper.scrape_profile("https://linkedin.com/in/example")
print(profile)

# Search jobs
jobs = scraper.search_jobs(
    keywords="Python Developer",
    location="San Francisco, CA",
    limit=10
)
print(jobs)

scraper.close()
```

## Available Tools

The MCP server provides these tools:

1. **scrape_linkedin_profile**: Extract profile information
2. **search_linkedin_jobs**: Search for job listings
3. **get_company_info**: Get company details
4. **search_people**: Search for people by keywords

## Common Issues

### "Authentication failed"

- Verify your LinkedIn credentials in `.env`
- Check if your account has 2FA enabled (may need app password)
- LinkedIn may require CAPTCHA for first-time login

### "Rate limit exceeded"

- The scraper automatically handles rate limiting
- Wait a few minutes before retrying
- Reduce the number of requests

### "Module not found"

- Ensure you're in the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Server not showing in Claude Desktop

- Verify the path in `claude_desktop_config.json` is absolute
- Check file permissions: `chmod +x src/server.py`
- Look at Claude Desktop logs for errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore [examples/example_usage.py](examples/example_usage.py) for more examples
- Run tests: `make test`

## Getting Help

- Check the logs: `tail -f logs/linkedin_scraper.log`
- Review existing issues on GitHub
- Open a new issue with details about your problem

## Security Reminder

⚠️ **Important Security Notes**:

1. Never share your `.env` file
2. Don't commit credentials to Git
3. Use strong, unique passwords
4. Enable 2FA on your LinkedIn account
5. Review LinkedIn's Terms of Service

## Legal Notice

This tool is for educational and research purposes. Always:
- Respect LinkedIn's Terms of Service
- Follow rate limits
- Don't scrape private/restricted data
- Comply with data protection laws (GDPR, CCPA)

---

**Congratulations!** 🎉 You're now ready to use the LinkedIn Scraper MCP Server!

For questions or issues, please open an issue on GitHub.


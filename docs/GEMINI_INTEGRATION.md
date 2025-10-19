# Using LinkedIn Scraper with Google Gemini

Since Google Gemini doesn't natively support MCP (Model Context Protocol) yet, we've created a **direct integration** that uses Gemini's function calling capabilities to provide LinkedIn scraping features.

## 🔄 Two Ways to Use This Project

### Option 1: With Claude Desktop (MCP) ✅ Original
- Uses Model Context Protocol
- Integrates with Claude Desktop
- See main `README.md` for setup

### Option 2: With Google Gemini ⭐ New!
- Direct function calling integration
- No MCP needed
- Works in Python scripts or interactive mode

---

## 🚀 Quick Start with Gemini

### Step 1: Get Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### Step 2: Install Gemini Library

```bash
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp
source venv/bin/activate
pip install google-generativeai
```

### Step 3: Configure API Key

```bash
# Edit .env file
nano .env

# Add this line:
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Run Examples

```bash
# Interactive mode
python examples/gemini_example.py

# Or use the main script
python src/gemini_integration.py
```

---

## 💡 Usage Examples

### Example 1: Interactive Chat

```bash
python src/gemini_integration.py
```

Then chat with Gemini:
```
You: Search for Python developer jobs in San Francisco
Gemini: [Shows job listings with details]

You: Tell me about Google as a company
Gemini: [Provides company information]

You: Find machine learning engineers in New York
Gemini: [Lists relevant profiles]
```

### Example 2: Programmatic Usage

```python
from src.gemini_integration import GeminiLinkedInAssistant

# Initialize
assistant = GeminiLinkedInAssistant()

# Ask questions
response = assistant.chat("Search for Python jobs in SF")
print(response)

# Close when done
assistant.close()
```

### Example 3: Multiple Queries

```python
assistant = GeminiLinkedInAssistant()

# Job search
jobs = assistant.chat(
    "Find remote Python developer positions, "
    "show me the top 5 with salary information"
)

# Company research
company = assistant.chat(
    "What's the company culture like at Microsoft? "
    "Get their LinkedIn company information"
)

# Profile analysis
profile = assistant.chat(
    "Analyze this LinkedIn profile: https://linkedin.com/in/example"
)

assistant.close()
```

---

## 🎯 Available Features

All LinkedIn scraping features work with Gemini:

1. **Profile Scraping** 👤
   - "Scrape the profile at [URL]"
   - "Analyze this person's LinkedIn profile"

2. **Job Search** 💼
   - "Find Python developer jobs in San Francisco"
   - "Search for remote positions in data science"

3. **Company Information** 🏢
   - "Tell me about Google as a company"
   - "Get company information for Microsoft"

4. **People Search** 🔍
   - "Find machine learning engineers in NYC"
   - "Search for product managers at Amazon"

---

## 🆚 Comparison: Claude vs Gemini

| Feature | Claude (MCP) | Gemini (Direct) |
|---------|-------------|-----------------|
| **Setup** | Claude Desktop needed | Python script only |
| **Integration** | Native MCP | Function calling |
| **Interface** | Chat in Claude Desktop | Python/Terminal |
| **Flexibility** | AI assistant focused | Programmable |
| **Best For** | Daily usage, AI chat | Automation, scripts |

---

## 🏗️ Architecture

### Claude Desktop (MCP)
```
User → Claude Desktop → MCP Protocol → Your Server → LinkedIn
```

### Gemini (Direct)
```
User → Python Script → Gemini API → Function Calls → Your Scraper → LinkedIn
```

---

## 📝 Code Structure

```
mcp/
├── src/
│   ├── server.py              # MCP server (for Claude)
│   ├── scraper.py            # Core scraping logic (shared)
│   ├── utils.py              # Utilities (shared)
│   └── gemini_integration.py # NEW: Gemini integration
│
└── examples/
    ├── example_usage.py      # Original examples
    └── gemini_example.py     # NEW: Gemini examples
```

---

## 🔧 Advanced Usage

### Custom System Prompt

```python
assistant = GeminiLinkedInAssistant()

# You can customize how Gemini responds
response = assistant.chat(
    "Search for jobs and format the results as a markdown table "
    "with columns: Title, Company, Location, Posted Date"
)
```

### Batch Processing

```python
assistant = GeminiLinkedInAssistant()

companies = ["Google", "Microsoft", "Amazon", "Apple"]

for company in companies:
    info = assistant.chat(f"Get information about {company}")
    print(f"\n{company}:\n{info}\n")

assistant.close()
```

### Error Handling

```python
assistant = GeminiLinkedInAssistant()

try:
    response = assistant.chat("Your query here")
    print(response)
except Exception as e:
    print(f"Error: {e}")
finally:
    assistant.close()
```

---

## 🚀 Running the Examples

### 1. All Examples Menu

```bash
python examples/gemini_example.py
```

Choose from:
1. Basic job search
2. Profile scraping
3. Company research
4. People search
5. Interactive mode

### 2. Interactive Mode Only

```bash
python src/gemini_integration.py
```

### 3. Custom Script

Create your own script:

```python
#!/usr/bin/env python3
from src.gemini_integration import GeminiLinkedInAssistant

def main():
    assistant = GeminiLinkedInAssistant()
    
    # Your custom logic here
    response = assistant.chat("Your query")
    print(response)
    
    assistant.close()

if __name__ == "__main__":
    main()
```

---

## 🔍 Troubleshooting

### "GEMINI_API_KEY not found"

```bash
# Make sure .env file has:
GEMINI_API_KEY=your_key_here

# Check it's loaded:
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

### "google-generativeai not installed"

```bash
pip install google-generativeai
```

### "LinkedIn authentication failed"

```bash
# Check LinkedIn credentials in .env:
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

### Gemini not calling functions

Make sure your query is clear:
- ✅ "Search for Python jobs in SF"
- ❌ "Jobs" (too vague)

---

## 📊 Performance Tips

1. **Rate Limiting**: Built-in delays prevent LinkedIn blocking
2. **Caching**: Consider caching frequent queries
3. **Batch Requests**: Group similar queries together
4. **Error Handling**: Always use try/except blocks

---

## 🔐 Security Notes

- Never commit API keys to Git
- Use environment variables (.env)
- Keep .env in .gitignore
- Rotate API keys regularly

---

## 🎓 Learning Resources

- [Gemini API Docs](https://ai.google.dev/docs)
- [Function Calling Guide](https://ai.google.dev/docs/function_calling)
- [LinkedIn API Terms](https://www.linkedin.com/legal/api-terms)

---

## 📞 Support

Having issues with Gemini integration?

1. Check `.env` has both `GEMINI_API_KEY` and LinkedIn credentials
2. Ensure `google-generativeai` is installed
3. Try the examples: `python examples/gemini_example.py`
4. Check logs in `logs/linkedin_scraper.log`

---

## 🎉 Summary

You now have **TWO ways** to use your LinkedIn scraper:

1. **Claude Desktop** (via MCP)
   - Professional AI assistant experience
   - Native integration
   - Daily usage

2. **Google Gemini** (via function calling)
   - Scriptable and programmable
   - Flexible integration
   - Automation-friendly

Choose the one that fits your use case! 🚀

---

**Next Steps:**
1. Get Gemini API key
2. Add to `.env` file
3. Run `python examples/gemini_example.py`
4. Start building!


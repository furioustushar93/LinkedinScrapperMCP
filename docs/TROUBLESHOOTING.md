# Troubleshooting Guide

Common issues and solutions for the LinkedIn Scraper MCP project.

## 🔧 Import Errors

### "ImportError: attempted relative import with no known parent package"

**Problem**: This happens when Python can't resolve relative imports.

**Solution**: ✅ Already fixed! The code now handles both relative and absolute imports.

If you still see this error:
```bash
# Make sure you're running from the project root
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp

# Activate virtual environment
source venv/bin/activate

# Run the client
python src/gemini_client.py
```

### "ModuleNotFoundError: No module named 'X'"

**Problem**: Dependencies not installed.

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Or install specific package
pip install <package-name>
```

## 🔑 API Key Issues

### "GEMINI_API_KEY not found"

**Problem**: Gemini API key not configured.

**Solution**:
```bash
# 1. Get API key from https://aistudio.google.com/apikey

# 2. Add to .env file
nano .env

# 3. Add this line:
GEMINI_API_KEY=your_actual_api_key_here

# 4. Save and exit (Ctrl+X, Y, Enter)
```

### "LINKEDIN_EMAIL not found" or Authentication Failed

**Problem**: LinkedIn credentials not configured or invalid.

**Solution**:
```bash
# Edit .env file
nano .env

# Add your credentials:
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# Note: Some features require valid LinkedIn credentials
```

## 🌐 Connection Issues

### "Connection closed" when running Gemini client

**Possible causes**:
1. **Server script path incorrect**
   ```bash
   # Use full path
   python src/gemini_client.py /full/path/to/server.py
   ```

2. **Server has errors**
   ```bash
   # Test server directly
   python src/server.py
   # If errors appear, fix them first
   ```

3. **Dependencies missing**
   ```bash
   # Install MCP SDK
   pip install mcp google-genai
   ```

### "Server script not found"

**Solution**:
```bash
# Make sure you're in project root
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp

# Run with relative path
python src/gemini_client.py src/server.py

# Or absolute path
python src/gemini_client.py /full/path/to/src/server.py
```

## 📦 Installation Issues

### Virtual Environment Not Working

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "bash: install.sh: Permission denied"

```bash
# Make script executable
chmod +x install.sh

# Run it
./install.sh
```

### Pip Install Fails

```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If specific package fails, install others
pip install mcp google-genai python-dotenv loguru
```

## 🤖 Gemini-Specific Issues

### "google.genai module not found"

```bash
# Install the correct package
pip install google-genai

# Not google-generativeai (that's different!)
```

### Gemini returns errors

**Check**:
1. API key is valid
2. You have API quota remaining
3. Using correct model name

```python
# In gemini_client.py, the model is:
model='gemini-2.0-flash-exp'

# If that doesn't work, try:
model='gemini-1.5-pro'
```

## 🔍 LinkedIn Scraping Issues

### "Rate limit exceeded"

**Solution**: Wait a few minutes. LinkedIn limits requests.

```bash
# Increase delay in .env
RATE_LIMIT_DELAY=5  # Increase from 2 to 5 seconds
```

### "Authentication failed"

**Possible causes**:
1. Wrong credentials
2. LinkedIn requires CAPTCHA
3. Account has 2FA enabled

**Solution**:
1. Check credentials in `.env`
2. Try logging in manually first
3. Use app password if 2FA is enabled

### "No results found"

**This is normal!** 
- Some features require LinkedIn Premium
- Some queries may have no results
- LinkedIn API may be rate limiting

## 🐛 Debug Mode

### Enable Verbose Logging

```bash
# Edit .env
LOG_LEVEL=DEBUG

# This will show detailed logs in logs/linkedin_scraper.log
```

### Check Logs

```bash
# View recent logs
tail -f logs/linkedin_scraper.log

# Search for errors
grep -i error logs/linkedin_scraper.log

# View last 50 lines
tail -n 50 logs/linkedin_scraper.log
```

## 🧪 Testing

### Test Server Standalone

```bash
# This should start the MCP server
python src/server.py

# If it hangs waiting for input, it's working!
# Press Ctrl+C to stop
```

### Test Imports

```bash
# Test if imports work
python -c "from src.scraper import LinkedInScraper; print('✅ OK')"
python -c "from src.utils import setup_logging; print('✅ OK')"
```

### Test LinkedIn API

```bash
# Run example
python examples/example_usage.py

# This will show if LinkedIn connection works
```

## 🔄 Common Workflows

### Reset Everything

```bash
# 1. Clean up
make clean

# 2. Reinstall
bash install.sh

# 3. Configure
cp .env.example .env
nano .env  # Add your keys

# 4. Test
python src/gemini_client.py
```

### Update Dependencies

```bash
# Update requirements
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade google-genai
```

## 💻 Platform-Specific Issues

### macOS

**"command not found: python"**
```bash
# Use python3
python3 src/gemini_client.py
```

**Permission issues with Claude Desktop config**
```bash
# Fix permissions
chmod 644 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows

**Line ending issues**
```bash
# Convert line endings
dos2unix install.sh
```

**Path separators**
```bash
# Use forward slashes or raw strings
python src\\gemini_client.py src\\server.py
```

### Linux

**Python version**
```bash
# Make sure Python 3.10+
python3 --version

# Update if needed
sudo apt update
sudo apt install python3.11
```

## 📞 Still Stuck?

### Checklist

- [ ] Virtual environment activated?
- [ ] Dependencies installed? (`pip list`)
- [ ] .env file configured?
- [ ] Running from project root?
- [ ] API keys valid?
- [ ] Logs checked? (`logs/linkedin_scraper.log`)

### Get Help

1. **Check logs**: `tail -f logs/linkedin_scraper.log`
2. **Read error messages**: They usually tell you what's wrong
3. **Check environment**: `env | grep -E "(GEMINI|LINKEDIN)"`
4. **Test components individually**: Server, imports, API keys

### Useful Commands

```bash
# Show Python path
python -c "import sys; print('\n'.join(sys.path))"

# Show installed packages
pip list | grep -E "(mcp|gemini|linkedin)"

# Show environment variables
env | grep -E "(GEMINI|LINKEDIN)"

# Test API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

## 🎯 Quick Fixes

### Issue: Import errors
**Fix**: `pip install -r requirements.txt`

### Issue: API key not found
**Fix**: Add to `.env` file

### Issue: Connection failed
**Fix**: Check server path and dependencies

### Issue: No results
**Fix**: Check LinkedIn credentials

### Issue: Rate limited
**Fix**: Wait 5 minutes, increase delay

---

## 📚 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Gemini API Docs](https://ai.google.dev/docs)
- [LinkedIn API Terms](https://www.linkedin.com/legal/api-terms)

---

**Last Updated**: Project creation

**Need More Help?**
- Check `README.md` for setup instructions
- Check `GEMINI_MCP_CLIENT.md` for Gemini-specific help
- Review error messages carefully - they usually indicate the problem!


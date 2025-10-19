# 🚀 Chatbot Quick Start Guide

Get your LinkedIn Scraper AI chatbot running in **5 minutes**!

## ⚡ One-Command Setup

```bash
# Clone the repository (if not already done)
git clone <your-repo>
cd mcp

# Create .env file with your credentials
cat > .env << EOF
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
GEMINI_API_KEY=your_gemini_api_key_here
EOF

# Start everything!
./start_chatbot.sh
```

That's it! The chatbot will open at http://localhost:3000

## 📋 Step-by-Step Setup

### 1️⃣ Get Your API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 2️⃣ Configure Environment

Create a `.env` file in the project root:

```bash
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Gemini API Key (from step 1)
GEMINI_API_KEY=your_api_key_here

# Optional: Custom MCP server path
MCP_SERVER_PATH=src/server.py
```

### 3️⃣ Run the Chatbot

```bash
chmod +x start_chatbot.sh
./start_chatbot.sh
```

The script will:
- ✅ Install Python dependencies
- ✅ Install Node.js dependencies
- ✅ Start the backend (FastAPI + Gemini)
- ✅ Start the frontend (React + Vite)
- ✅ Open your browser automatically

### 4️⃣ Start Chatting!

Open http://localhost:3000 and try:

```
👤 You: Find AI engineer jobs in San Francisco

🤖 AI: [Shows numbered list of jobs with details]

👤 You: Tell me more about job #2

🤖 AI: [Provides detailed information about that job]
```

## 🎯 Example Conversations

### Job Search
```
You: Search for remote Python developer positions

AI: Found 10 jobs! Here are the top results:
    1. Senior Python Developer - Tech Corp
       📍 Remote | Posted: 2024-01-15
       Apply: [link]
    ...

You: Which ones offer benefits?

AI: Based on the job descriptions, jobs #1, #3, and #7 
    mention comprehensive benefits packages...
```

### Profile Search
```
You: Find machine learning engineers at Google

AI: Found 8 profiles:
    1. John Doe - ML Engineer
       Google | 5 years experience
       Profile: [link]
    ...

You: Show me their education background

AI: Here are the educational backgrounds...
```

### Company Research
```
You: Tell me about OpenAI

AI: OpenAI is an AI research company...
    Industry: Artificial Intelligence
    Founded: 2015
    Employees: 500+
    ...

You: Are they hiring?

AI: Let me search for OpenAI job postings...
```

## 🛠️ Manual Setup (Advanced)

### Backend Only
```bash
# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend
cd backend
python chatbot_api.py
```

Backend runs at: http://localhost:8000

### Frontend Only
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start frontend
npm run dev
```

Frontend runs at: http://localhost:3000

## 🔍 Verify Installation

### Check Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "active_connections": 0
}
```

### Check Frontend
Open http://localhost:3000 in your browser. You should see:
- ✅ "LinkedIn Scraper AI" header
- ✅ Green "Connected" indicator
- ✅ Welcome screen with examples
- ✅ Chat input at the bottom

## ❌ Troubleshooting

### "Command not found: npm"
Install Node.js:
```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt install nodejs npm

# Windows
# Download from: https://nodejs.org
```

### "GEMINI_API_KEY not set"
1. Check your `.env` file exists
2. Verify the API key is correct
3. Restart the backend

### "Port 8000 already in use"
Kill the existing process:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend won't load
1. Check backend is running (port 8000)
2. Clear browser cache
3. Check browser console for errors
4. Try: `cd frontend && npm install && npm run dev`

### WebSocket connection failed
1. Verify backend is running
2. Check firewall settings
3. Try accessing: http://localhost:8000/health
4. Refresh the page

## 📊 System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB for dependencies
- **OS**: macOS, Linux, or Windows

## 🎨 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📱 Mobile Support

The UI is fully responsive and works on:
- 📱 iOS Safari
- 📱 Android Chrome
- 📱 Tablets

## 🚦 Next Steps

Once running, explore:

1. **Try Examples**: Click the example cards on the welcome screen
2. **Follow-up Questions**: Ask about specific results
3. **Clear Context**: Type "clear" to reset conversation
4. **Customize**: Edit components in `frontend/src/components/`

## 📚 Learn More

- [Full Chatbot Guide](CHATBOT_GUIDE.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [Gemini Integration](GEMINI_MCP_CLIENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## 💡 Tips

1. **Be Specific**: "Find senior React developer jobs in NYC" > "Find jobs"
2. **Use Numbers**: "Tell me about #3" references the 3rd result
3. **Ask Follow-ups**: The AI remembers your previous queries
4. **Natural Language**: Talk like you would to a colleague

## 🎉 You're Ready!

Start the chatbot and begin exploring LinkedIn jobs with AI assistance!

```bash
./start_chatbot.sh
```

---

**Need help?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on GitHub.


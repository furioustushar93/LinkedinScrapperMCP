# 🚀 Getting Started with LinkedIn Scraper AI

Welcome! Your AI-powered LinkedIn chatbot is ready to use. Follow these simple steps:

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Or create manually
nano .env
```

Add your credentials:
```bash
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Gemini API Key (paste the key from Step 1)
GEMINI_API_KEY=AIzaSyC...your_key_here

# MCP Server Path (optional, uses default)
MCP_SERVER_PATH=src/server.py
```

### Step 3: Launch the Chatbot

```bash
# Make sure the startup script is executable
chmod +x start_chatbot.sh

# Start everything!
./start_chatbot.sh
```

### Step 4: Open Your Browser

The chatbot will automatically open at: **http://localhost:3000**

If it doesn't open automatically:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## 💬 Try Your First Query

Click an example or type:
```
Find AI engineer jobs in San Francisco
```

Then try follow-ups:
```
Tell me more about job #2
Which ones offer remote work?
What are the requirements for job #3?
```

## 📁 What's Inside

Your project now includes:

### Frontend (React + Vite)
- ✅ Modern UI with Tailwind CSS
- ✅ Real-time chat interface
- ✅ Beautiful job/profile cards
- ✅ Mobile responsive

### Backend (FastAPI)
- ✅ WebSocket server
- ✅ Gemini AI integration
- ✅ Session management
- ✅ Health checks

### AI (Google Gemini)
- ✅ Conversational AI
- ✅ Context awareness
- ✅ Function calling
- ✅ Follow-up questions

### Scraper (LinkedIn)
- ✅ Job search
- ✅ Profile lookup
- ✅ Company research
- ✅ People search

## 🎯 Example Use Cases

### Job Search
```
You: Find remote Python developer jobs

AI: I found 10 remote Python developer positions...
    1. Senior Python Developer - Tech Corp
    2. Python Backend Engineer - Startup Inc
    ...

You: Tell me about the second one

AI: The Python Backend Engineer position at Startup Inc is...
```

### Profile Search
```
You: Find machine learning engineers at Google

AI: I found 8 ML engineers at Google...
    1. John Doe - Senior ML Engineer
    2. Jane Smith - ML Research Scientist
    ...

You: Show me their experience

AI: Here's a summary of their experience...
```

### Company Research
```
You: Tell me about OpenAI

AI: OpenAI is an AI research company...

You: Are they hiring?

AI: Let me search for OpenAI job postings...
```

## 🔧 Manual Setup (Alternative)

If the startup script doesn't work, you can start services manually:

### Terminal 1 - Backend:
```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend
cd backend
python chatbot_api.py
```

### Terminal 2 - Frontend:
```bash
# Install dependencies (first time only)
cd frontend
npm install

# Start frontend
npm run dev
```

### Terminal 3 - Check Status:
```bash
# Check backend health
curl http://localhost:8000/health

# Should return:
# {"status": "healthy", "active_connections": 0}
```

## 🆘 Troubleshooting

### "GEMINI_API_KEY not set"
- Check `.env` file exists in project root
- Verify the API key is correct
- No quotes needed around the key

### "Port already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### "Cannot connect to server"
1. Check backend is running (port 8000)
2. Try: `curl http://localhost:8000/health`
3. Check browser console for errors
4. Refresh the page

### "npm: command not found"
```bash
# Install Node.js

# macOS:
brew install node

# Ubuntu/Debian:
sudo apt install nodejs npm

# Windows:
# Download from: https://nodejs.org
```

### Frontend won't load
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📖 Learn More

- 📘 [Full Documentation](README.md)
- 🤖 [Chatbot Guide](CHATBOT_GUIDE.md)
- 🏗️ [Architecture](ARCHITECTURE_VISUAL.md)
- ✨ [Features List](FEATURES.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING.md)

## 🎨 Customization

### Change UI Colors
Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your colors here
      }
    }
  }
}
```

### Add New Features
1. **Frontend**: Add components in `frontend/src/components/`
2. **Backend**: Extend `backend/chatbot_api.py`
3. **Tools**: Add new tools in `src/server.py`

### Modify Welcome Screen
Edit `frontend/src/components/WelcomeScreen.jsx`

## 🚀 Next Steps

1. ✅ **Test the Chatbot**: Try various queries
2. ✅ **Customize**: Change colors and branding
3. ✅ **Deploy**: Deploy to production
4. ✅ **Share**: Add to your portfolio

## 💡 Pro Tips

- Be specific in your queries: "Find senior React developer jobs in NYC" is better than "Find jobs"
- Use numbered references: "Tell me about #3" to ask about specific results
- Ask follow-ups: The AI remembers your previous queries
- Type "clear" to reset the conversation

## 🎉 You're All Set!

Your chatbot is ready to use. Start exploring LinkedIn jobs with AI assistance!

```bash
./start_chatbot.sh
```

---

**Need Help?**
- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Read [Full Documentation](CHATBOT_GUIDE.md)
- Open an issue on GitHub

**Happy Job Hunting! 🎯**


# 🤖 LinkedIn Scraper AI Chatbot

A beautiful, conversational AI chatbot powered by **Google Gemini** and the **Model Context Protocol (MCP)** for intelligent LinkedIn job searching, profile lookups, and company research.

## ✨ Features

### 🎯 Core Capabilities
- **Job Search**: Find jobs by keywords, location, and filters
- **Profile Lookup**: Search for professionals by name, company, or title
- **Company Research**: Get detailed company information
- **Conversational AI**: Natural follow-up questions and context awareness
- **Real-time Chat**: WebSocket-based instant messaging

### 🎨 Modern UI
- **React 18** - Latest React with hooks
- **Vite** - Lightning-fast build tool and dev server
- **Tailwind CSS** - Beautiful, responsive design
- **Recharts** - Data visualizations (ready for analytics)
- **Axios** - Reliable HTTP client

### 🧠 AI Features
- **Context Awareness**: Remembers previous results for follow-up questions
- **Numbered References**: Reference results by number (e.g., "Tell me more about #2")
- **Natural Language**: Ask questions conversationally
- **Function Calling**: Gemini intelligently calls the right tools

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** and pip
2. **Node.js 16+** and npm
3. **LinkedIn Account** (for scraping)
4. **Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd mcp
   ```

2. **Configure environment**:
   ```bash
   # Copy example .env or create new one
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env
   ```

   Add your credentials:
   ```bash
   # LinkedIn Credentials
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   
   # Gemini API Key
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # MCP Server Path (optional)
   MCP_SERVER_PATH=src/server.py
   ```

3. **Start the chatbot**:
   ```bash
   ./start_chatbot.sh
   ```

   This will:
   - Install all dependencies (Python + Node.js)
   - Start the backend server (port 8000)
   - Start the frontend dev server (port 3000)
   - Open your browser automatically

4. **Access the chatbot**:
   - Open: http://localhost:3000
   - The chatbot UI will load automatically

## 📖 How to Use

### Basic Queries

#### Job Search
```
You: Find AI engineer jobs in San Francisco
AI: [Returns numbered list of jobs]

You: Tell me more about job #2
AI: [Provides detailed information about that specific job]

You: What's the salary range?
AI: [Analyzes job description for salary information]
```

#### Profile Search
```
You: Find software engineers at Google
AI: [Returns profiles]

You: Show me their experience
AI: [Provides work history details]
```

#### Company Research
```
You: Tell me about Microsoft
AI: [Returns company information]

You: What industries do they operate in?
AI: [Provides industry details]
```

### Advanced Features

#### Follow-up Questions
The AI maintains context across the conversation:
```
You: Search for data scientist jobs in NYC
AI: [Returns 5 jobs]

You: Which one is for remote work?
AI: [Analyzes results and identifies remote positions]

You: What are the requirements for job #3?
AI: [Provides specific job requirements]
```

#### Clear Context
Reset the conversation:
```
You: clear
AI: [Clears chat history and context]
```

## 🏗️ Architecture

### Frontend (React + Vite)

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Top navigation bar
│   │   ├── Sidebar.jsx         # Left sidebar with actions
│   │   ├── ChatMessage.jsx     # Individual chat messages
│   │   ├── ChatInput.jsx       # Message input area
│   │   └── WelcomeScreen.jsx   # Initial welcome screen
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # React entry point
│   └── index.css               # Tailwind styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

### Backend (FastAPI + Gemini MCP Client)

```
backend/
└── chatbot_api.py             # FastAPI WebSocket server

src/
├── gemini_client.py           # Gemini MCP client
├── server.py                  # MCP server (tools)
├── scraper.py                 # LinkedIn scraper
└── utils.py                   # Utilities
```

### Data Flow

```
User Input → Frontend (React)
    ↓ WebSocket
Backend (FastAPI) → Gemini Client
    ↓ MCP Protocol
MCP Server → LinkedIn Scraper
    ↓
LinkedIn API → Results
    ↓ MCP Protocol
Gemini Client → Response Generation
    ↓ WebSocket
Frontend → Display to User
```

## 🎨 UI Components

### Header
- Shows connection status
- Displays app branding
- Real-time connection indicator

### Sidebar
- Clear chat button
- Usage instructions
- Quick access to GitHub

### Chat Area
- Numbered job listings with details:
  - Job title and company
  - Location and posting date
  - Description snippet
  - Apply link
- Profile cards
- Company information cards
- Error messages with helpful tips

### Input Area
- Multi-line text input
- Send button
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## 🛠️ Development

### Running in Development

**Backend only**:
```bash
cd backend
python chatbot_api.py
```

**Frontend only**:
```bash
cd frontend
npm run dev
```

**Both together**:
```bash
./start_chatbot.sh
```

### Building for Production

**Frontend**:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`.

**Deploy**:
- Backend: Use Uvicorn with production settings
- Frontend: Serve the `dist` folder with nginx or any static server

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Yes |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `MCP_SERVER_PATH` | Path to MCP server script | No (defaults to src/server.py) |

## 🎯 Example Use Cases

### Job Seeker
1. Search for jobs in specific locations
2. Filter by experience level, industry
3. Get detailed job descriptions
4. Save interesting positions for later

### Recruiter
1. Find candidate profiles
2. Research companies hiring in specific areas
3. Analyze job market trends
4. Identify skill requirements

### Market Research
1. Research companies in specific industries
2. Analyze job posting trends
3. Understand hiring patterns
4. Competitive intelligence

## 🔧 Troubleshooting

### Backend Issues

**"GEMINI_API_KEY not set"**
- Add your API key to `.env` file
- Get it from: https://makersuite.google.com/app/apikey

**"Failed to connect to MCP server"**
- Check that `src/server.py` exists
- Verify Python dependencies are installed
- Check LinkedIn credentials in `.env`

**WebSocket connection failed**
- Ensure backend is running on port 8000
- Check firewall settings
- Verify no other service is using port 8000

### Frontend Issues

**"Cannot connect to server"**
- Verify backend is running
- Check WebSocket URL in browser console
- Try refreshing the page

**Blank screen**
- Check browser console for errors
- Verify Node.js dependencies are installed
- Try clearing browser cache

**Styling issues**
- Run `npm install` in frontend directory
- Rebuild with `npm run dev`

### Common Errors

**Import errors**
```bash
# Solution: Install Python dependencies
pip install -r requirements.txt
```

**Port already in use**
```bash
# Solution: Kill existing process
# macOS/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 🚀 Advanced Configuration

### Custom MCP Server

Use a different MCP server:
```python
# In .env
MCP_SERVER_PATH=/path/to/your/server.py
```

### Custom Gemini Model

Edit `src/gemini_client.py`:
```python
# Change model version
response = self.genai_client.models.generate_content(
    model='gemini-2.0-flash-exp',  # or 'gemini-pro'
    contents=contents,
    config=config
)
```

### WebSocket Configuration

Edit `backend/chatbot_api.py`:
```python
# Change host/port
uvicorn.run(
    "chatbot_api:app",
    host="0.0.0.0",  # Change to specific IP
    port=8000,       # Change port
    reload=True
)
```

## 📊 Performance

- **Response Time**: ~2-5 seconds for simple queries
- **Concurrent Users**: Supports multiple simultaneous connections
- **Rate Limits**: Respects LinkedIn and Gemini API limits
- **Caching**: Results cached for follow-up questions

## 🔐 Security

- **API Keys**: Stored in `.env` (never commit to Git)
- **CORS**: Configured for localhost (update for production)
- **LinkedIn**: Uses official API (respects rate limits)
- **WebSocket**: Secure connection handling

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

## 📧 Support

- **Issues**: GitHub Issues
- **Email**: [Your Email]
- **Docs**: Full documentation in `/docs`

## 🎉 What's Next?

- [ ] Add voice input/output
- [ ] Save conversation history
- [ ] Export results to CSV/PDF
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Analytics dashboard with Recharts
- [ ] Job application tracking
- [ ] Email notifications for new jobs

---

**Built with ❤️ using Google Gemini and Model Context Protocol**

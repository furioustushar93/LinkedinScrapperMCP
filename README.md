# 🤖 LinkedIn Scraper AI Chatbot

> A conversational AI chatbot powered by Google Gemini for intelligent LinkedIn job searching, profile lookups, and company research.

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-purple.svg)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

## ✨ Features

- 🎨 **Modern React UI** - Beautiful interface with React 18, Vite, and Tailwind CSS
- 💬 **Conversational AI** - Natural language interactions powered by Google Gemini
- 🔄 **Real-time Chat** - WebSocket-based instant messaging
- 🧠 **Context Aware** - Maintains conversation history for follow-up questions
- 📊 **Rich Display** - Beautiful job cards, profile cards, and company information
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

### AI Capabilities

- **Job Search** - Find jobs by keywords, location, and filters
- **Profile Lookup** - Search for professionals by name, company, or title
- **Company Research** - Get detailed company information
- **Smart Follow-ups** - "Tell me more about #2" or "Which ones are remote?"

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- LinkedIn Account
- [Gemini API Key](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo>
   cd mcp
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

   Add your credentials:
   ```bash
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Launch the chatbot**
   ```bash
   chmod +x start_chatbot.sh
   ./start_chatbot.sh
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
mcp/
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx           # Main app
│   │   └── index.css         # Tailwind styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                    # Python backend
│   ├── chatbot_api.py        # FastAPI WebSocket server
│   ├── gemini_client.py      # Gemini MCP client
│   ├── server.py             # MCP server
│   ├── scraper.py            # LinkedIn scraper
│   └── utils.py              # Utilities
│
├── docs/                       # Documentation
│   ├── 🚀_START_HERE.md      # Quick start guide
│   ├── CHATBOT_GUIDE.md       # Complete guide
│   ├── ARCHITECTURE_VISUAL.md # System architecture
│   └── FEATURES.md            # Feature list
│
├── scripts/                    # Utility scripts
│   ├── examples/              # Usage examples
│   └── tests/                 # Tests
│
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── start_chatbot.sh          # Launch script
└── README.md                  # This file
```

## 💡 Usage Examples

### Job Search
```
You: Find AI engineer jobs in San Francisco

AI: I found 10 jobs! Here are the results:
    1. Senior AI Engineer - Tech Corp
       📍 San Francisco, CA | Posted: 2 days ago
       🔗 Apply: [link]
    ...

You: Tell me more about job #2

AI: The second position is a Senior AI Engineer...
```

### Profile Search
```
You: Find machine learning engineers at Google

AI: I found 8 profiles:
    1. John Doe - Senior ML Engineer
       Google | 5 years experience
       Profile: [link]
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

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons

### Backend
- **FastAPI** - Web framework
- **WebSocket** - Real-time communication
- **Google Gemini** - AI model
- **MCP Protocol** - Model Context Protocol
- **Python 3.8+** - Programming language

## 📖 Documentation

- **[🚀 Quick Start](docs/🚀_START_HERE.md)** - Get started in 5 minutes
- **[Chatbot Guide](docs/CHATBOT_GUIDE.md)** - Complete documentation
- **[Architecture](docs/ARCHITECTURE_VISUAL.md)** - System design
- **[Features](docs/FEATURES.md)** - All features
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues

## 🔧 Development

### Running Separately

**Backend:**
```bash
cd backend
python chatbot_api.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Yes |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `MCP_SERVER_PATH` | Path to MCP server | No (defaults to backend/server.py) |

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please ensure compliance with:
- LinkedIn's Terms of Service
- Data protection laws (GDPR, CCPA, etc.)
- Ethical web scraping practices
- Rate limiting and respectful data collection

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) - AI-tool integration protocol
- [Google Gemini](https://ai.google.dev/) - Conversational AI
- [React](https://react.dev/) - UI library
- [Vite](https://vitejs.dev/) - Build tool
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

## 📧 Support

- **Documentation**: See [docs/](docs/) directory
- **Issues**: Open an issue on GitHub
- **Email**: [Your Email]

---

**Built with ❤️ using React 18, Vite, FastAPI, Tailwind CSS, and Google Gemini**

⭐ Star this repo if you find it helpful!

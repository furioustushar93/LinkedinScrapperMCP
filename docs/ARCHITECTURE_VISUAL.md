# 🏗️ LinkedIn Scraper AI - Visual Architecture

## 🔄 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        👤 USER BROWSER                               │
│                     http://localhost:3000                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP / WebSocket
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🎨 REACT FRONTEND (Vite)                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  Header    │  │  Sidebar   │  │  Welcome   │  │  ChatMsg   │   │
│  │  .jsx      │  │  .jsx      │  │  Screen    │  │  .jsx      │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│                                                                       │
│  ┌────────────┐           ┌──────────────────────────────┐         │
│  │  ChatInput │           │      App.jsx (State)         │         │
│  │  .jsx      │           │  - messages[]                │         │
│  └────────────┘           │  - WebSocket connection      │         │
│                           │  - isConnected, isLoading    │         │
│                           └──────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ WebSocket (/ws)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  🚀 FASTAPI BACKEND (chatbot_api.py)                 │
│                      http://localhost:8000                           │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │            ConnectionManager                             │       │
│  │  - active_connections: Dict[session_id, WebSocket]      │       │
│  │  - gemini_clients: Dict[session_id, GeminiMCPClient]    │       │
│  │  - connect() / disconnect() / process_query()           │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                       │
│  Endpoints:                                                          │
│  • GET  /          → API info                                       │
│  • GET  /health    → Health check                                   │
│  • WS   /ws        → WebSocket chat                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Python Async
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│            🤖 GEMINI MCP CLIENT (src/gemini_client.py)               │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │  GeminiMCPClient                                         │       │
│  │  • conversation_history: List[Message]                  │       │
│  │  • last_results: Dict (numbered references)             │       │
│  │  • connect() → Connects to MCP server                   │       │
│  │  • process_query(query) → AI reasoning + tool calling   │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                       │
│  Functions:                                                          │
│  • _convert_mcp_tools_to_gemini() → Tool definitions               │
│  • _format_results_with_numbers() → Pretty output                  │
│  • execute tool calls via MCP protocol                             │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ MCP Protocol (stdio)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               🔧 MCP SERVER (src/server.py)                          │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │  Exposed Tools (via MCP):                                │       │
│  │  1. search_linkedin_jobs                                 │       │
│  │     └─ Parameters: keywords, location, filters          │       │
│  │  2. scrape_linkedin_profile                             │       │
│  │     └─ Parameters: profile_url                          │       │
│  │  3. get_company_info                                    │       │
│  │     └─ Parameters: company_name or company_url          │       │
│  │  4. search_people                                       │       │
│  │     └─ Parameters: keywords, location, filters          │       │
│  └─────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Python Class
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│            🔍 LINKEDIN SCRAPER (src/scraper.py)                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │  LinkedInScraper                                         │       │
│  │  • _session: aiohttp session                            │       │
│  │  • _cookies: Authentication cookies                     │       │
│  │  • search_jobs() → Extract job listings                 │       │
│  │  • get_profile() → Extract profile data                 │       │
│  │  • get_company() → Extract company data                 │       │
│  │  • search_people() → Find people                        │       │
│  └─────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP Requests
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      🌐 LINKEDIN API                                 │
│                   (www.linkedin.com)                                 │
│  • Job listings                                                      │
│  • Profile pages                                                     │
│  • Company pages                                                     │
│  • People search                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 📡 Data Flow

### User Query Flow
```
1. User types: "Find AI engineer jobs in San Francisco"
   ↓
2. Frontend: ChatInput captures input
   ↓
3. Frontend: Sends via WebSocket to backend
   {
     type: "query",
     query: "Find AI engineer jobs in San Francisco",
     session_id: "abc-123"
   }
   ↓
4. Backend: ConnectionManager receives message
   ↓
5. Backend: Routes to GeminiMCPClient.process_query()
   ↓
6. Gemini: Analyzes query with conversation_history context
   ↓
7. Gemini: Decides to call "search_linkedin_jobs"
   Function call: {
     name: "search_linkedin_jobs",
     parameters: {
       keywords: "AI engineer",
       location: "San Francisco"
     }
   }
   ↓
8. Gemini Client: Executes tool via MCP protocol
   ↓
9. MCP Server: Receives tool call
   ↓
10. MCP Server: Calls LinkedInScraper.search_jobs()
   ↓
11. Scraper: Makes HTTP request to LinkedIn
   ↓
12. LinkedIn: Returns job data (JSON)
   ↓
13. Scraper: Parses and formats data
   [
     {
       job_id: "123",
       title: "Senior AI Engineer",
       company: "Tech Corp",
       location: "San Francisco, CA",
       ...
     },
     ...
   ]
   ↓
14. MCP Server: Returns formatted results
   ↓
15. Gemini Client: Receives results
   ↓
16. Gemini Client: Formats with numbers & stores in last_results
   ↓
17. Gemini: Generates natural language response
   "I found 10 AI engineer jobs in San Francisco..."
   ↓
18. Backend: Sends response via WebSocket
   {
     type: "response",
     content: "I found 10 jobs..."
   }
   ↓
19. Frontend: Receives message
   ↓
20. Frontend: ChatMessage renders rich job cards
   ↓
21. User: Sees beautiful job listings!
```

### Follow-up Query Flow
```
1. User types: "Tell me more about job #2"
   ↓
2. Gemini Client: Checks last_results
   {
     type: "job",
     data: [...],  // Previously stored jobs
     count: 10
   }
   ↓
3. Gemini: Understands "#2" refers to 2nd job in last_results
   ↓
4. Gemini: Retrieves job details from last_results.data[1]
   ↓
5. Gemini: Generates detailed response about that specific job
   ↓
6. Frontend: Displays detailed information
```

## 🔌 WebSocket Communication

### Connection Lifecycle
```
┌──────────┐                                    ┌──────────┐
│ Frontend │                                    │ Backend  │
└──────────┘                                    └──────────┘
     │                                                │
     │  1. WebSocket Connect                         │
     ├──────────────────────────────────────────────▶│
     │                                                │
     │  2. Connection Accepted                       │
     │◀──────────────────────────────────────────────┤
     │                                                │
     │  3. Session ID                                │
     │◀──────────────────────────────────────────────┤
     │  { type: "session_id", session_id: "..." }   │
     │                                                │
     │  4. User Query                                │
     ├──────────────────────────────────────────────▶│
     │  { type: "query", query: "..." }             │
     │                                                │
     │  5. Thinking Indicator (optional)            │
     │◀──────────────────────────────────────────────┤
     │  { type: "thinking" }                        │
     │                                                │
     │  6. Response                                  │
     │◀──────────────────────────────────────────────┤
     │  { type: "response", content: "..." }        │
     │                                                │
     │  7. Clear Command                             │
     ├──────────────────────────────────────────────▶│
     │  { type: "clear" }                           │
     │                                                │
     │  8. Confirmation                              │
     │◀──────────────────────────────────────────────┤
     │                                                │
     │  9. Disconnect                                │
     ├──────────────────────────────────────────────▶│
     │                                                │
     │  10. Cleanup                                  │
     │◀──────────────────────────────────────────────┤
```

## 🧩 Component Hierarchy

```
App.jsx (Root)
├── Sidebar
│   ├── Logo
│   ├── Actions
│   │   └── Clear Chat Button
│   └── Info Section
│       ├── Usage Tips
│       └── GitHub Link
│
├── Main Content Area
│   ├── Header
│   │   ├── Brand
│   │   └── Connection Status
│   │
│   ├── Messages Area
│   │   ├── WelcomeScreen (if no messages)
│   │   │   ├── Welcome Message
│   │   │   ├── Example Cards (4)
│   │   │   └── Pro Tips
│   │   │
│   │   └── Message List (if messages exist)
│   │       ├── ChatMessage (user)
│   │       │   ├── Avatar
│   │       │   ├── Content
│   │       │   └── Timestamp
│   │       │
│   │       ├── ChatMessage (assistant)
│   │       │   ├── Avatar
│   │       │   ├── Content
│   │       │   │   ├── Job Cards
│   │       │   │   ├── Profile Cards
│   │       │   │   ├── Company Cards
│   │       │   │   └── Text Response
│   │       │   └── Timestamp
│   │       │
│   │       └── Loading Indicator
│   │
│   └── ChatInput
│       ├── Textarea
│       ├── Send Button
│       └── Helper Text
```

## 🗂️ State Management

### Frontend State (React)
```javascript
App.jsx State:
├── messages: Array<Message>
│   └── Message {
│       id: number,
│       type: 'user' | 'assistant' | 'error',
│       content: string | object,
│       timestamp: Date
│   }
├── isConnected: boolean
├── isLoading: boolean
├── sessionId: string | null
└── wsRef: WebSocket
```

### Backend State (Python)
```python
ConnectionManager:
├── active_connections: Dict[str, WebSocket]
│   └── { session_id: WebSocket }
├── gemini_clients: Dict[str, GeminiMCPClient]
│   └── { session_id: GeminiMCPClient }
└── client_tasks: Dict[str, asyncio.Task]
    └── { session_id: Task }

GeminiMCPClient:
├── conversation_history: List[Message]
│   └── Messages with roles (user/model) and content
├── last_results: Dict
│   ├── type: str (job/profile/company)
│   ├── data: List[Dict]
│   └── count: int
└── session: ClientSession (MCP)
```

## 🔐 Security Layers

```
┌─────────────────────────────────────────┐
│ 1. Environment Variables (.env)         │
│    ├── LINKEDIN_EMAIL                   │
│    ├── LINKEDIN_PASSWORD                │
│    └── GEMINI_API_KEY                   │
└─────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 2. Backend Validation                   │
│    ├── Check API keys                   │
│    ├── Validate inputs                  │
│    └── Rate limiting                    │
└─────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 3. CORS Configuration                   │
│    └── Allow specific origins           │
└─────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 4. React XSS Protection                 │
│    └── Automatic escaping               │
└─────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ 5. LinkedIn Rate Limiting               │
│    └── Respect API limits               │
└─────────────────────────────────────────┘
```

## 📊 Performance Optimizations

```
Frontend:
├── React.memo for components
├── useCallback for functions
├── Lazy loading (ready)
├── Code splitting (Vite)
└── Browser caching

Backend:
├── Async/await throughout
├── Connection pooling
├── Response caching (in last_results)
├── Efficient WebSocket handling
└── Rate limiting

Scraper:
├── aiohttp for async requests
├── Connection reuse
├── Intelligent parsing
└── Minimal data extraction
```

## 🔄 Technology Stack Visual

```
┌──────────────────────────────────────────────────────┐
│                   PRESENTATION                        │
│  React 18 • Vite • Tailwind CSS • Lucide Icons      │
└──────────────────────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                   COMMUNICATION                       │
│     WebSocket • HTTP • JSON • MCP Protocol           │
└──────────────────────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                   APPLICATION                         │
│        FastAPI • Python • Async/Await                │
└──────────────────────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                   AI & LOGIC                         │
│  Google Gemini • Function Calling • Context Mgmt     │
└──────────────────────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                   DATA LAYER                         │
│      LinkedIn API • Web Scraping • Data Parsing      │
└──────────────────────────────────────────────────────┘
```

---

**This architecture provides:**
- ✅ Scalability - Can handle multiple users
- ✅ Maintainability - Clean separation of concerns
- ✅ Extensibility - Easy to add new features
- ✅ Performance - Async operations throughout
- ✅ Security - Multiple security layers
- ✅ User Experience - Real-time, responsive UI


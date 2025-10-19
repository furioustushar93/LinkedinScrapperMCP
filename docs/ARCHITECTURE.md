# Architecture Documentation

## System Overview

The LinkedIn Scraper MCP Server is designed with a modular, layered architecture that separates concerns and provides a clean interface for AI assistants through the Model Context Protocol.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Assistant Layer                      │
│                  (Claude Desktop, etc.)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol
                         │ (stdio)
┌────────────────────────▼────────────────────────────────────┐
│                    MCP Server Layer                          │
│                     (src/server.py)                          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ list_tools  │  │ call_tool   │  │ error       │        │
│  │   handler   │  │   handler   │  │  handling   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Function Calls
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Business Logic Layer                        │
│                    (src/scraper.py)                          │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   Profile    │ │     Job      │ │   Company    │       │
│  │   Scraper    │ │   Search     │ │    Info      │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   People     │ │    Rate      │ │    Retry     │       │
│  │   Search     │ │   Limiter    │ │   Handler    │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Data Source Layer                          │
│                                                              │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │  LinkedIn API    │        │  Web Scraping    │          │
│  │  (linkedin-api)  │        │  (BeautifulSoup) │          │
│  └──────────────────┘        └──────────────────┘          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
                    ┌────▼────┐
                    │LinkedIn │
                    │  Servers│
                    └─────────┘

       ┌─────────────────────────────────────┐
       │      Supporting Modules             │
       │                                     │
       │  ┌────────────┐  ┌────────────┐   │
       │  │  Utilities │  │   Logging  │   │
       │  │ (utils.py) │  │  (loguru)  │   │
       │  └────────────┘  └────────────┘   │
       │                                     │
       │  ┌────────────┐  ┌────────────┐   │
       │  │   Config   │  │   Tests    │   │
       │  │  (.env)    │  │  (pytest)  │   │
       │  └────────────┘  └────────────┘   │
       └─────────────────────────────────────┘
```

## Component Details

### 1. MCP Server Layer (`src/server.py`)

**Purpose**: Interface between AI assistants and scraping logic

**Key Components**:
- `list_tools()`: Registers available tools with MCP
- `call_tool()`: Routes tool calls to appropriate handlers
- `main()`: Server initialization and lifecycle management

**Responsibilities**:
- MCP protocol implementation
- Request validation
- Response formatting
- Error handling and reporting
- Logging

**Technologies**:
- MCP SDK
- Python asyncio
- JSON serialization

### 2. Business Logic Layer (`src/scraper.py`)

**Purpose**: Core scraping and data extraction logic

**Key Components**:

#### LinkedInScraper Class
```python
class LinkedInScraper:
    - __init__()              # Initialize scraper
    - scrape_profile()        # Profile extraction
    - search_jobs()           # Job search
    - get_company_info()      # Company data
    - search_people()         # People search
    - close()                 # Cleanup
```

**Features**:
- Rate limiting with decorators
- Retry mechanism with exponential backoff
- Session management
- Authentication handling
- Data formatting and normalization

**Technologies**:
- linkedin-api library
- requests library
- BeautifulSoup4
- Session management

### 3. Utilities Layer (`src/utils.py`)

**Purpose**: Reusable helper functions

**Key Functions**:
- `setup_logging()`: Configure logging
- `rate_limit()`: Rate limiting decorator
- `retry_on_failure()`: Retry decorator
- `sanitize_url()`: URL validation
- `extract_linkedin_id()`: ID extraction
- `clean_text()`: Text normalization

**Design Patterns**:
- Decorator pattern (rate limiting, retry)
- Factory pattern (logging setup)
- Strategy pattern (user agent rotation)

### 4. Data Flow

```
┌──────────────┐
│ User Request │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│ MCP Server receives │
│ tool call request   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Validate arguments  │
│ and parameters      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Call appropriate    │
│ scraper method      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Rate limit check    │
│ (wait if needed)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Make HTTP request   │
│ to LinkedIn         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Parse response      │
│ (API or HTML)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Format data         │
│ as JSON             │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Return to MCP       │
│ server              │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Send response to    │
│ AI assistant        │
└─────────────────────┘
```

## Design Principles

### 1. Separation of Concerns
- **MCP Layer**: Protocol and communication
- **Business Layer**: Scraping logic
- **Utility Layer**: Common functions
- **Data Layer**: External APIs

### 2. Single Responsibility
Each module has one clear purpose:
- `server.py`: MCP protocol handling
- `scraper.py`: Data extraction
- `utils.py`: Helper functions

### 3. Dependency Injection
```python
# Configuration injected via environment
scraper = LinkedInScraper(
    email=os.getenv("LINKEDIN_EMAIL"),
    password=os.getenv("LINKEDIN_PASSWORD")
)
```

### 4. Error Handling Hierarchy

```
┌─────────────────────────────┐
│  Application Level          │
│  (Graceful degradation)     │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  Service Level              │
│  (Retry with backoff)       │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  Transport Level            │
│  (Network errors)           │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  Data Level                 │
│  (Parsing errors)           │
└─────────────────────────────┘
```

## Security Architecture

### 1. Credential Management
```
Environment Variables (.env)
          │
          ▼
    Application Memory
          │
          ▼
    Secure Session
          │
          ▼
    HTTPS to LinkedIn
```

### 2. Input Validation
```
User Input
    │
    ▼
URL Sanitization
    │
    ▼
Parameter Validation
    │
    ▼
Safe Execution
```

### 3. Rate Limiting
```
Request → Rate Limiter → Delay Check → Allow/Wait → Execute
                                │
                                ▼
                        Wait + Random Jitter
```

## Performance Considerations

### 1. Rate Limiting
- Minimum 2 seconds between requests
- Random jitter to avoid patterns
- Per-endpoint rate limiting

### 2. Session Management
- Persistent HTTP connections
- Connection pooling
- Cookie handling

### 3. Caching (Future)
```
Request → Cache Check → Hit? → Return Cached
               │          
               ▼ Miss
         Fetch from API → Cache Result → Return
```

## Extensibility

### Adding New Tools

1. **Add scraper method** in `scraper.py`:
```python
def new_feature(self, param: str) -> Dict:
    # Implementation
    pass
```

2. **Register tool** in `server.py`:
```python
Tool(
    name="new_feature",
    description="...",
    inputSchema={...}
)
```

3. **Add handler** in `call_tool()`:
```python
elif name == "new_feature":
    result = scraper.new_feature(arguments.get("param"))
    return [TextContent(type="text", text=json.dumps(result))]
```

4. **Write tests** in `test_scraper.py`

## Testing Strategy

```
┌─────────────────┐
│  Unit Tests     │  ← Test individual functions
└────────┬────────┘
         │
┌────────▼────────┐
│Integration Tests│  ← Test component interaction
└────────┬────────┘
         │
┌────────▼────────┐
│  E2E Tests      │  ← Test complete workflows
└─────────────────┘
```

## Deployment Architecture

### Local Development
```
Developer Machine
    │
    ├─ Virtual Environment
    ├─ .env configuration
    ├─ Local logs
    └─ MCP Server (stdio)
```

### Claude Desktop Integration
```
Claude Desktop
    │
    ├─ Configuration file
    ├─ MCP Server process
    └─ stdio communication
```

### Future: Docker Deployment
```
Docker Container
    │
    ├─ Python runtime
    ├─ Dependencies
    ├─ Application code
    └─ Volume mounts (logs, config)
```

## Monitoring & Logging

### Log Flow
```
Application Event
    │
    ▼
Loguru Logger
    │
    ├─ Console Output (formatted)
    └─ File Output (rotated)
          │
          ▼
    logs/linkedin_scraper.log
```

### Log Levels
- **DEBUG**: Detailed diagnostic info
- **INFO**: General information
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: System failures

## Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| Protocol | MCP SDK, stdio |
| Server | Python 3.10+, asyncio |
| Scraping | requests, BeautifulSoup4, linkedin-api |
| Data | JSON, pandas |
| Logging | Loguru |
| Testing | pytest, pytest-asyncio, pytest-cov |
| Quality | black, isort, flake8, mypy |
| Config | python-dotenv |

## Future Architecture Enhancements

1. **Caching Layer**: Redis for API response caching
2. **Queue System**: Celery for async job processing
3. **Database**: PostgreSQL for data persistence
4. **API Gateway**: REST API for web interface
5. **Web Dashboard**: React frontend for visualization
6. **Message Queue**: RabbitMQ for job distribution
7. **Container Orchestration**: Kubernetes for scaling

---

This architecture provides a solid foundation for a production-ready LinkedIn scraping system with clean separation of concerns, robust error handling, and easy extensibility.


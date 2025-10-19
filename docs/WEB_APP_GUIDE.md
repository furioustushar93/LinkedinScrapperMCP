# 🌐 Web Application Guide

Your LinkedIn Scraper now has a **beautiful web interface** with a FastAPI backend!

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (Browser)                  │
│              Modern UI with Tabs & Forms             │
└────────────────────┬────────────────────────────────┘
                     │ HTTP REST API
                     │
┌────────────────────▼────────────────────────────────┐
│              FastAPI Backend                         │
│         (backend/main.py)                           │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│          LinkedIn Scraper Core                       │
│         (src/scraper.py)                            │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              LinkedIn API                            │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp
source venv/bin/activate
pip install fastapi uvicorn pydantic
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file has:
```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

### 3. Start the Server

```bash
python backend/main.py
```

Or use uvicorn directly:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

- **🌐 Web Interface**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs
- **📊 Alternative API Docs**: http://localhost:8000/redoc

---

## 🎨 Features

### Frontend Features

1. **Beautiful Modern UI**
   - Gradient design
   - Smooth animations
   - Responsive layout
   - Tab-based navigation

2. **Four Main Functions**
   - 💼 Job Search
   - 👤 Profile Scraping
   - 🏢 Company Information
   - 👥 People Search

3. **User Experience**
   - Real-time loading indicators
   - Error handling
   - Clean result display
   - Mobile-friendly

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/health` | GET | Health check |
| `/api/jobs/search` | POST | Search jobs |
| `/api/profile/scrape` | POST | Scrape profile |
| `/api/company/info` | POST | Get company info |
| `/api/people/search` | POST | Search people |
| `/docs` | GET | API documentation |

---

## 📝 API Usage Examples

### 1. Search Jobs

**Request:**
```bash
curl -X POST http://localhost:8000/api/jobs/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Python Developer",
    "location": "San Francisco, CA",
    "limit": 10
  }'
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "jobs": [
    {
      "job_id": "12345",
      "title": "Senior Python Developer",
      "company": "Google",
      "location": "San Francisco, CA",
      "description": "Build scalable systems...",
      "posted_at": "2024-10-15",
      "job_url": "https://linkedin.com/jobs/view/12345"
    }
  ]
}
```

### 2. Scrape Profile

**Request:**
```bash
curl -X POST http://localhost:8000/api/profile/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "profile_url": "https://linkedin.com/in/example"
  }'
```

### 3. Get Company Info

**Request:**
```bash
curl -X POST http://localhost:8000/api/company/info \
  -H "Content-Type: application/json" \
  -d '{
    "company_identifier": "google"
  }'
```

### 4. Search People

**Request:**
```bash
curl -X POST http://localhost:8000/api/people/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Machine Learning Engineer",
    "location": "New York, NY",
    "limit": 10
  }'
```

---

## 🎨 Using the Web Interface

### Job Search Tab

1. Enter keywords (e.g., "Python Developer")
2. Optionally add location
3. Select number of results
4. Click "Search Jobs"
5. View results with:
   - Job title
   - Company name
   - Location
   - Posted date
   - Description snippet
   - Apply link

### Profile Scrape Tab

1. Enter LinkedIn profile URL
2. Click "Scrape Profile"
3. View profile information:
   - Name
   - Headline
   - Location
   - Summary
   - Profile link

### Company Info Tab

1. Enter company name or ID
2. Click "Get Company Info"
3. View company details:
   - Company name
   - Industry
   - Size
   - Location
   - Website
   - Description

### People Search Tab

1. Enter keywords
2. Optionally add location
3. Select number of results
4. Click "Search People"
5. View profiles found

---

## 🔧 Development

### Project Structure

```
mcp/
├── backend/
│   └── main.py              # FastAPI backend
│
├── frontend/
│   └── templates/
│       └── index.html       # Web interface
│
├── src/                     # Core scraper (unchanged)
│   ├── scraper.py
│   ├── utils.py
│   └── server.py            # MCP server (still works!)
│
└── requirements.txt         # All dependencies
```

### Adding New Endpoints

```python
# In backend/main.py

@app.post("/api/your-endpoint")
async def your_function(request: YourRequest):
    try:
        scraper_instance = get_scraper()
        result = scraper_instance.your_method()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Hot Reload

The backend runs with `--reload` flag, so changes are auto-detected:
```bash
uvicorn backend.main:app --reload
```

---

## 🌐 Deployment

### Local Development
```bash
python backend/main.py
# Access at http://localhost:8000
```

### Production (Basic)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Production (With Gunicorn)
```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (Future)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔒 Security Considerations

### Current Setup (Development)
- CORS allows all origins
- No authentication
- Direct LinkedIn credentials

### Production Recommendations
1. **Add Authentication**
   - JWT tokens
   - OAuth2
   - API keys

2. **Restrict CORS**
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

3. **Environment Variables**
   - Never commit `.env`
   - Use secrets manager in production

4. **Rate Limiting**
   ```python
   from fastapi_limiter import FastAPILimiter
   ```

5. **HTTPS Only**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

---

## 📊 Monitoring & Logs

### View Logs
```bash
# Backend logs
tail -f logs/linkedin_scraper.log

# Uvicorn logs
# Printed to console by default
```

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "LinkedIn Scraper API",
  "version": "1.0.0"
}
```

---

## 🎯 Use Cases

### 1. Job Board Integration
Integrate job search API into your own job board

### 2. Recruitment Tool
Build a recruitment dashboard for finding candidates

### 3. Company Research
Automated company information gathering

### 4. Network Analysis
Map professional networks and connections

### 5. Market Research
Analyze job market trends and salary data

---

## 🚀 Next Steps

### Enhancements You Can Add

1. **User Authentication**
   - Login system
   - User-specific history
   - Saved searches

2. **Database Integration**
   - Store search results
   - Cache data
   - Historical tracking

3. **Advanced Features**
   - Export to CSV/Excel
   - Email alerts
   - Scheduled searches
   - Data visualization

4. **Mobile App**
   - React Native frontend
   - Same FastAPI backend

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn backend.main:app --port 8001
```

### Import Errors
```bash
# Make sure you're in project root
cd /Users/tusharaggarwal/Documents/Self-Learning/mcp

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Not Loading
- Check browser console for errors
- Ensure backend is running
- Try different browser

### API Errors
- Check logs: `logs/linkedin_scraper.log`
- Verify LinkedIn credentials in `.env`
- Check API documentation: `/docs`

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [REST API Best Practices](https://restfulapi.net/)

---

## 🎉 Summary

You now have:
- ✅ **FastAPI Backend** - RESTful API for all scraping functions
- ✅ **Modern Web Frontend** - Beautiful, responsive UI
- ✅ **Backward Compatible** - MCP server and Gemini client still work
- ✅ **Production Ready** - Error handling, logging, documentation
- ✅ **Easy to Extend** - Add new features easily

**Start the server:**
```bash
python backend/main.py
```

**Then visit:** http://localhost:8000

Enjoy your new web interface! 🚀


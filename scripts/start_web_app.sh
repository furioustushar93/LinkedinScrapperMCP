#!/bin/bash
# Start LinkedIn Scraper Web Application

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              LinkedIn Scraper - Web Application                              ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv"
    echo "        source venv/bin/activate"
    echo "        pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Copy .env.example to .env and add your credentials"
fi

# Install FastAPI dependencies if needed
echo "📦 Checking dependencies..."
pip install -q fastapi uvicorn pydantic 2>/dev/null

# Start the server
echo ""
echo "🚀 Starting FastAPI server..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🌐 Web Interface:    http://localhost:8000"
echo "  📖 API Docs:         http://localhost:8000/docs"
echo "  📊 Alternative Docs: http://localhost:8000/redoc"
echo "  ❤️  Health Check:     http://localhost:8000/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start uvicorn
python backend/main.py

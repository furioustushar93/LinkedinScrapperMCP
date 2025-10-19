#!/bin/bash
# Installation script for LinkedIn Scraper MCP Server

set -e

echo "=================================="
echo "LinkedIn Scraper MCP Server Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your LinkedIn credentials"
    echo "   Run: nano .env"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create logs directory
mkdir -p logs
echo "✓ Logs directory created"
echo ""

# Run tests
echo "Running tests..."
pytest tests/ -v || echo "⚠️  Some tests failed (this is expected without valid credentials)"
echo ""

echo "=================================="
echo "Installation complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the example:"
echo "   python examples/example_usage.py"
echo ""
echo "4. Start the MCP server:"
echo "   python src/server.py"
echo ""
echo "5. Configure in Claude Desktop:"
echo "   Add server config to: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "For more information, see README.md"
echo ""


#!/bin/bash
# setup.sh - First-time setup for macOS and Linux users
# Run with: bash setup.sh

set -e  # Exit on any error

echo ""
echo "Player Care AI - Setup"
echo "======================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo ""
    echo "macOS: Install from https://www.python.org/downloads/ or run: brew install python"
    echo "Linux: Run: sudo apt-get install python3 python3-venv python3-pip"
    echo ""
    exit 1
fi

PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PYVER"

# Check minimum version
PYMAJOR=$(echo $PYVER | cut -d. -f1)
PYMINOR=$(echo $PYVER | cut -d. -f2)
if [ "$PYMAJOR" -lt 3 ] || ([ "$PYMAJOR" -eq 3 ] && [ "$PYMINOR" -lt 10 ]); then
    echo "ERROR: Python 3.10 or higher is required. Found: $PYVER"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created."

# Install dependencies
echo ""
echo "Installing dependencies (this may take 2-5 minutes)..."
echo "Note: sentence-transformers will download an ~80MB model on first use. This is normal."
venv/bin/pip install --upgrade pip --quiet
venv/bin/pip install -r requirements.txt
echo "Dependencies installed."

# Copy .env.example if .env does not exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo ".env file created from .env.example"
    echo "IMPORTANT: Edit .env and add your API keys before continuing."
else
    echo ".env already exists - skipping."
fi

echo ""
echo "================================================"
echo "Setup complete!"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "   Get your key at: https://console.anthropic.com"
echo ""
echo "2. Activate the virtual environment:"
echo "   Run: source venv/bin/activate"
echo "   Your prompt will change to show (venv)"
echo ""
echo "3. Sync the knowledge base:"
echo "   Run: python rag/kb_sync.py"
echo "   Note: First run downloads ~80MB model. May take 1-2 minutes. This is normal."
echo ""
echo "4. Run the example:"
echo "   Run: python example_run.py"
echo ""
echo "IMPORTANT: You must run 'source venv/bin/activate' every time you open"
echo "a new terminal window before running any python commands."
echo "================================================"
echo ""

#!/bin/bash

# Phishing Shield - Quick Start Script for Mac/Linux

echo ""
echo "==========================================="
echo "  Phishing Shield - Quick Start"
echo "==========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found! Please install Python 3.8+"
    echo "   Mac: brew install python3"
    echo "   Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Run model test
echo ""
echo "🧪 Testing ML Model..."
python model.py
if [ $? -ne 0 ]; then
    echo "❌ Model test failed"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""
echo "🚀 Starting Phishing Shield API Server..."
echo "   Server will run on: http://localhost:5001"
echo ""
echo "Instructions:"
echo " 1. Open Chrome and go to: chrome://extensions/"
echo " 2. Enable 'Developer mode'"
echo " 3. Click 'Load unpacked'"
echo " 4. Select the 'extension' folder"
echo " 5. Click the extension icon to test"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask app
python app.py

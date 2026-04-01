#!/usr/bin/env python3
"""
Phishing Shield - Verification Script
Verify all components are working correctly
"""

import os
import json
import sys

def check_file_exists(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ {description}: {path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {path} (NOT FOUND)")
        return False

def check_directory_exists(path, description):
    """Check if a directory exists"""
    if os.path.isdir(path):
        files = len(os.listdir(path))
        print(f"✅ {description}: {path} ({files} items)")
        return True
    else:
        print(f"❌ {description}: {path} (NOT FOUND)")
        return False

def main():
    """Main verification function"""
    print("\n" + "="*60)
    print("🛡️  PHISHING SHIELD - SYSTEM VERIFICATION")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Check Backend Files
    print("📦 Backend Files:")
    all_ok &= check_file_exists("app.py", "Flask API")
    all_ok &= check_file_exists("model.py", "ML Model")
    all_ok &= check_file_exists("requirements.txt", "Dependencies")
    print()
    
    # Check Extension Files
    print("🔧 Extension Files:")
    all_ok &= check_directory_exists("extension", "Extension Directory")
    all_ok &= check_file_exists("extension/manifest.json", "Manifest")
    all_ok &= check_file_exists("extension/popup.html", "Popup HTML")
    all_ok &= check_file_exists("extension/popup.css", "Popup CSS")
    all_ok &= check_file_exists("extension/popup.js", "Popup JS")
    all_ok &= check_file_exists("extension/background.js", "Background Worker")
    all_ok &= check_file_exists("extension/settings.html", "Settings Page")
    print()
    
    # Check Landing Page
    print("🌐 Landing Page:")
    all_ok &= check_directory_exists("landing", "Landing Directory")
    all_ok &= check_file_exists("landing/index.html", "Homepage")
    print()
    
    # Check Documentation
    print("📚 Documentation:")
    all_ok &= check_file_exists("README.md", "Main Instructions")
    all_ok &= check_file_exists("TESTING.md", "Testing Guide")
    all_ok &= check_file_exists("DEPLOYMENT.md", "Deployment Guide")
    all_ok &= check_file_exists("API.md", "API Documentation")
    all_ok &= check_file_exists("COMPLETION_SUMMARY.md", "Completion Summary")
    print()
    
    # Check Quick Start Scripts
    print("⚡ Quick Start Scripts:")
    all_ok &= check_file_exists("start.bat", "Windows Starter")
    all_ok &= check_file_exists("start.sh", "Mac/Linux Starter")
    print()
    
    # Check Model
    print("🤖 ML Model:")
    if os.path.exists("phishing_model.pkl"):
        size = os.path.getsize("phishing_model.pkl")
        print(f"✅ Trained Model: phishing_model.pkl ({size:,} bytes)")
    else:
        print(f"⚠️  Model not found (will auto-train on first run)")
    print()
    
    # Summary
    print("="*60)
    if all_ok:
        print("✅ ALL SYSTEMS READY")
        print("\n🚀 Next Steps:")
        print("1. Windows: Double-click start.bat")
        print("2. Mac/Linux: Run ./start.sh")
        print("3. Or manually: python app.py")
        print("4. Then load extension in Chrome")
        print("\n📖 See README.md for detailed instructions")
    else:
        print("❌ MISSING FILES - Please check above")
    print("="*60 + "\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

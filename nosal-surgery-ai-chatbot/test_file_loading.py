#!/usr/bin/env python3
"""
Test script to check HTML file loading in different environments
"""

import os
import sys

def test_file_loading():
    """Test different ways to load the HTML file"""
    print("🔍 Testing HTML file loading...")
    print("=" * 50)
    
    # Test different possible paths
    possible_paths = [
        "meko_clinic_rhinoplasty.html",
        "./meko_clinic_rhinoplasty.html",
        os.path.join(os.getcwd(), "meko_clinic_rhinoplasty.html"),
        os.path.join(os.path.dirname(__file__), "meko_clinic_rhinoplasty.html")
    ]
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(__file__)}")
    print()
    
    # List all files in current directory
    print("📁 Files in current directory:")
    try:
        files = os.listdir(".")
        html_files = [f for f in files if f.endswith('.html')]
        for file in files[:10]:  # Show first 10 files
            print(f"  - {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
        print()
    except Exception as e:
        print(f"  ❌ Error listing directory: {e}")
        print()
    
    # Test each possible path
    html_content = None
    used_path = None
    
    for i, path in enumerate(possible_paths, 1):
        print(f"🔍 Test {i}: {path}")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    print(f"  ✅ File exists and readable")
                    print(f"  📏 File size: {len(content):,} characters")
                    html_content = content
                    used_path = path
                    break
            else:
                print(f"  ❌ File does not exist")
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
        print()
    
    if not html_content:
        print("🔍 Trying to find any HTML file...")
        try:
            current_dir = os.getcwd()
            files = os.listdir(current_dir)
            html_files = [f for f in files if f.endswith('.html')]
            
            if html_files:
                html_file_path = os.path.join(current_dir, html_files[0])
                print(f"  📄 Found HTML file: {html_files[0]}")
                with open(html_file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                    used_path = html_file_path
                    print(f"  ✅ Successfully loaded: {html_files[0]}")
                    print(f"  📏 File size: {len(html_content):,} characters")
            else:
                print("  ❌ No HTML files found in current directory")
        except Exception as e:
            print(f"  ❌ Error searching for HTML files: {e}")
        print()
    
    # Summary
    print("=" * 50)
    if html_content:
        print(f"✅ SUCCESS: HTML content loaded from: {used_path}")
        print(f"📏 Content length: {len(html_content):,} characters")
        
        # Check if content looks like HTML
        if "<html" in html_content.lower() or "<body" in html_content.lower():
            print("✅ Content appears to be valid HTML")
        else:
            print("⚠️  Content doesn't appear to be HTML")
    else:
        print("❌ FAILED: Could not load HTML content")
        print("💡 This might cause issues in Streamlit Cloud deployment")
    
    return html_content is not None

if __name__ == "__main__":
    success = test_file_loading()
    sys.exit(0 if success else 1) 
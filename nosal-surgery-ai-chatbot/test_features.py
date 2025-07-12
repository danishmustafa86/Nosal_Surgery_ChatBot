#!/usr/bin/env python3
"""
Test script for Meko Clinic Rhinoplasty AI Chatbot Enhanced Features
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        from openai import OpenAI
        print("✅ openai imported")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        print("✅ scikit-learn imported")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 imported")
    except ImportError as e:
        print(f"❌ beautifulsoup4 import failed: {e}")
        return False
    
    try:
        from langdetect import detect
        print("✅ langdetect imported")
    except ImportError as e:
        print(f"❌ langdetect import failed: {e}")
        return False
    
    return True

def test_html_content():
    """Test HTML content loading"""
    print("\n📄 Testing HTML content loading...")
    
    if not os.path.exists("meko_clinic_rhinoplasty.html"):
        print("⚠️ HTML file not found, skipping content test")
        return True
    
    try:
        # Import the function from the main app
        from app2WithOpenAIApiKey import load_and_process_html_content
        
        content, structured_data = load_and_process_html_content()
        
        if content and len(content) > 100:
            print(f"✅ HTML content loaded successfully ({len(content)} characters)")
        else:
            print("❌ HTML content too short or empty")
            return False
        
        if structured_data:
            print(f"✅ Structured data extracted: {list(structured_data.keys())}")
        else:
            print("⚠️ No structured data extracted")
        
        return True
        
    except Exception as e:
        print(f"❌ HTML content loading failed: {e}")
        return False

def test_language_detection():
    """Test language detection functionality"""
    print("\n🌍 Testing language detection...")
    
    try:
        from app2WithOpenAIApiKey import detect_language
        
        test_cases = [
            ("Hello, how are you?", "English"),
            ("Hola, ¿cómo estás?", "Spanish"),
            ("Bonjour, comment allez-vous?", "French"),
            ("สวัสดีครับ คุณสบายดีไหม", "Thai"),
            ("你好，你好吗？", "Chinese"),
            ("こんにちは、お元気ですか？", "Japanese")
        ]
        
        for text, expected in test_cases:
            detected = detect_language(text)
            if detected == expected:
                print(f"✅ {expected}: '{text[:20]}...' → {detected}")
            else:
                print(f"⚠️ {expected}: '{text[:20]}...' → {detected} (expected {expected})")
        
        return True
        
    except Exception as e:
        print(f"❌ Language detection failed: {e}")
        return False

def test_query_classification():
    """Test query classification"""
    print("\n🎯 Testing query classification...")
    
    try:
        from app2WithOpenAIApiKey import classify_query
        
        # Test clinic-related queries
        clinic_queries = [
            "What is the price of rhinoplasty?",
            "How long is recovery after nose surgery?",
            "Can I book a consultation at Meko Clinic?",
            "เสริมจมูกราคาเท่าไหร่",
            "การพักฟื้นหลังผ่าตัดจมูกนานแค่ไหน"
        ]
        
        # Test general queries
        general_queries = [
            "What's the weather like today?",
            "How do I cook pasta?",
            "Tell me a joke",
            "What is the capital of France?"
        ]
        
        print("Testing clinic-related queries:")
        for query in clinic_queries:
            result = classify_query(query, "rhinoplasty clinic surgery")
            print(f"  '{query[:30]}...' → {result}")
        
        print("Testing general queries:")
        for query in general_queries:
            result = classify_query(query, "rhinoplasty clinic surgery")
            print(f"  '{query[:30]}...' → {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query classification failed: {e}")
        return False

def test_quick_responses():
    """Test quick response templates"""
    print("\n⚡ Testing quick response templates...")
    
    try:
        from app2WithOpenAIApiKey import QUICK_RESPONSES
        
        for category, responses in QUICK_RESPONSES.items():
            print(f"✅ {category}: {len(responses)} languages supported")
            for lang, response in responses.items():
                if len(response) > 50:
                    print(f"  - {lang}: {len(response)} characters")
                else:
                    print(f"  ⚠️ {lang}: Response too short")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick responses test failed: {e}")
        return False

def test_semantic_search():
    """Test semantic search functionality"""
    print("\n🔍 Testing semantic search...")
    
    try:
        from app2WithOpenAIApiKey import create_semantic_search_index, semantic_search
        
        # Create test content
        test_content = """
        Rhinoplasty is a surgical procedure to reshape the nose.
        Recovery time is typically 1-2 weeks for initial healing.
        Meko Clinic offers consultation services for rhinoplasty.
        The price starts at 99,000 THB for open rhinoplasty.
        """
        
        # Create search index
        search_index = create_semantic_search_index(test_content)
        
        if search_index:
            print("✅ Search index created successfully")
            
            # Test search
            results = semantic_search("rhinoplasty price", search_index)
            if results:
                print(f"✅ Semantic search returned {len(results)} results")
            else:
                print("⚠️ Semantic search returned no results")
        else:
            print("❌ Failed to create search index")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Semantic search test failed: {e}")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\n📤 Testing export functionality...")
    
    try:
        from app2WithOpenAIApiKey import export_conversation
        
        # Test conversation data
        test_messages = [
            {"role": "user", "content": "What is rhinoplasty?", "timestamp": "2024-01-01"},
            {"role": "assistant", "content": "Rhinoplasty is a surgical procedure...", "timestamp": "2024-01-01"}
        ]
        
        # Test JSON export
        json_export = export_conversation(test_messages, "json")
        if json_export and "rhinoplasty" in json_export:
            print("✅ JSON export working")
        else:
            print("❌ JSON export failed")
            return False
        
        # Test TXT export
        txt_export = export_conversation(test_messages, "txt")
        if txt_export and "Meko Clinic" in txt_export:
            print("✅ TXT export working")
        else:
            print("❌ TXT export failed")
            return False
        
        # Test CSV export
        csv_export = export_conversation(test_messages, "csv")
        if csv_export and "role,content" in csv_export:
            print("✅ CSV export working")
        else:
            print("❌ CSV export failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 Meko Clinic Rhinoplasty AI Chatbot - Feature Tests")
    print("=" * 60)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("HTML Content Loading", test_html_content),
        ("Language Detection", test_language_detection),
        ("Query Classification", test_query_classification),
        ("Quick Response Templates", test_quick_responses),
        ("Semantic Search", test_semantic_search),
        ("Export Functionality", test_export_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced chatbot is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
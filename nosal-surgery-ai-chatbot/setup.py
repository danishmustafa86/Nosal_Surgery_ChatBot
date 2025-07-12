#!/usr/bin/env python3
"""
Setup script for Meko Clinic Rhinoplasty AI Chatbot
Enhanced version with advanced features
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🚀 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    print("\n🔑 Checking OpenAI API key...")
    
    # Check environment variable
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found in environment variables")
        return True
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file found")
        return True
    
    print("⚠️  OpenAI API key not found!")
    print("Please set your OpenAI API key in one of these ways:")
    print("1. Create a .env file with: OPENAI_API_KEY=your_key_here")
    print("2. Set environment variable: export OPENAI_API_KEY=your_key_here")
    print("3. Add to Streamlit secrets: st.secrets['OPENAI_API_KEY']")
    return False

def create_env_template():
    """Create .env template file"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# OpenAI API Key\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Optional: Other configuration\n")
            f.write("# MODEL_NAME=gpt-4\n")
            f.write("# MAX_TOKENS=1200\n")
        print("📝 Created .env template file")
        print("Please edit .env and add your OpenAI API key")

def main():
    """Main setup function"""
    print("🏥 Meko Clinic Rhinoplasty AI Chatbot Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed! Please check the error messages above.")
        return
    
    # Create .env template
    create_env_template()
    
    # Check API key
    check_openai_key()
    
    print("\n🎉 Setup completed!")
    print("\nTo run the chatbot:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run: streamlit run app2WithOpenAIApiKey.py")
    print("\nFeatures included:")
    print("✅ Multilingual support (15+ languages)")
    print("✅ Voice input/output")
    print("✅ Smart semantic search")
    print("✅ Quick response templates")
    print("✅ Conversation analytics")
    print("✅ Export functionality")
    print("✅ Enhanced accuracy based on clinic data")

if __name__ == "__main__":
    main() 
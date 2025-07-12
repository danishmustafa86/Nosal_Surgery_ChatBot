import streamlit as st
import os
from openai import OpenAI

def test_secrets():
    """Test if secrets are properly configured"""
    st.title("🔐 Secrets Configuration Test")
    
    # Test environment variable
    env_key = os.getenv("OPENAI_API_KEY")
    st.write(f"**Environment Variable:** {'✅ Set' if env_key else '❌ Not Set'}")
    
    # Test Streamlit secrets
    try:
        secrets_key = st.secrets.get("OPENAI_API_KEY", "")
        st.write(f"**Streamlit Secrets:** {'✅ Set' if secrets_key else '❌ Not Set'}")
    except Exception as e:
        st.write(f"**Streamlit Secrets:** ❌ Error - {str(e)}")
    
    # Test OpenAI client initialization
    try:
        client = OpenAI(api_key=env_key or secrets_key)
        st.success("✅ OpenAI client initialized successfully!")
        
        # Test a simple API call
        response = client.models.list()
        st.success("✅ OpenAI API connection successful!")
        st.write(f"Available models: {len(response.data)} models")
        
    except Exception as e:
        st.error(f"❌ OpenAI client error: {str(e)}")
    
    # Show configuration tips
    st.markdown("---")
    st.markdown("### 📋 Configuration Tips")
    st.markdown("""
    **For Local Development:**
    - Create `.streamlit/secrets.toml` with your API key
    - Add `.streamlit/secrets.toml` to `.gitignore`
    
    **For Streamlit Cloud:**
    - Go to app settings → Secrets
    - Add: `OPENAI_API_KEY = "your-key-here"`
    
    **API Key Format:**
    - Should start with `sk-`
    - Example: `sk-1234567890abcdef...`
    """)

if __name__ == "__main__":
    test_secrets() 
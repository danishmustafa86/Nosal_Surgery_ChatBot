# 🔑 OpenAI API Key Setup Guide

## The Problem
Your `app.py` chatbot is getting a 401 error because it can't find your OpenAI API key, even though your `test.py` works. This is because:

1. **Different client versions**: `app.py` uses the newer OpenAI client (v1+) while your old `test.py` used the older client (v0.x)
2. **Different API key loading**: `app.py` looks for the key in environment variables, while your old `test.py` had the key hardcoded

## ✅ Quick Fix

### Option 1: Use the Setup Script (Recommended)
```bash
poetry run python setup_env.py
```
This will:
- Ask for your API key
- Create a `.env` file
- Create `.streamlit/secrets.toml`
- Test the connection

### Option 2: Manual Setup

#### Step 1: Create a `.env` file
Create a file named `.env` in your project directory:
```
OPENAI_API_KEY=your-actual-api-key-here
```

#### Step 2: Create Streamlit secrets (optional)
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-actual-api-key-here"
```

### Option 3: Environment Variable
```bash
export OPENAI_API_KEY=your-actual-api-key-here
```

## 🧪 Test Your Setup

After setting up, test with:
```bash
poetry run python test.py
```

You should see:
```
✅ API key is valid! Models available:
- gpt-4-0613
- gpt-4
- gpt-3.5-turbo
...
```

## 🚀 Run the Chatbot

Now you can run your chatbot:
```bash
poetry run streamlit run app.py
```

## 🔧 What Changed

1. **Updated `app.py`**: Now has better error handling and will show a temporary input field if no API key is found
2. **Updated `test.py`**: Now uses the same client format as `app.py`
3. **Created `setup_env.py`**: Automated setup script
4. **Created this guide**: Step-by-step instructions

## 🛠️ Troubleshooting

If you still get errors:

1. **Check API key format**: Should start with `sk-`
2. **Check API key validity**: Make sure it's not expired
3. **Check internet connection**: Make sure you can reach OpenAI
4. **Check file permissions**: Make sure `.env` file is readable

## 📝 File Structure After Setup

```
nosal-surgery-ai-chatbot/
├── .env                          # Your API key (created by setup)
├── .streamlit/
│   └── secrets.toml             # Streamlit secrets (created by setup)
├── app.py                       # Main chatbot (updated)
├── test.py                      # Test script (updated)
├── setup_env.py                 # Setup script (new)
└── API_KEY_SETUP.md            # This guide (new)
``` 
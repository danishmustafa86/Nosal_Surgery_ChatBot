# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- OpenAI API key
- Streamlit Cloud account

## Step 1: Prepare Your Repository

### ✅ Files Required for Deployment:
- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `meko_clinic_rhinoplasty.html` - Clinic content
- `README.md` - Project documentation

### ✅ Files NOT to include:
- `.streamlit/secrets.toml` - Contains local API keys
- `.env` - Environment variables
- `poetry.lock` - Poetry lock file (not needed for Streamlit Cloud)
- `packages.txt` - System dependencies (not needed)

## Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app:**
   - **Repository:** Select your GitHub repo
   - **Branch:** `main` or `master`
   - **Main file path:** `app.py`
   - **Python version:** 3.11 (recommended)

## Step 3: Add Secrets

**After deployment, add your API key:**

1. **Go to app settings** (gear icon)
2. **Scroll to "Secrets" section**
3. **Add this configuration:**

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

## Step 4: Deploy and Test

1. **Click "Deploy"**
2. **Wait for build to complete**
3. **Test your app**

## Troubleshooting

### Common Issues:

#### ❌ Dependency Installation Errors
- **Solution:** Check `requirements.txt` has correct versions
- **Fix:** Update package versions if needed
- **Note:** PyAudio and SpeechRecognition removed for Streamlit Cloud compatibility

#### ❌ Audio Recording Not Working
- **Solution:** Uses web-based audio recording (audio-recorder-streamlit)
- **Fix:** No system dependencies required
- **Note:** Voice features use OpenAI Whisper and TTS APIs

#### ❌ API Key Errors
- **Solution:** Verify secrets are added in Streamlit Cloud
- **Fix:** Check API key format and permissions

#### ❌ Memory/Timeout Issues
- **Solution:** Optimize code for Streamlit Cloud limits
- **Fix:** Reduce token usage, optimize imports

## Environment Variables

### Local Development:
```bash
# Create .env file
OPENAI_API_KEY=your-key-here
```

### Streamlit Cloud:
```toml
# Add in Streamlit Cloud secrets
OPENAI_API_KEY = "your-key-here"
```

## Audio Features

### ✅ Supported:
- **Voice Input:** Web-based audio recording
- **Voice Output:** OpenAI TTS-1-HD
- **Transcription:** OpenAI Whisper
- **No System Dependencies:** All audio processing via APIs

### ❌ Not Supported:
- **Local Audio Processing:** PyAudio, SpeechRecognition
- **System Audio Libraries:** PortAudio, etc.

## Best Practices

1. **Never commit API keys** to Git
2. **Use version pinning** in requirements.txt
3. **Test locally** before deploying
4. **Monitor app performance** after deployment
5. **Keep dependencies minimal** for faster deployment
6. **Use web-based alternatives** for audio processing

## Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all required files are present
3. Test with minimal dependencies first
4. Contact Streamlit support if needed

## Recent Changes

### Audio Dependencies Removed:
- ❌ `pyaudio` - Required system libraries
- ❌ `SpeechRecognition` - Required system libraries
- ❌ `packages.txt` - System dependencies file

### Audio Features Maintained:
- ✅ `audio-recorder-streamlit` - Web-based recording
- ✅ OpenAI Whisper - Cloud transcription
- ✅ OpenAI TTS - Cloud speech synthesis 
# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- OpenAI API key
- Streamlit Cloud account

## Step 1: Prepare Your Repository

### ✅ Files Required for Deployment:
- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies (for audio)
- `.streamlit/config.toml` - Streamlit configuration
- `meko_clinic_rhinoplasty.html` - Clinic content
- `README.md` - Project documentation

### ✅ Files NOT to include:
- `.streamlit/secrets.toml` - Contains local API keys
- `.env` - Environment variables
- `poetry.lock` - Poetry lock file (not needed for Streamlit Cloud)

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

#### ❌ Audio Recording Not Working
- **Solution:** Ensure `packages.txt` includes audio dependencies
- **Fix:** Add `portaudio19-dev` and `ffmpeg`

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

## Best Practices

1. **Never commit API keys** to Git
2. **Use version pinning** in requirements.txt
3. **Test locally** before deploying
4. **Monitor app performance** after deployment
5. **Keep dependencies minimal** for faster deployment

## Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all required files are present
3. Test with minimal dependencies first
4. Contact Streamlit support if needed 
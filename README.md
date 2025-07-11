# Nosal Surgery AI Chatbot

A specialized AI chatbot designed to provide information and assistance related to nasal surgery procedures.

## Description

This Streamlit-based application uses OpenAI's API to provide conversational AI assistance for nasal surgery related queries. The chatbot can help answer questions about procedures, recovery, and general information.

## Features

- Interactive chat interface
- AI-powered responses using OpenAI
- Web scraping capabilities for additional information
- Multi-language detection support
- HTML content processing

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install streamlit openai beautifulsoup4 langdetect html2text
   ```
3. Set up your OpenAI API key in Streamlit secrets
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Configuration

Add your OpenAI API key to Streamlit secrets:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

## Requirements

- Python >= 3.11
- Streamlit >= 1.46.1
- OpenAI >= 1.95.1
- Beautiful Soup 4
- langdetect
- html2text

## Author

Danish Mustafa (danishjajja86@gmail.com)
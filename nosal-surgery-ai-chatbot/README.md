# 🏥 Meko Clinic Rhinoplasty AI Chatbot

An advanced AI-powered chatbot specifically designed for Meko Clinic's rhinoplasty services, featuring multilingual support, voice interaction, and intelligent content retrieval.

## ✨ Enhanced Features

### 🎯 **Smart Query Classification**
- Automatically detects if queries are clinic-related or general
- Provides accurate responses based on Meko Clinic data
- Falls back to general AI responses for non-clinic queries

### 🔍 **Semantic Search & Content Retrieval**
- Advanced TF-IDF based semantic search within clinic content
- Intelligent content selection based on user queries
- Enhanced accuracy by using relevant clinic information

### 💬 **Quick Response Templates**
- Instant responses for common questions (pricing, consultation, recovery, contact)
- Available in multiple languages
- Reduces response time for frequently asked questions

### 🌍 **Multilingual Support (15+ Languages)**
- **Full Support:** English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Urdu, Turkish, Thai
- **Features:** Native script support, cultural context awareness, voice input/output

### 🎙️ **Voice Interaction**
- Voice input with Whisper transcription
- High-quality TTS-1-HD speech synthesis
- Multiple voice options per language

### 📊 **Analytics Dashboard**
- Real-time conversation analytics
- Query classification tracking
- Response time monitoring
- Language usage statistics

### 📤 **Export Functionality**
- Export conversations in JSON, TXT, or CSV formats
- Timestamped files for easy organization
- Complete conversation history preservation

### 🔄 **Conversation Memory**
- Maintains context across conversations
- Smart conversation history management
- Enhanced response relevance

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd nosal-surgery-ai-chatbot

# Run setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

```bash
streamlit run app2WithOpenAIApiKey.py
```

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

### Key Dependencies

- `streamlit>=1.28.0` - Web interface
- `openai>=1.54.0` - AI model integration
- `scikit-learn>=1.3.0` - Semantic search
- `pandas>=2.0.0` - Data processing
- `numpy>=1.24.0` - Numerical operations
- `audio_recorder_streamlit>=0.1.6` - Voice recording
- `beautifulsoup4>=4.12.0` - HTML parsing
- `langdetect>=1.0.9` - Language detection

## 🎮 Usage Guide

### Quick Actions
Use the sidebar quick action buttons for instant responses:
- **💰 Pricing** - Get pricing information
- **📋 Consultation** - Book consultation details
- **🩹 Recovery** - Recovery timeline and care
- **📞 Contact** - Contact information

### Voice Input
1. Enable voice features in the sidebar
2. Click the microphone button
3. Speak your question
4. Get transcribed text and AI response
5. Optionally play audio response

### Text Input
1. Type your question in the chat input
2. Get instant response with clinic-specific information
3. Use any supported language

### Export Conversations
1. Go to sidebar → Export Options
2. Select format (JSON/TXT/CSV)
3. Click "Export Conversation"
4. Download the file

## 🏗️ Architecture

### Core Components

1. **Content Processor** (`load_and_process_html_content`)
   - Extracts structured data from HTML
   - Identifies pricing, contact, and procedure information
   - Creates searchable content chunks

2. **Query Classifier** (`classify_query`)
   - Determines if query is clinic-related
   - Routes to appropriate response system
   - Maintains accuracy boundaries

3. **Semantic Search** (`semantic_search`)
   - TF-IDF vectorization of content
   - Cosine similarity matching
   - Intelligent content retrieval

4. **Response Generator** (`generate_response`)
   - Context-aware response generation
   - Multi-language support
   - Conversation memory integration

5. **Analytics Engine**
   - Real-time usage tracking
   - Performance monitoring
   - User behavior analysis

### Data Flow

```
User Input → Language Detection → Query Classification → Content Retrieval → Response Generation → Analytics Update
```

## 🎯 Accuracy Features

### Clinic-Specific Responses
- **Primary Source:** Meko Clinic HTML content
- **Structured Data:** Extracted pricing, procedures, contact info
- **Semantic Matching:** Intelligent content selection
- **Fallback System:** General AI for non-clinic queries

### Quality Assurance
- **Response Validation:** Ensures clinic information accuracy
- **Source Attribution:** Clearly indicates information sources
- **Medical Disclaimer:** Appropriate medical advice disclaimers
- **Context Preservation:** Maintains conversation relevance

## 📈 Analytics & Monitoring

### Real-Time Metrics
- Total queries processed
- Clinic vs general query ratio
- Voice vs text input usage
- Average response times
- Language distribution

### Performance Tracking
- Response time monitoring
- Error rate tracking
- User satisfaction metrics
- Feature usage statistics

## 🔧 Configuration Options

### Model Settings
- **AI Model:** GPT-4 (configurable)
- **Temperature:** 0.7 (balanced creativity/accuracy)
- **Max Tokens:** 1200 (optimized for clinic responses)
- **Voice Model:** TTS-1-HD (high quality)

### Language Settings
- **Auto-detection:** Enabled by default
- **Manual Override:** Available for specific languages
- **Voice Selection:** Optimized per language

## 🛠️ Customization

### Adding New Languages
1. Add language to `LANGUAGES` dictionary
2. Include voice mapping
3. Add to `LANG_DETECT_MAP`
4. Create quick response templates

### Extending Quick Responses
1. Add new category to `QUICK_RESPONSES`
2. Include translations for supported languages
3. Update keyword matching logic

### Custom Content Processing
1. Modify `load_and_process_html_content`
2. Add new data extraction patterns
3. Update structured data schema

## 🚨 Important Notes

### Medical Disclaimer
- This chatbot provides general information only
- Not a substitute for professional medical advice
- Always consult healthcare professionals for medical decisions
- Meko Clinic should be contacted directly for consultations

### API Usage
- Requires OpenAI API key
- Usage costs apply based on API calls
- Monitor usage through OpenAI dashboard
- Consider rate limiting for production use

### Data Privacy
- Conversations are stored locally in session
- No data is permanently stored
- Export functionality allows user control
- Follow local privacy regulations

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper testing
4. Submit pull request
5. Ensure all tests pass

## 📞 Support

For technical support or questions:
- Check the documentation
- Review the code comments
- Contact the development team

For medical consultations:
- **Phone:** +66 2 272 0022
- **Facebook:** @MEKOCLINIC
- **Website:** mekoclinic.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for Meko Clinic**
*Enhancing patient experience through intelligent AI assistance*
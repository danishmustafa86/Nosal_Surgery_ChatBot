import streamlit as st
import os
from openai import OpenAI
from bs4 import BeautifulSoup
import html2text
import re
from langdetect import detect
import tempfile
import base64
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import hashlib
import json
import time
from datetime import datetime
import pandas as pd
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import requests
from urllib.parse import urlparse, urljoin

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Meko Clinic Rhinoplasty Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language mapping with voice support
LANGUAGES = {
    "English": {"code": "en", "native": "English", "voice": "alloy"},
    "Spanish": {"code": "es", "native": "Español", "voice": "nova"},
    "French": {"code": "fr", "native": "Français", "voice": "alloy"},
    "German": {"code": "de", "native": "Deutsch", "voice": "echo"},
    "Italian": {"code": "it", "native": "Italiano", "voice": "alloy"},
    "Portuguese": {"code": "pt", "native": "Português", "voice": "nova"},
    "Russian": {"code": "ru", "native": "Русский", "voice": "fable"},
    "Chinese": {"code": "zh", "native": "中文", "voice": "shimmer"},
    "Japanese": {"code": "ja", "native": "日本語", "voice": "shimmer"},
    "Korean": {"code": "ko", "native": "한국어", "voice": "onyx"},
    "Arabic": {"code": "ar", "native": "العربية", "voice": "onyx"},
    "Hindi": {"code": "hi", "native": "हिंदी", "voice": "nova"},
    "Urdu": {"code": "ur", "native": "اردو", "voice": "nova"},
    "Turkish": {"code": "tr", "native": "Türkçe", "voice": "echo"},
    "Thai": {"code": "th", "native": "ไทย", "voice": "alloy"}
}

# Language detection mapping
LANG_DETECT_MAP = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese",
    "zh-cn": "Chinese", "zh-tw": "Chinese", "ja": "Japanese", "ko": "Korean",
    "ar": "Arabic", "hi": "Hindi", "ur": "Urdu", "tr": "Turkish", "th": "Thai"
}

# Quick response templates for common questions
QUICK_RESPONSES = {
    "pricing": {
        "Thai": "💰 ราคาเสริมจมูกแบบ Open เริ่มต้นที่ 99,000 บาท\n\nรายละเอียดเพิ่มเติม:\n- ราคาขึ้นอยู่กับความซับซ้อนของเคส\n- รวมค่าแพทย์ ค่าห้องผ่าตัด และการดูแลหลังผ่าตัด\n- มีโปรโมชั่นและผ่อนชำระได้\n\nติดต่อสอบถามราคา: +66 2 272 0022",
        "English": "💰 Open Rhinoplasty pricing starts at 99,000 THB\n\nDetails:\n- Price varies based on case complexity\n- Includes surgeon, operating room, and post-op care\n- Promotions and payment plans available\n\nContact for pricing: +66 2 272 0022"
    },
    "consultation": {
        "Thai": "📋 การปรึกษาแพทย์\n\n✅ ปรึกษาฟรีผ่านออนไลน์\n✅ ประเมินใบหน้าดิจิทัล\n✅ วางแผนการผ่าตัด\n✅ คำแนะนำก่อนผ่าตัด\n\nนัดหมาย: +66 2 272 0022\nหรือ Facebook Messenger: @MEKOCLINIC",
        "English": "📋 Consultation Process\n\n✅ Free online consultation\n✅ Digital facial assessment\n✅ Surgical planning\n✅ Pre-operative instructions\n\nBook appointment: +66 2 272 0022\nOr Facebook Messenger: @MEKOCLINIC"
    },
    "recovery": {
        "Thai": "🩹 ระยะเวลาพักฟื้น\n\n• 1-2 สัปดาห์: แผลเริ่มหาย\n• 2-3 สัปดาห์: กลับไปทำงานได้\n• 6-12 เดือน: ผลลัพธ์เต็มที่\n\nการดูแลหลังผ่าตัด:\n- หลีกเลี่ยงการกระทบกระเทือน\n- ทำความสะอาดตามคำแนะนำ\n- มาพบแพทย์ตามนัด",
        "English": "🩹 Recovery Timeline\n\n• 1-2 weeks: Initial healing\n• 2-3 weeks: Return to work\n• 6-12 months: Full results\n\nPost-op care:\n- Avoid trauma to nose\n- Follow cleaning instructions\n- Attend follow-up appointments"
    },
    "contact": {
        "Thai": "📞 ติดต่อเมโกะคลินิก\n\n📱 เบอร์โทร: +66 2 272 0022\n💬 Facebook Messenger: @MEKOCLINIC\n📧 WhatsApp: +66 2 272 0022\n🌐 เว็บไซต์: mekoclinic.com\n\n📍 สาขา: กรุงเทพฯ, ประเทศไทย",
        "English": "📞 Contact Meko Clinic\n\n📱 Phone: +66 2 272 0022\n💬 Facebook Messenger: @MEKOCLINIC\n📧 WhatsApp: +66 2 272 0022\n🌐 Website: mekoclinic.com\n\n📍 Location: Bangkok, Thailand"
    }
}

# Related links and resources database
RELATED_RESOURCES = {
    "rhinoplasty": {
        "videos": [
            {
                "title": "เสริมจมูก ครั้งแรกในชีวิตถึงกับร้องโอโหห ต้องที่ เมโกะคลินิก",
                "url": "https://www.youtube.com/watch?v=example1",
                "description": "รีวิวจากผู้ป่วยจริงที่ทำเสริมจมูกครั้งแรก"
            },
            {
                "title": "คุณพลอย พลอยพรรณ เผยจมูกใหม่สวยเป๊ะ ที่เมโกะ คลินิก",
                "url": "https://www.youtube.com/watch?v=example2",
                "description": "ผลลัพธ์หลังเสริมจมูก Open technique"
            },
            {
                "title": "เสริมจมูก Open ปรับเปลี่ยนโครงสร้างจมูกให้สโลปสวย",
                "url": "https://www.youtube.com/watch?v=example3",
                "description": "เทคนิคการเสริมจมูกแบบเปิด"
            }
        ],
        "websites": [
            {
                "title": "Meko Clinic Official Website",
                "url": "https://mekoclinic.com",
                "description": "เว็บไซต์หลักของเมโกะคลินิก"
            },
            {
                "title": "Rhinoplasty Information - Mayo Clinic",
                "url": "https://www.mayoclinic.org/tests-procedures/rhinoplasty/about/pac-20384532",
                "description": "ข้อมูลทางการแพทย์เกี่ยวกับการเสริมจมูก"
            },
            {
                "title": "American Society of Plastic Surgeons - Rhinoplasty",
                "url": "https://www.plasticsurgery.org/cosmetic-procedures/rhinoplasty",
                "description": "ข้อมูลจากสมาคมศัลยกรรมพลาสติกอเมริกัน"
            }
        ]
    },
    "recovery": {
        "videos": [
            {
                "title": "การดูแลหลังเสริมจมูก - 7 วันแรก",
                "url": "https://www.youtube.com/watch?v=recovery1",
                "description": "คำแนะนำการดูแลหลังผ่าตัด"
            }
        ],
        "websites": [
            {
                "title": "Post-Operative Care Guide",
                "url": "https://mekoclinic.com/recovery-guide",
                "description": "คู่มือการดูแลหลังผ่าตัด"
            }
        ]
    },
    "consultation": {
        "videos": [
            {
                "title": "ขั้นตอนการปรึกษาแพทย์ที่เมโกะคลินิก",
                "url": "https://www.youtube.com/watch?v=consult1",
                "description": "ขั้นตอนการนัดปรึกษาและประเมิน"
            }
        ],
        "websites": [
            {
                "title": "Book Consultation - Meko Clinic",
                "url": "https://mekoclinic.com/book-consultation",
                "description": "จองนัดปรึกษาแพทย์ออนไลน์"
            }
        ]
    }
}

# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    # Try multiple sources for API key
    api_key = None
    
    # 1. Try environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 2. Try Streamlit secrets
    if not api_key:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except:
            pass
    
    # 3. Try .env file (if dotenv is loaded)
    if not api_key:
        try:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
        except:
            pass
    
    # 4. Show configuration help if no key found
    if not api_key:
        st.error("⚠️ OpenAI API Key not found!")
        st.markdown("""
        **Please set up your API key in one of these ways:**
        
        1. **Create a `.env` file** in the project root:
        ```
        OPENAI_API_KEY=your-actual-api-key-here
        ```
        
        2. **Set environment variable:**
        ```bash
        export OPENAI_API_KEY=your-actual-api-key-here
        ```
        
        3. **Create `.streamlit/secrets.toml`:**
        ```toml
        OPENAI_API_KEY = "your-actual-api-key-here"
        ```
        
        4. **For Streamlit Cloud:** Add to app secrets in the dashboard
        """)
        
        # Show a text input for temporary testing
        st.markdown("### 🔑 Temporary API Key Input (for testing)")
        temp_key = st.text_input("Enter your OpenAI API key (temporary):", type="password")
        if temp_key:
            api_key = temp_key
        else:
            st.stop()
    
    # Validate API key format
    if api_key and not api_key.startswith("sk-"):
        st.error("❌ Invalid API key format. API key should start with 'sk-'")
        st.stop()
    
    try:
        client = OpenAI(api_key=api_key)
        # Test the connection
        client.models.list()
        return client
    except Exception as e:
        st.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
        st.markdown("""
        **Common issues:**
        - API key is invalid or expired
        - Network connection issues
        - OpenAI service is down
        
        **Please check your API key and try again.**
        """)
        st.stop()

# Enhanced language detection
def detect_language(text):
    try:
        text_lower = text.lower()
        
        # Check for native scripts
        if re.search(r'[\u0600-\u06FF]', text):
            urdu_words = ['یہ', 'کیا', 'ہے', 'اور', 'میں']
            arabic_words = ['هذا', 'في', 'من', 'على']
            urdu_count = sum(1 for word in urdu_words if word in text)
            arabic_count = sum(1 for word in arabic_words if word in text)
            return "Urdu" if urdu_count > arabic_count else "Arabic"
        
        if re.search(r'[\u0E00-\u0E7F]', text): return "Thai"
        if re.search(r'[\u0900-\u097F]', text): return "Hindi"
        if re.search(r'[\u4e00-\u9fff]', text): return "Chinese"
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text): return "Japanese"
        if re.search(r'[\uac00-\ud7af]', text): return "Korean"
        if re.search(r'[\u0400-\u04FF]', text): return "Russian"
        
        # Check for Roman scripts
        thai_patterns = [r'\b(chai|mai|krub|krab|arai|yang|ngai|sabai)\b']
        urdu_patterns = [r'\b(kya|hai|yaar|kar|hona|lagta|hota|mera|tera)\b']
        hindi_patterns = [r'\b(kya|hai|kar|hona|mera|tera|hamara|mata)\b']
        
        thai_score = sum(1 for p in thai_patterns if re.search(p, text_lower))
        urdu_score = sum(1 for p in urdu_patterns if re.search(p, text_lower))
        hindi_score = sum(1 for p in hindi_patterns if re.search(p, text_lower))
        
        if thai_score > 0: return "Thai"
        if urdu_score > hindi_score: return "Urdu"
        if hindi_score > 0: return "Hindi"
        
        # Use langdetect for other languages
        detected = detect(text)
        return LANG_DETECT_MAP.get(detected, "English")
        
    except:
        return "English"

# Extract links and videos from HTML content
def extract_links_from_html(html_content):
    """Extract video and website links from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    links = {
        "videos": [],
        "websites": []
    }
    
    # Extract video links
    video_elements = soup.find_all(['video', 'iframe'])
    for video in video_elements:
        src = video.get('src', '')
        if src:
            links["videos"].append({
                "title": video.get('title', 'Video'),
                "url": src,
                "description": "Video content from clinic website"
            })
    
    # Extract website links
    website_links = soup.find_all('a', href=True)
    for link in website_links:
        href = link.get('href')
        if href and not href.startswith('#'):
            # Filter for relevant links
            if any(keyword in href.lower() for keyword in ['rhinoplasty', 'nose', 'surgery', 'clinic', 'meko']):
                links["websites"].append({
                    "title": link.get_text(strip=True) or "Related Link",
                    "url": href,
                    "description": "Related information from clinic website"
                })
    
    return links

# Web search functionality using OpenAI's web search
def search_web_for_resources(query, language="English"):
    """Get related resources from predefined database instead of web search"""
    try:
        # Return predefined resources based on query keywords
        query_lower = query.lower()
        
        # Define search keywords and their corresponding resources
        search_keywords = {
            "rhinoplasty": ["rhinoplasty", "nose surgery", "เสริมจมูก", "จมูก"],
            "recovery": ["recovery", "healing", "post-op", "พักฟื้น", "หาย"],
            "consultation": ["consultation", "appointment", "ปรึกษา", "นัด"],
            "pricing": ["price", "cost", "ราคา", "ค่าใช้จ่าย"],
            "contact": ["contact", "phone", "email", "ติดต่อ", "โทร"]
        }
        
        # Find matching resources
        matching_resources = []
        for category, keywords in search_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if category in RELATED_RESOURCES:
                    resources = RELATED_RESOURCES[category]
                    if "videos" in resources:
                        matching_resources.extend(resources["videos"][:2])
                    if "websites" in resources:
                        matching_resources.extend(resources["websites"][:2])
        
        # If no specific matches, return general rhinoplasty resources
        if not matching_resources and "rhinoplasty" in RELATED_RESOURCES:
            resources = RELATED_RESOURCES["rhinoplasty"]
            if "videos" in resources:
                matching_resources.extend(resources["videos"][:2])
            if "websites" in resources:
                matching_resources.extend(resources["websites"][:2])
        
        return matching_resources
        
    except Exception as e:
        st.error(f"Resource search error: {str(e)}")
        return []

# Get related resources based on query
def get_related_resources(user_query, language="English"):
    """Get related video and website links based on user query"""
    query_lower = user_query.lower()
    
    # Check predefined resources first
    related_links = []
    
    for category, resources in RELATED_RESOURCES.items():
        if category in query_lower or any(word in query_lower for word in ["rhinoplasty", "nose", "surgery", "เสริมจมูก", "จมูก", "ผ่าตัด"]):
            if "videos" in resources:
                related_links.extend(resources["videos"][:2])  # Limit to 2 videos
            if "websites" in resources:
                related_links.extend(resources["websites"][:2])  # Limit to 2 websites
    
    # If no predefined resources found, try the updated search function
    if not related_links:
        try:
            search_results = search_web_for_resources(user_query, language)
            if search_results:
                related_links = search_results[:4]  # Limit to 4 results
        except Exception as e:
            # Silently handle any errors to prevent chatbot crashes
            pass
    
    return related_links

# Format related resources for display
def format_related_resources(links, language="English"):
    """Format related resources for display in the response"""
    if not links:
        return ""
    
    if language == "Thai":
        header = "\n\n📺 **วิดีโอและลิงก์ที่เกี่ยวข้อง:**\n"
    else:
        header = "\n\n📺 **Related Videos & Links:**\n"
    
    formatted_links = header
    
    for i, link in enumerate(links[:4], 1):  # Limit to 4 links
        title = link.get("title", "Related Resource")
        url = link.get("url", "#")
        description = link.get("description", "")
        
        formatted_links += f"{i}. **{title}**\n"
        formatted_links += f"   🔗 [{url}]({url})\n"
        if description:
            formatted_links += f"   📝 {description}\n"
        formatted_links += "\n"
    
    return formatted_links

# Enhanced content processing with structured data extraction
@st.cache_data
def load_and_process_html_content():
    try:
        # Try multiple possible paths for the HTML file
        possible_paths = [
            "meko_clinic_rhinoplasty.html",
            "./meko_clinic_rhinoplasty.html",
            os.path.join(os.getcwd(), "meko_clinic_rhinoplasty.html"),
            os.path.join(os.path.dirname(__file__), "meko_clinic_rhinoplasty.html")
        ]
        
        html_content = None
        used_path = None
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as file:
                        html_content = file.read()
                        used_path = path
                        break
            except Exception as e:
                continue
        
        if not html_content:
            # Try to find the file in the current directory
            try:
                current_dir = os.getcwd()
                files = os.listdir(current_dir)
                html_files = [f for f in files if f.endswith('.html')]
                
                if html_files:
                    # Use the first HTML file found
                    html_file_path = os.path.join(current_dir, html_files[0])
                    with open(html_file_path, "r", encoding="utf-8") as file:
                        html_content = file.read()
                        used_path = html_file_path
                        st.info(f"📄 Found HTML file: {html_files[0]}")
            except Exception as e:
                pass
        
        if not html_content:
            st.warning("⚠️ HTML file 'meko_clinic_rhinoplasty.html' not found. Using fallback content.")
            st.info("💡 This might be due to deployment environment differences. The app will still work with fallback content.")
            return get_fallback_content(), {}
        
        # Log which path was used (for debugging)
        if used_path:
            st.success(f"✅ Successfully loaded HTML content from: {used_path}")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract structured data
        structured_data = {
            "procedures": [],
            "pricing": [],
            "contact": [],
            "reviews": [],
            "gallery": [],
            "videos": [],
            "doctors": [],
            "locations": []
        }
        
        # Extract text content
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0
        text_content = h.handle(str(soup))
        
        # Clean up the text
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
        text_content = re.sub(r'\s+', ' ', text_content)
        
        # Extract specific information patterns
        # Pricing
        price_patterns = [
            r'(\d{2,3}(?:,\d{3})*)\s*บาท',
            r'เริ่มเพียง\s*(\d{2,3}(?:,\d{3})*)\s*บาท',
            r'ราคา\s*(\d{2,3}(?:,\d{3})*)\s*บาท'
        ]
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content)
            structured_data["pricing"].extend(matches)
        
        # Contact information
        contact_patterns = [
            r'\+66\s*2\s*272\s*0022',
            r'@MEKOCLINIC',
            r'mekoclinic\.com'
        ]
        for pattern in contact_patterns:
            matches = re.findall(pattern, text_content)
            structured_data["contact"].extend(matches)
        
        # Procedures
        procedure_keywords = [
            "เสริมจมูกแบบเปิด", "Open Rhinoplasty", "เสริมจมูก", "nose surgery",
            "ตะไบจมูก", "ปรับโครงสร้าง", "แก้จมูก", "revision rhinoplasty"
        ]
        for keyword in procedure_keywords:
            if keyword in text_content:
                structured_data["procedures"].append(keyword)
        
        # Extract links from HTML
        extracted_links = extract_links_from_html(html_content)
        structured_data["videos"] = extracted_links["videos"]
        structured_data["websites"] = extracted_links["websites"]
        
        return text_content, structured_data
        
    except Exception as e:
        st.error(f"Error loading HTML content: {str(e)}")
        st.info("💡 Using fallback content. The app will still function normally.")
        return get_fallback_content(), {}

# Fallback content when HTML file is not available
def get_fallback_content():
    return """
    MEKO CLINIC - RHINOPLASTY SPECIALISTS
    
    About Us:
    Meko Clinic is a leading medical facility specializing in rhinoplasty (nose surgery) procedures. 
    We provide comprehensive cosmetic and reconstructive nose surgery services.
    
    Our Services:
    - Primary Rhinoplasty
    - Revision Rhinoplasty 
    - Ethnic Rhinoplasty
    - Functional Rhinoplasty
    - Non-surgical Nose Jobs
    - Consultation Services
    
    Why Choose Meko Clinic:
    - Expert surgeons with years of experience
    - State-of-the-art facilities
    - Personalized treatment plans
    - Comprehensive aftercare support
    - Natural-looking results
    
    Procedure Information:
    Rhinoplasty can address various concerns including:
    - Nose size and shape
    - Nostril size and shape
    - Nasal tip refinement
    - Bridge adjustments
    - Breathing improvements
    
    Recovery Process:
    - Initial healing: 1-2 weeks
    - Return to normal activities: 2-3 weeks
    - Full results visible: 6-12 months
    
    Consultation Process:
    - Initial assessment
    - Digital imaging
    - Surgical planning
    - Pre-operative instructions
    - Follow-up care
    
    Contact Information:
    For consultations and appointments, please contact Meko Clinic directly.
    We offer both in-person and virtual consultations.
    """

# Smart query classification
def classify_query(user_message, clinic_content):
    """Classify if the query is clinic-related or general"""
    clinic_keywords = [
        "rhinoplasty", "nose surgery", "nose job", "เสริมจมูก", "จมูก", "surgery",
        "clinic", "doctor", "procedure", "recovery", "consultation", "price",
        "cost", "appointment", "meko", "เมโกะ", "ผ่าตัด", "ศัลยกรรม"
    ]
    
    user_lower = user_message.lower()
    clinic_score = sum(1 for keyword in clinic_keywords if keyword in user_lower)
    
    # Check if query contains clinic-specific content
    clinic_content_lower = clinic_content.lower()
    content_matches = sum(1 for keyword in clinic_keywords if keyword in clinic_content_lower)
    
    # If query has clinic keywords or matches clinic content, it's clinic-related
    if clinic_score > 0 or content_matches > 0:
        return "clinic_related"
    else:
        return "general"

# Enhanced semantic search
@st.cache_data
def create_semantic_search_index(clinic_content):
    """Create a semantic search index for better content retrieval"""
    try:
        # Split content into chunks
        chunks = re.split(r'\n\n+', clinic_content)
        chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(chunks)
        
        return {
            'vectorizer': vectorizer,
            'tfidf_matrix': tfidf_matrix,
            'chunks': chunks
        }
    except Exception as e:
        st.error(f"Error creating search index: {str(e)}")
        return None

def semantic_search(query, search_index, top_k=3):
    """Perform semantic search on clinic content"""
    if not search_index:
        return []
    
    try:
        # Transform query
        query_vector = search_index['vectorizer'].transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, search_index['tfidf_matrix'])
        
        # Get top matches
        top_indices = similarities[0].argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[0][idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'content': search_index['chunks'][idx],
                    'similarity': similarities[0][idx]
                })
        
        return results
    except Exception as e:
        st.error(f"Error in semantic search: {str(e)}")
        return []

# Token counting function
def count_tokens(text):
    """Rough token count estimation (1 token ≈ 4 characters)"""
    return len(text) // 4

# Smart content selection based on user query with better token management
def select_relevant_content(user_message, clinic_content, search_index=None, max_tokens=1500):
    """Select the most relevant content based on user query with strict token limits"""
    
    # First try semantic search if available
    if search_index:
        semantic_results = semantic_search(user_message, search_index, top_k=1)  # Reduced to 1 result
        if semantic_results:
            selected_content = semantic_results[0]['content']
            if count_tokens(selected_content) <= max_tokens:
                return selected_content
    
    # Fallback to keyword-based selection
    keywords_map = {
        "procedure": ["procedure", "surgery", "operation", "rhinoplasty", "nose job", "plastic surgery", "เสริมจมูก", "ผ่าตัด"],
        "recovery": ["recovery", "healing", "aftercare", "post-op", "swelling", "bruising", "rest", "พักฟื้น", "หาย"],
        "cost": ["cost", "price", "fee", "payment", "insurance", "financing", "expensive", "ราคา", "ค่าใช้จ่าย"],
        "consultation": ["consultation", "appointment", "visit", "meet", "doctor", "surgeon", "ปรึกษา", "นัดหมาย"],
        "types": ["types", "kinds", "different", "options", "primary", "revision", "ethnic", "แบบ", "ประเภท"],
        "results": ["results", "outcome", "before", "after", "expect", "appearance", "look", "ผลลัพธ์", "ผลงาน"]
    }
    
    user_lower = user_message.lower()
    
    # Split content into sections
    sections = clinic_content.split('\n\n')
    scored_sections = []
    
    for section in sections:
        if len(section.strip()) < 50:  # Skip very short sections
            continue
            
        section_lower = section.lower()
        score = 0
        
        # Score based on keyword matches
        for category, keywords in keywords_map.items():
            for keyword in keywords:
                if keyword in user_lower:
                    score += section_lower.count(keyword) * 2
                score += section_lower.count(keyword)
        
        # Boost score for sections with general medical terms
        medical_terms = ["rhinoplasty", "nose", "surgery", "procedure", "clinic", "doctor", "patient", "จมูก", "เมโกะ"]
        for term in medical_terms:
            score += section_lower.count(term)
        
        scored_sections.append((score, section))
    
    # Sort by relevance and select top sections with strict token limit
    scored_sections.sort(key=lambda x: x[0], reverse=True)
    
    selected_content = ""
    current_tokens = 0
    
    for score, section in scored_sections:
        section_tokens = count_tokens(section)
        if current_tokens + section_tokens <= max_tokens:
            selected_content += section + "\n\n"
            current_tokens += section_tokens
        else:
            # If we can't fit the full section, try to fit a portion
            if current_tokens < max_tokens * 0.8:  # Leave some buffer
                words = section.split()
                partial_section = ""
                for word in words:
                    test_section = partial_section + " " + word if partial_section else word
                    if count_tokens(test_section) <= max_tokens - current_tokens:
                        partial_section = test_section
                    else:
                        break
                if partial_section:
                    selected_content += partial_section + "\n\n"
            break
    
    return selected_content.strip() if selected_content else clinic_content[:max_tokens*3]  # Reduced multiplier

# Enhanced response generation with smart context management and related resources
def generate_response(user_message, detected_language, clinic_content, search_index=None, conversation_history=None):
    try:
        client = init_openai_client()
        
        # Classify query
        query_type = classify_query(user_message, clinic_content)
        
        # Check for quick response templates
        user_lower = user_message.lower()
        for key, responses in QUICK_RESPONSES.items():
            if key in user_lower or any(word in user_lower for word in ["ราคา", "price", "cost", "ปรึกษา", "consult", "ติดต่อ", "contact", "พักฟื้น", "recovery"]):
                if detected_language in responses:
                    base_response = responses[detected_language]
                    # Add related resources to quick responses
                    related_links = get_related_resources(user_message, detected_language)
                    if related_links:
                        base_response += format_related_resources(related_links, detected_language)
                    return base_response
        
        lang_info = LANGUAGES.get(detected_language, LANGUAGES["English"])
        native_name = lang_info["native"]
        
        # Select relevant content with reduced token limit
        relevant_content = select_relevant_content(user_message, clinic_content, search_index, max_tokens=1000)
        
        # Build conversation context with strict limits
        context = ""
        if conversation_history and len(conversation_history) > 0:
            # Only use last 2 messages to save tokens
            recent_messages = conversation_history[-2:]
            context_parts = []
            for msg in recent_messages:
                # Truncate long messages
                content = msg['content'][:200] if len(msg['content']) > 200 else msg['content']
                context_parts.append(f"{msg['role']}: {content}")
            context = "\n".join(context_parts)
        
        # Get related resources
        related_links = get_related_resources(user_message, detected_language)
        
        # Create system prompt based on query type with reduced content
        if query_type == "clinic_related":
            system_prompt = f"""You are a medical assistant for Meko Clinic specializing in rhinoplasty.

LANGUAGE: Respond in {detected_language} ({native_name} script)

ROLE: Provide expert information about rhinoplasty procedures, recovery, consultations, and clinic services.

CLINIC INFO:
{relevant_content}

CONVERSATION CONTEXT:
{context}

GUIDELINES:
- Be professional, empathetic, and detailed
- Use the provided clinic information as primary source
- Recommend consulting doctors for medical advice
- Include specific details about procedures, timelines, and care
- Maintain medical confidentiality and ethics
- If information is not in clinic data, clearly state it's general information"""
        else:
            system_prompt = f"""You are a helpful AI assistant.

LANGUAGE: Respond in {detected_language} ({native_name} script)

ROLE: Provide helpful information on general topics.

GUIDELINES:
- Be informative and helpful
- Provide accurate information
- Be conversational and friendly
- If medical advice is requested, recommend consulting healthcare professionals"""

        # Calculate remaining tokens for response with strict limits
        system_tokens = count_tokens(system_prompt)
        user_tokens = count_tokens(user_message)
        max_response_tokens = min(800, 7000 - system_tokens - user_tokens - 500)  # Reduced limits
        
        # Ensure we don't exceed token limits
        if max_response_tokens < 100:
            max_response_tokens = 100
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=max_response_tokens,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        base_response = response.choices[0].message.content
        
        # Add related resources to the response if not already included (with token check)
        if related_links and "📺" not in base_response and "Related" not in base_response:
            resources_text = format_related_resources(related_links, detected_language)
            if count_tokens(base_response + resources_text) < 1500:  # Check total response length
                base_response += resources_text
        
        return base_response
        
    except Exception as e:
        error_messages = {
            "Thai": f"❌ เกิดข้อผิดพลาดในการประมวลผล: {str(e)}",
            "Urdu": f"❌ جواب بناتے وقت خرابی: {str(e)}",
            "Arabic": f"❌ خطأ في معالجة الطلب: {str(e)}",
            "Hindi": f"❌ उत्तर बनाने में त्रुटि: {str(e)}",
            "Spanish": f"❌ Error al procesar la solicitud: {str(e)}",
            "French": f"❌ Erreur lors du traitement: {str(e)}",
            "German": f"❌ Fehler bei der Verarbeitung: {str(e)}",
            "Chinese": f"❌ 处理请求时出错: {str(e)}",
            "Japanese": f"❌ 処理エラー: {str(e)}"
        }
        return error_messages.get(detected_language, f"❌ Error generating response: {str(e)}")

# Enhanced transcription with better error handling
def transcribe_audio(audio_bytes):
    try:
        client = init_openai_client()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        with open(tmp_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language=None,
                temperature=0.2
            )
        
        os.unlink(tmp_file_path)
        return transcription.strip()
    except Exception as e:
        st.error(f"❌ Transcription error: {str(e)}")
        return None

# Enhanced speech generation with better quality
def generate_speech(text, language):
    try:
        client = init_openai_client()
        voice = LANGUAGES.get(language, LANGUAGES["English"])["voice"]
        
        # Truncate text if too long, but try to cut at sentence boundaries
        max_length = 2000
        if len(text) > max_length:
            truncated = text[:max_length]
            last_sentence = truncated.rfind('.')
            if last_sentence > max_length * 0.8:
                text = truncated[:last_sentence + 1]
            else:
                text = truncated + "..."
        
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=0.9
        )
        return response.content
    except Exception as e:
        st.error(f"❌ Speech generation error: {str(e)}")
        return None

# Create audio player with better styling
def create_audio_player(audio_content):
    audio_base64 = base64.b64encode(audio_content).decode()
    return f"""
    <div style="margin: 10px 0;">
        <audio controls style="width: 100%; max-width: 400px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    </div>
    """

# Export conversation
def export_conversation(messages, format="json"):
    if format == "json":
        return json.dumps(messages, indent=2, ensure_ascii=False)
    elif format == "txt":
        text = "Meko Clinic Chatbot Conversation\n"
        text += "=" * 40 + "\n\n"
        for msg in messages:
            text += f"{msg['role'].upper()}: {msg['content']}\n\n"
        return text
    elif format == "csv":
        df = pd.DataFrame(messages)
        return df.to_csv(index=False)

# Function to manage conversation history and prevent token overflow
def manage_conversation_history(messages, max_messages=10):
    """Keep conversation history manageable to prevent token overflow"""
    if len(messages) > max_messages:
        # Keep the first message (greeting) and the last max_messages-1 messages
        return [messages[0]] + messages[-(max_messages-1):]
    return messages

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clinic_content" not in st.session_state:
    st.session_state.clinic_content, st.session_state.structured_data = load_and_process_html_content()
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = []
if "search_index" not in st.session_state:
    st.session_state.search_index = create_semantic_search_index(st.session_state.clinic_content)
if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "total_queries": 0,
        "clinic_queries": 0,
        "general_queries": 0,
        "voice_queries": 0,
        "text_queries": 0,
        "languages_used": defaultdict(int),
        "response_times": []
    }

# Manage conversation history to prevent token overflow
st.session_state.messages = manage_conversation_history(st.session_state.messages)

# Enhanced sidebar with more options
with st.sidebar:
    st.title("🏥 Meko Clinic")
    st.markdown("### Advanced Rhinoplasty Chatbot")
    
    # Display content status
    content_length = len(st.session_state.clinic_content)
    st.info(f"📄 Clinic content loaded: {content_length:,} characters")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💰 Pricing", help="Get pricing information"):
            st.session_state.quick_action = "pricing"
    
    with col2:
        if st.button("📋 Consultation", help="Book consultation"):
            st.session_state.quick_action = "consultation"
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🩹 Recovery", help="Recovery information"):
            st.session_state.quick_action = "recovery"
    
    with col4:
        if st.button("📞 Contact", help="Contact information"):
            st.session_state.quick_action = "contact"
    
    # Voice settings
    voice_enabled = st.toggle("🎙️ Enable Voice Features", value=st.session_state.voice_enabled)
    st.session_state.voice_enabled = voice_enabled
    
    # Language selection
    selected_language = st.selectbox(
        "🌐 Language Override",
        options=["Auto-detect"] + list(LANGUAGES.keys()),
        index=0,
        help="Select a specific language or use auto-detection"
    )
    
    # Model settings
    st.markdown("### ⚙️ AI Model Settings")
    st.info("Using GPT-4 for high-quality responses")
    st.info("Using Whisper for accurate transcription")
    st.info("Using TTS-1-HD for clear speech")
    
    # Export options
    st.markdown("### 📤 Export Options")
    export_format = st.selectbox("Export format", ["json", "txt", "csv"])
    if st.button("📥 Export Conversation"):
        if st.session_state.messages:
            export_data = export_conversation(st.session_state.messages, export_format)
            st.download_button(
                label="Download",
                data=export_data,
                file_name=f"meko_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}",
                mime="text/plain"
            )
    
    # Clear chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.last_audio_hash = None
        st.session_state.conversation_context = []
        st.rerun()
    
    # Analytics
    if st.session_state.analytics["total_queries"] > 0:
        st.markdown("### 📊 Analytics")
        st.metric("Total Queries", st.session_state.analytics["total_queries"])
        st.metric("Clinic Queries", st.session_state.analytics["clinic_queries"])
        st.metric("Voice Queries", st.session_state.analytics["voice_queries"])
        
        if st.session_state.analytics["response_times"]:
            avg_time = np.mean(st.session_state.analytics["response_times"])
            st.metric("Avg Response Time", f"{avg_time:.1f}s")
    
    # Conversation stats
    if st.session_state.messages:
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"**Messages:** {total_messages} ({user_messages} from you)")
    
    # Supported languages
    st.markdown("### 🌍 Supported Languages")
    st.markdown("""
    **Full Support:** English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Urdu, Turkish, Thai
    
    **Features:** Voice input/output, native script support, cultural context awareness
    """)
    

    # Tips
    st.markdown("### 💡 Tips for Better Results")
    st.markdown("""
    - Ask specific questions about procedures
    - Mention your concerns or goals
    - Ask about recovery times
    - Inquire about consultation process
    - Use voice input for natural conversation
    - Use quick action buttons for common questions
    """)

# Main interface with enhanced styling
st.title("💬 Meko Clinic Rhinoplasty Assistant")
st.markdown("*Ask me anything about rhinoplasty procedures, recovery, consultations, and our services*")

# Handle quick actions
if hasattr(st.session_state, 'quick_action') and st.session_state.quick_action:
    action = st.session_state.quick_action
    detected_lang = selected_language if selected_language != "Auto-detect" else "English"
    
    if action in QUICK_RESPONSES and detected_lang in QUICK_RESPONSES[action]:
        response = QUICK_RESPONSES[action][detected_lang]
        
        # Add to conversation
        st.session_state.messages.append({
            "role": "user",
            "content": f"Quick action: {action}",
            "detected_language": detected_lang,
            "input_type": "quick_action"
        })
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "language": detected_lang,
            "has_audio": True
        })
        
        # Update analytics
        st.session_state.analytics["total_queries"] += 1
        st.session_state.analytics["clinic_queries"] += 1
        
        del st.session_state.quick_action
        st.rerun()

# Enhanced chat history display with auto-scroll
if st.session_state.messages:
    st.markdown("### 💬 Conversation History")
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                lang = msg.get('detected_language', 'Unknown')
                input_type = msg.get('input_type', 'text')
                icon = "🎤" if input_type == "voice" else "💬" if input_type == "text" else "⚡"
                
                with st.chat_message("user"):
                    st.markdown(f"**{icon} ({lang}):** {msg['content']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg['content'])
                    
                    # Enhanced voice playback for assistant messages
                    if st.session_state.voice_enabled and msg.get('language') and msg.get('has_audio'):
                        col1, col2 = st.columns([1, 4])
                        
                        with col1:
                            if st.button(f"🔊 Play", key=f"play_{i}", help="Generate and play audio response"):
                                with st.spinner("🎵 Generating high-quality audio..."):
                                    speech_bytes = generate_speech(msg['content'], msg['language'])
                                    if speech_bytes:
                                        st.markdown(create_audio_player(speech_bytes), unsafe_allow_html=True)
                                    else:
                                        st.error("❌ Failed to generate audio")
                        
                        with col2:
                            st.caption(f"Language: {msg.get('language', 'Unknown')}")

# Auto-scroll to bottom when new messages are added
if st.session_state.messages:
    # Add a spacer to push content to bottom
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    # Add auto-scroll JavaScript
    st.markdown("""
    <script>
        // Function to scroll to bottom
        function scrollToBottom() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }
        
        // Scroll to bottom when page loads
        window.addEventListener('load', scrollToBottom);
        
        // Scroll to bottom when new content is added
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    setTimeout(scrollToBottom, 100);
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Also scroll when Streamlit reruns
        if (window.parent !== window) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'scroll'
            }, '*');
        }
    </script>
    """, unsafe_allow_html=True)

# Input section at the bottom
st.markdown("---")
st.markdown("### 💬 Ask Your Question")

# Voice input section (moved to bottom)
if st.session_state.voice_enabled:
    st.markdown("#### 🎙️ Voice Input")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        audio_bytes = audio_recorder(
            text="🎤 Click to record your question",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            key="voice_input"
        )
    
    with col2:
        if audio_bytes:
            st.success("✅ Audio recorded")
    
    # Process audio with better handling
    if audio_bytes:
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        if audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = audio_hash
            
            with st.spinner("🎧 Transcribing your voice..."):
                transcription = transcribe_audio(audio_bytes)
            
            if transcription:
                st.success(f"🎤 **Transcribed:** {transcription}")
                
                # Process voice input
                detected_language = selected_language if selected_language != "Auto-detect" else detect_language(transcription)
                
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": transcription,
                    "detected_language": detected_language,
                    "input_type": "voice"
                })
                
                # Update analytics
                st.session_state.analytics["total_queries"] += 1
                st.session_state.analytics["voice_queries"] += 1
                st.session_state.analytics["languages_used"][detected_language] += 1
                
                # Generate response
                start_time = time.time()
                with st.spinner("🤖 Generating detailed response..."):
                    reply = generate_response(
                        transcription, 
                        detected_language, 
                        st.session_state.clinic_content,
                        st.session_state.search_index,
                        st.session_state.messages
                    )
                
                response_time = time.time() - start_time
                st.session_state.analytics["response_times"].append(response_time)
                
                # Classify query for analytics
                query_type = classify_query(transcription, st.session_state.clinic_content)
                if query_type == "clinic_related":
                    st.session_state.analytics["clinic_queries"] += 1
                else:
                    st.session_state.analytics["general_queries"] += 1
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "language": detected_language,
                    "has_audio": True
                })
                
                st.rerun()

# Text input section (at the very bottom)
st.markdown("#### 💬 Text Input")
if prompt := st.chat_input("💭 Ask about rhinoplasty procedures, recovery, costs, or consultations..."):
    detected_language = selected_language if selected_language != "Auto-detect" else detect_language(prompt)
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "detected_language": detected_language,
        "input_type": "text"
    })
    
    # Update analytics
    st.session_state.analytics["total_queries"] += 1
    st.session_state.analytics["text_queries"] += 1
    st.session_state.analytics["languages_used"][detected_language] += 1
    
    # Generate response
    start_time = time.time()
    with st.spinner("🤖 Generating comprehensive response..."):
        reply = generate_response(
            prompt, 
            detected_language, 
            st.session_state.clinic_content,
            st.session_state.search_index,
            st.session_state.messages
        )
    
    response_time = time.time() - start_time
    st.session_state.analytics["response_times"].append(response_time)
    
    # Classify query for analytics
    query_type = classify_query(prompt, st.session_state.clinic_content)
    if query_type == "clinic_related":
        st.session_state.analytics["clinic_queries"] += 1
    else:
        st.session_state.analytics["general_queries"] += 1
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "language": detected_language,
        "has_audio": True
    })
    
    st.rerun()

# Footer with additional information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏥 <strong>Meko Clinic Rhinoplasty Assistant</strong></p>
    <p>Powered by GPT-4 • Multilingual Support • Voice Enabled • Smart Search</p>
    <p><em>For medical consultations, please contact Meko Clinic directly</em></p>
</div>
""", unsafe_allow_html=True)
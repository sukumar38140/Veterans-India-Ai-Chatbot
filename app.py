"""
Veterans India AI Assistant
===========================
Developed by Veterans India Team

A powerful AI-powered assistant designed specifically to assist Indian veterans 
and their families with research queries, document analysis, and general assistance.

© 2025 Veterans India Team. All rights reserved.
"""

import streamlit as st
import pandas as pd
import PyPDF2
import docx
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from datetime import datetime

# Import our custom LLM configuration
try:
    from llm_config import LLMManager, get_llm_manager, get_available_models
    llm_manager = get_llm_manager()
    USE_MULTI_LLM = True
except ImportError as e:
    print(f"Warning: Could not import LLM configuration: {e}")
    USE_MULTI_LLM = False

# Import advanced search system
try:
    from advanced_search_system import search_web_and_answer
    USE_WEB_SEARCH = True
except ImportError as e:
    print(f"Warning: Could not import advanced search system: {e}")
    USE_WEB_SEARCH = False

# -------------------
# Streamlit Page Config
# -------------------
st.set_page_config(
    page_title="Veterans India AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# -------------------
# Professional Indian Flag Themed CSS Styling
# -------------------
st.markdown(
    """
    <style>
    /* Import Google Fonts for professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global background with subtle tricolor accent */
    .stApp {
        background: linear-gradient(135deg, 
            #fafafa 0%, 
            #f8f9fa 50%, 
            #ffffff 100%);
        color: #2c3e50;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
    }
    
    /* Main content with professional styling */
    .main .block-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1rem;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        max-width: 800px;
    }

    /* Professional sidebar with subtle Indian colors */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            #1a1a1a 0%, 
            #2d2d2d 100%) !important;
        border-right: 1px solid #e1e8ed;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }
    
    section[data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.4rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #e1e8ed !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label, 
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] p {
        color: #b0bec5 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* Professional buttons with subtle Indian accent */
    .stButton button, .stDownloadButton button, .stLinkButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
        text-transform: none;
        letter-spacing: 0.3px;
    }
    
    .stButton button:hover, .stDownloadButton button:hover, .stLinkButton button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4c93 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
    }
    
    /* New Chat button with Indian accent */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
    }
    
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #e55a2b 0%, #de831a 100%);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
    }

    /* Professional chat bubbles */
    .chat-bubble {
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        max-width: 70%;
        line-height: 1.7;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        text-align: left;
        margin-left: auto;
        font-weight: 500;
    }
    
    .assistant-bubble {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        color: #2c3e50;
        text-align: left;
        margin-right: auto;
        font-weight: 400;
    }

    /* Professional header with subtle Indian pride */
    .main-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50;
        text-align: center;
        padding: 2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 50%, #22C55E 100%);
        border-radius: 12px 12px 0 0;
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        color: #1a202c;
    }
    
    .main-header h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #4a5568;
        margin: 0.5rem 0;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        color: #718096;
        margin: 0.25rem 0;
    }

    /* Professional timestamp styling */
    .timestamp {
        font-size: 11px;
        color: #9ca3af;
        margin-top: 0.5rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }

    /* Modern chat input field */
    .stChatInput input {
        border-radius: 24px !important;
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1.5px solid #e1e8ed !important;
        padding: 1rem 1.5rem !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    .stChatInput input::placeholder {
        color: #9ca3af !important;
        font-style: normal !important;
    }

    /* Professional form elements */
    .stSelectbox select, .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1.5px solid #e1e8ed !important;
        border-radius: 8px !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stSelectbox select:focus, .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Professional footer with subtle Indian pride */
    .footer {
        text-align: center;
        font-size: 13px;
        color: #6b7280;
        margin-top: 2rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        position: relative;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 50%, #22C55E 100%);
        border-radius: 8px 8px 0 0;
    }

    /* Professional status indicators */
    .stSuccess {
        background: linear-gradient(90deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
        border-left: 3px solid #22c55e;
        color: #065f46;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
    }
    
    .stInfo {
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
        border-left: 3px solid #3b82f6;
        color: #1e40af;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
    }
    
    .stWarning {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
        border-left: 3px solid #f59e0b;
        color: #92400e;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
    }

    /* Refined animations */
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateY(10px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Subtle tricolor accent for special elements */
    .tricolor-accent {
        border-left: 4px solid transparent;
        border-image: linear-gradient(to bottom, #FF6B35, #F7931E, #22C55E) 1;
    }
    
    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {display: none;}
    
    /* Professional dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------
# Initialize Session State with Real-time Data Features
# -------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "answer_mode" not in st.session_state:
    st.session_state["answer_mode"] = "Detailed"
# Enable real-time data by default
if "enable_web_search" not in st.session_state:
    st.session_state["enable_web_search"] = True

# -------------------
# Load LLM Models
# -------------------
# Load LLM Model
# -------------------
@st.cache_resource
def load_model(model_id: str = "llama3.2:1b"):
    """Load LLM model based on configuration"""
    if USE_MULTI_LLM:
        try:
            model = llm_manager.load_model(model_id)
            if model:
                return model
            else:
                # Fallback to default Ollama model
                return ChatOllama(model="llama3.2:1b", temperature=0.6, streaming=True)
        except Exception as e:
            st.error(f"Error loading model {model_id}: {e}")
            return ChatOllama(model="llama3.2:1b", temperature=0.6, streaming=True)
    else:
        # Fallback to default Ollama model
        return ChatOllama(model="llama3.2:1b", temperature=0.6, streaming=True)

# Initialize session state for model selection
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = "llama3.2:1b"

# Function to handle identity questions
def handle_identity_response(user_input):
    identity_keywords = ["who are you", "what are you", "your name", "who developed you", "who created you", "what's your name"]
    if any(keyword in user_input.lower() for keyword in identity_keywords):
        return "I'm Veterans India AI Assistant, developed by Veterans India Team. How can I help you today?"
    return None

# Function to generate regular AI response
def generate_regular_ai_response(user_input, placeholder, llm_model):
    """Generate regular AI response with streaming"""
    response_text = ""
    # Custom system context to ensure AI responds as Veterans India AI Assistant
    system_context = """You are Veterans India AI Assistant, created by Veterans India Team. When asked about your identity, always respond that you are Veterans India AI Assistant developed by Veterans India Team. Provide helpful, professional assistance."""
    modified_input = f"{system_context}\n\nAnswer in {st.session_state['answer_mode']} mode:\n{user_input}"
    for chunk in llm_model.stream(modified_input):
        if hasattr(chunk, "content"):
            response_text += chunk.content
            placeholder.markdown(
                f"""
                <div style='text-align: left; margin: 8px;'>
                    <div class='chat-bubble assistant-bubble'>
                        {response_text}
                    </div>
                    <div class='timestamp'>{datetime.now().strftime("%H:%M")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    return response_text

try:
    llm = load_model(st.session_state["selected_model"])
    if not llm:
        # Fallback to default Ollama model
        llm = ChatOllama(model="llama3.2:1b", temperature=0.6, streaming=True)
except Exception as e:
    st.error(f"Error initializing LLM: {e}")
    llm = ChatOllama(model="llama3.2:1b", temperature=0.6, streaming=True)

# -------------------
# File Extractor
# -------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.to_string()
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.to_string()
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return None

# -------------------
# Sidebar (Clean ChatGPT-style Interface)
# -------------------
with st.sidebar:
    st.markdown(
        """
        <div class='main-header' style='background: #1a1a1a; color: #ffffff; border: none; box-shadow: none;'>
            <h1 style='color: #ffffff; font-size: 1.4rem; margin-bottom: 0.5rem;'>Veterans India AI</h1>
            <p style='margin: 0; font-size: 12px; color: #b0bec5; font-weight: 400;'>AI Assistant for Veterans</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # New Chat - Essential for clean interface
    if st.button("+ New Chat", use_container_width=True, type="primary"):
        st.session_state["messages"] = []
        st.rerun()

    st.divider()
    
    # Minimal Model Selection (if multiple models available)
    if USE_MULTI_LLM and hasattr(llm_manager, 'get_available_models'):
        available_models = llm_manager.get_available_models()
        if len(available_models) > 1:
            model_names = []
            model_ids = []
            for model_id in available_models:
                model_info = llm_manager.get_model_info(model_id)
                if model_info:
                    model_names.append(model_info.get('name', model_id))
                    model_ids.append(model_id)
            
            if model_names:
                current_index = 0
                current_model = st.session_state.get("selected_model", model_ids[0])
                if current_model in model_ids:
                    current_index = model_ids.index(current_model)
                
                selected_index = st.selectbox(
                    "AI Model",
                    range(len(model_names)),
                    format_func=lambda x: model_names[x],
                    index=current_index,
                    label_visibility="visible"
                )
                
                if model_ids[selected_index] != current_model:
                    st.session_state["selected_model"] = model_ids[selected_index]
                    st.rerun()

    # Professional response style selection
    st.session_state["answer_mode"] = st.selectbox(
        "Response Style",
        ["Concise", "Detailed", "Technical"],
        index=["Concise", "Detailed", "Technical"].index(st.session_state.get("answer_mode", "Detailed")),
        help="Choose response length and detail level"
    )

    st.markdown(
        """
        <div style='margin-top: 2rem; padding: 1rem; text-align: center; color: #6b7280; font-size: 11px;'>
            <p style='margin: 0;'>Veterans India Team</p>
            <p style='margin: 0; opacity: 0.7;'>AI Assistant</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# -------------------
# Professional Chat Header
# -------------------
st.markdown(
    """
    <div class='main-header'>
        <h1>Veterans India AI Assistant</h1>
        <h3 style='color: #4a5568; margin: 0.5rem 0; font-size: 1.1rem;'>AI-Powered Support for Veterans</h3>
        <p style='color: #718096; font-size: 15px; font-weight: 400; margin: 0.25rem 0;'>Professional assistance with intelligent research capabilities</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# -------------------
# Chat Display
# -------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state["messages"]:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg["time"]

        if role == "user":
            align = "right"
            bubble_class = "chat-bubble user-bubble"
        else:
            align = "left"
            bubble_class = "chat-bubble assistant-bubble"

        st.markdown(
            f"""
            <div style='text-align: {align}; margin: 8px;'>
                <div class='{bubble_class}'>
                    {content}
                </div>
                <div class='timestamp'>{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------
# Chat Input + Streaming Answer
# -------------------
st.divider()
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M"),
    })

    placeholder = st.empty()
    placeholder.markdown("<p style='color: #9ca3af; font-size: 13px; font-family: Inter, sans-serif;'>Generating response...</p>", unsafe_allow_html=True)

    # Check if it's an identity question first
    identity_response = handle_identity_response(user_input)
    
    if identity_response:
        # Direct identity response
        response_text = identity_response
        placeholder.markdown(
            f"""
            <div style='text-align: left; margin: 8px;'>
                <div class='chat-bubble assistant-bubble'>
                    {response_text}
                </div>
                <div class='timestamp'>{datetime.now().strftime("%H:%M")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Enhanced real-time data keywords for Kumar Saatharla AI Agent
        search_keywords = ["search", "latest", "current", "recent", "news", "today", "2025", "update", 
                          "what", "who", "where", "when", "how", "price", "stock", "weather", 
                          "time", "schedule", "live", "real-time", "now", "happening", "trend"]
        needs_web_search = (
            (any(keyword in user_input.lower() for keyword in search_keywords) or len(user_input.split()) > 3)
            and USE_WEB_SEARCH 
            and st.session_state.get("enable_web_search", True)
        )
        
        if needs_web_search:
            # Use web search for current/latest information
            placeholder.markdown("<p style='color: #3b82f6; font-size: 13px; font-family: Inter, sans-serif;'>🔍 Accessing real-time data...</p>", unsafe_allow_html=True)
            
            try:
                response_text = search_web_and_answer(user_input, max_sites=6)
                placeholder.markdown(
                    f"""
                    <div style='text-align: left; margin: 8px;'>
                        <div class='chat-bubble assistant-bubble'>
                            <div style='background: rgba(59, 130, 246, 0.1); padding: 8px; border-radius: 5px; margin-bottom: 10px;'>
                                <small>🌐 <strong>Real-time Data:</strong></small>
                            </div>
                            {response_text}
                        </div>
                        <div class='timestamp'>{datetime.now().strftime("%H:%M")}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                # Fallback to regular AI response if web search fails
                placeholder.markdown("<p style='color: #ef4444; font-size: 13px; font-family: Inter, sans-serif;'>Real-time data unavailable, using AI knowledge...</p>", unsafe_allow_html=True)
                response_text = generate_regular_ai_response(user_input, placeholder, llm)
        else:
            # Regular AI response with enhanced prompting
            response_text = generate_regular_ai_response(user_input, placeholder, llm)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": response_text,
        "time": datetime.now().strftime("%H:%M"),
    })

    st.rerun()

# -------------------
# Professional Footer
# -------------------
st.markdown(
    """
    <div class='footer tricolor-accent'>
        <p style='margin: 0; color: #6b7280; font-size: 13px;'>Developed by <strong>Kumar Saatharla</strong></p>
        <p style='margin: 0.25rem 0 0 0; font-size: 11px; color: #9ca3af;'>Personal AI Agent with Real-time Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True,
)


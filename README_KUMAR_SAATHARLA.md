# 🤖 Kumar Saatharla AI Agent

**Personal AI Assistant with Real-time Data Integration**

A sophisticated personal AI assistant that provides intelligent responses with access to real-time information from the web. Built with advanced language models and web search capabilities for comprehensive assistance across various domains.

---

## ✨ **Key Features**

### 🌐 **Real-time Data Access**
- Live web search integration for current information
- Automatic detection of queries requiring fresh data
- Intelligent information synthesis from multiple sources

### 🤖 **Advanced AI Capabilities**
- Multiple AI model support (LLaMA, Mistral, Code Llama, etc.)
- Context-aware responses with streaming output
- Configurable response styles (Concise, Detailed, Technical)

### 💬 **Professional Chat Interface**
- Clean, ChatGPT-style interface design
- Real-time response generation
- Conversation memory and context retention

### 🔍 **Intelligent Search**
- Automatic web search for questions about current events
- Smart keyword detection for real-time data needs
- Enhanced search results processing and summarization

---

## 🚀 **Quick Start**

### **1. Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup AI models
python setup_models.py
```

### **2. Launch**
```bash
# Start the AI agent
streamlit run app.py
```

### **3. Access**
Open your browser and navigate to `http://localhost:8501`

---

## 🛠️ **Configuration**

### **AI Models**
The agent supports multiple AI models:
- **LLaMA 3.2 1B** - Fast responses (1.3GB)
- **LLaMA 3.2 3B** - Balanced performance (2.0GB)
- **Mistral 7B** - High quality responses (4.1GB)
- **Code Llama 7B** - Programming assistance (3.8GB)

### **Real-time Data**
Web search automatically activates for queries containing:
- Current events keywords: "latest", "recent", "today", "news"
- Question words: "what", "who", "where", "when", "how"
- Data queries: "price", "weather", "time", "schedule"
- Live information: "live", "real-time", "now", "happening"

---

## 🎯 **Use Cases**

- **Personal Research**: Get current information on any topic
- **Decision Support**: Real-time data for informed decisions
- **General Assistance**: Wide range of knowledge and capabilities
- **Current Events**: Stay updated with latest news and trends
- **Technical Help**: Programming and technical assistance

---

## 🔧 **Technical Details**

### **Framework**: Streamlit + LangChain
### **AI Models**: Ollama (Local execution)
### **Search**: Real-time web integration
### **Interface**: Professional ChatGPT-style design

---

## 📞 **Contact**

**Developer**: Kumar Saatharla  
**Purpose**: Personal AI Agent with Real-time Intelligence

---

## 📄 **License**

© 2025 Kumar Saatharla. All rights reserved.

# �️ Veterans India AI Assistant

A comprehensive **AI-powered assistant** designed specifically for **Indian military veterans** and their families. Built with advanced web search capabilities, real-time information access, and automatic continuous learning to provide the most relevant and up-to-date assistance for veteran services, job opportunities, government benefits, and support.

---

## 🚀 Key Features  
- ✅ **Real-time Web Search Integration** - Get current job openings, government updates, and latest veteran services information
- ✅ **Veteran-focused AI Assistant** - Specialized knowledge in veteran affairs, benefits, and services
- ✅ **Automatic Continuous Training** - AI learns from user interactions to improve responses over time
- ✅ **Job Opportunity Search** - Current openings for veterans across government and private sectors
- ✅ **Government Benefits Guide** - Information on pensions, healthcare, education, and welfare schemes
- ✅ **Professional Modern UI** with military-inspired design
- ✅ **Feedback System** - Rate responses to help improve AI accuracy
- ✅ **Venue Search** - Find conference and event venues across India
- ✅ **Memory-efficient AI** using LLaMA 3.2 for optimal performance

---

## 🎯 Specialized Services

### Veteran Employment
- Current job openings for ex-servicemen
- Corporate veteran hiring programs  
- Government job notifications with reservations
- Skill development and career transition support

### Government Benefits
- Pension schemes and application procedures
- ECHS healthcare facilities and benefits
- Educational scholarships for veteran families
- CSD canteen access and benefits

### Support Services
- Legal assistance and rights awareness
- Rehabilitation and welfare programs
- Family support services
- Housing and accommodation assistance

---

## 🤖 AI Technology Stack

### Core AI Model
- **LLaMA 3.2 1B** - Fast, efficient responses optimized for veteran queries
- **Ollama Integration** - Local AI processing for privacy and speed
- **Automatic Training System** - Continuous improvement based on user feedback

### Web Search Integration
- **Google Search API** - Real-time information retrieval
- **Multi-source Content Extraction** - BeautifulSoup, Scrapy, newspaper3k
- **Content Filtering** - Relevance scoring and quality assessment
- **LLM Synthesis** - AI-powered information synthesis and summarization

---

## 📂 Project Structure  

```bash
veterans-india-ai/
│── app_simple.py           # Main Streamlit application with web search
│── advanced_search_system.py  # Web search and content extraction engine
│── auto_training_system.py    # Automatic continuous training system  
│── venue_search_help.py      # Venue information for events and conferences
│── llm_config.py             # LLM configuration and management
│── requirements.txt          # Python dependencies
│── training_data/            # User interaction logs for training
    └── interactions.jsonl    # Conversation history and feedback
│── requirements.txt    # Python dependencies
│── models/             # Directory for local model files
│── llms/              # LLM configurations and cache
└── README.md          # This documentation
```

---

## 🛠️ Quick Start

### Method 1: Automated Setup (Recommended)
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Free Space Technologies Chatbot"
   ```

2. **Run setup script**
   ```bash
   python setup_models.py
   ```
   Choose option 1 to install Python dependencies, then option 2 to install recommended models.

3. **Start the application**
   ```bash
   python run_app.py
   ```

### Method 2: Manual Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama** (if not already installed)
   - Download from: https://ollama.com/download
   - Follow installation instructions for your OS

3. **Pull LLM models**
   ```bash
   # Quick start with lightweight model
   ollama pull llama3.2:1b
   
   # For better quality (larger download)
   ollama pull llama3.2:3b
   ollama pull mistral:7b
   
   # For coding assistance
   ollama pull codellama:7b
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:8501`

---

## ⚙️ Model Installation Guide

### Ollama Models
The application supports multiple Ollama models. Install any combination:

```bash
# Meta LLaMA models
ollama pull llama3.2:1b      # 1.3GB - Fast
ollama pull llama3.2:3b      # 2.0GB - Balanced
ollama pull llama3.1:8b      # 4.7GB - High Quality
ollama pull llama3.1:70b     # 40GB+ - Premium (requires 64GB+ RAM)
ollama pull llama2:7b        # 3.8GB - Reliable
ollama pull llama2:13b       # 7.3GB - Better quality

# Other excellent models
ollama pull mistral:7b       # 4.1GB - Great general purpose
ollama pull codellama:7b     # 3.8GB - Programming specialist
ollama pull phi3:3.8b        # 2.2GB - Microsoft's efficient model
ollama pull qwen2:7b         # 4.4GB - Multilingual
ollama pull gemma:7b         # 5.0GB - Google's model
```

### Model Recommendations by Use Case

| **Use Case** | **Recommended Model** | **Size** | **Description** |
|--------------|----------------------|----------|-----------------|
| **Quick Testing** | llama3.2:1b | 1.3GB | Fastest, good for development |
| **General Use** | llama3.2:3b | 2.0GB | Best balance of speed/quality |
| **High Quality** | llama3.1:8b | 4.7GB | Excellent responses |
| **Programming** | codellama:7b | 3.8GB | Code generation & debugging |
| **Alternative** | mistral:7b | 4.1GB | Great general purpose |
| **Production** | llama3.1:70b | 40GB+ | Highest quality (needs powerful GPU) |

---

## 🖥️ System Requirements

### Minimum Requirements
- **RAM**: 8GB (for 1B-3B models)
- **Storage**: 5GB free space
- **Python**: 3.8+
- **OS**: Windows, macOS, Linux

### Recommended Requirements
- **RAM**: 16GB+ (for 7B models)
- **Storage**: 20GB+ free space
- **GPU**: Optional, but improves performance
- **CPU**: Multi-core processor

### For Large Models (70B+)
- **RAM**: 64GB+
- **GPU**: 24GB+ VRAM (RTX 4090, A100, etc.)
- **Storage**: 100GB+ free space

---

## 🚀 Usage Guide

1. **Start the application**
   ```bash
   python run_app.py
   ```

2. **Select your model**
   - Use the sidebar to choose from available models
   - The app will show which models are installed
   - Install commands are provided for missing models

3. **Chat with the AI**
   - Type your questions in the chat input
   - Upload documents for analysis
   - Adjust answer style (Concise/Detailed/Technical)

4. **Features**
   - **Document Upload**: PDF, Word, Excel, TXT files
   - **User Authentication**: Login/Signup system
   - **Chat Memory**: Conversation history
   - **Multiple Models**: Switch between different AI models

---

## 🔧 Configuration

The LLM configuration is managed in `llm_config.py`. You can:
- Add new models
- Adjust temperature settings  
- Configure local model paths
- Set model-specific parameters

---

## 📚 Development

### Adding New Models
1. Edit `llm_config.py`
2. Add model configuration to `_initialize_models()`
3. Test with `setup_models.py`

### Customizing the Interface
- Modify `app.py` for UI changes
- Update CSS styling in the markdown sections
- Add new features to the sidebar

---

## ❗ Troubleshooting

### Common Issues

**"Model not found" error**
```bash
# Pull the missing model
ollama pull <model-name>
```

**Slow response times**
- Try a smaller model (llama3.2:1b)
- Close other applications to free memory
- Check if Ollama is running: `ollama list`

**Installation issues**
```bash
# Update pip and reinstall
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Ollama not starting**
- Restart Ollama service
- Check if port 11434 is available
- Reinstall Ollama if necessary

---

## 🎯 Purpose

This AI Assistant is specifically designed to:
- **Support Indian Veterans** with information and assistance
- **Provide research-grade responses** for various queries
- **Handle document analysis** and summarization
- **Offer personalized assistance** with memory capabilities

---

## 🤝 Contributing

We welcome contributions from the veterans community and supporters. Please feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

---

## 📞 Support

For support and inquiries, please contact:
**Veterans India Team**

---

**© 2025 Veterans India Team. Developed with ❤️ for Indian Veterans.**  

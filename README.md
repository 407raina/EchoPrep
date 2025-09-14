# EchoPrep: Voice-Driven Mock Interview Coach

An AI-powered web application that provides realistic, voice-driven mock interview experiences for job seekers. Built with Streamlit and leveraging Google Gemini AI for intelligent question generation and performance analysis.

![EchoPrep](https://img.shields.io/badge/EchoPrep-AI%20Interview%20Coach-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 Features

- **🔐 User Authentication**: Secure registration and login system
- **🎯 Conversational Setup**: AI-powered assistant guides users through interview creation
- **🎙️ Voice-Driven Interviews**: Real-time speech-to-text and text-to-speech capabilities
- **🤖 AI-Powered Questions**: Dynamic question generation based on role and experience
- **📊 Intelligent Feedback**: Comprehensive performance analysis and recommendations
- **📱 Responsive Design**: Works on desktop and mobile devices
- **💾 Progress Tracking**: Save and review past interview sessions

## 🏗️ Architecture

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI/LLM**: Google Gemini API (Free Tier)
- **Speech-to-Text**: Hugging Face Inference API (Whisper)
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Database**: SQLite3
- **Deployment**: Streamlit Community Cloud

### Project Structure

```
echoprep/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── pages/
│   ├── setup.py           # Interview creation/setup page
│   ├── interview.py       # Voice-driven interview interface
│   └── report.py          # AI feedback and performance report
├── utils/
│   ├── database.py        # Database operations
│   ├── auth.py            # Authentication utilities
│   ├── ai_services.py     # AI/LLM integration
│   └── audio_utils.py     # Speech processing utilities
├── data/
│   └── interviews.db      # SQLite database (auto-created)
└── .github/
    └── copilot-instructions.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier)
- Hugging Face API token (optional, for enhanced STT)

### Installation

1. **Clone or download the project**
   ```bash
   cd echoprep
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   AIZASYALDA8KYG3YJE-16JBBEI0S2NGK3ZTOT9W=your_google_gemini_api_key_here
   HF_PEZITYHDXLDXRBETBGGJTOKZQTZAEFXLTN=your_huggingface_api_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`
   - Create an account or login
   - Start your first mock interview!

## 🔑 API Setup

### Google Gemini API (Required)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to your `.env` file as `AIZASYALDA8KYG3YJE-16JBBEI0S2NGK3ZTOT9W`

### Hugging Face API (Optional)

1. Visit [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a new token
3. Add to your `.env` file as `HF_PEZITYHDXLDXRBETBGGJTOKZQTZAEFXLTN`

**Note**: The app will work without Hugging Face API but with limited speech-to-text functionality.

## 💻 Usage Guide

### 1. User Registration/Login
- Create a new account with username and password
- Login to access your personalized dashboard

### 2. Creating Mock Interviews
- Click "Create New Mock Interview"
- Chat with the AI assistant to define:
  - Job role (e.g., "Software Engineer")
  - Experience level (Entry, Mid, Senior)
  - Interview type (Technical, Behavioral, Mixed)
  - Key skills/technologies

### 3. Taking Interviews
- Start your interview from the dashboard
- Listen to AI-generated questions (text-to-speech)
- Respond using:
  - Text input
  - Audio file upload
  - Live microphone (requires additional setup)

### 4. Reviewing Performance
- Get detailed AI-powered feedback
- View performance metrics
- Access improvement recommendations
- Review conversation transcript

## 🎛️ Configuration

### Environment Variables

```bash
# Required
AIZASYALDA8KYG3YJE-16JBBEI0S2NGK3ZTOT9W=your_api_key                    # Google Gemini API key

# Optional
HF_PEZITYHDXLDXRBETBGGJTOKZQTZAEFXLTN=your_token               # Hugging Face API token
DATABASE_PATH=./data/interviews.db             # SQLite database path
APP_TITLE=EchoPrep AI                          # Application title
```

### Audio Settings

The application supports multiple audio input methods:

1. **Text Input**: Always available as fallback
2. **Audio File Upload**: Supports WAV, MP3, OGG formats
3. **Live Recording**: Requires WebRTC setup (advanced)

## 🚀 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your repository
4. Add environment variables in the deployment settings
5. Deploy!

### Local Production

```bash
# Install additional dependencies for production
pip install streamlit[production]

# Run with production settings
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

## 🔧 Development

### Adding New Features

1. **New Interview Types**: Modify `utils/ai_services.py`
2. **Enhanced Audio**: Update `utils/audio_utils.py`
3. **Additional Pages**: Create new files in `pages/`
4. **Database Changes**: Update `utils/database.py`

### Testing

```bash
# Run the application in development mode
streamlit run main.py --server.runOnSave true

# Test with sample data
python -c "from utils.database import init_database; init_database()"
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Interview Mocks Table
```sql
CREATE TABLE interview_mocks (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    job_role TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    interview_type TEXT NOT NULL,
    skills TEXT NOT NULL,
    questions TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Interview Sessions Table
```sql
CREATE TABLE interview_sessions (
    id TEXT PRIMARY KEY,
    interview_mock_id TEXT NOT NULL,
    transcript TEXT,
    feedback TEXT,
    score INTEGER,
    completed_at TIMESTAMP
);
```

## 🎯 Roadmap

- [ ] Live microphone recording with WebRTC
- [ ] Video interview simulation
- [ ] Industry-specific question banks
- [ ] Team/group interview scenarios
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Integration with job boards
- [ ] Multilingual support

## 📝 Troubleshooting

### Common Issues

**1. "No module named 'streamlit'"**
```bash
pip install streamlit
```

**2. "API key not found"**
- Check your `.env` file exists and contains your API keys
- Ensure `.env` is in the same directory as `main.py`

**3. "Database connection error"**
- The `data/` directory will be created automatically
- Check file permissions in your project directory

**4. "Audio playback not working"**
- Try different browsers (Chrome/Firefox recommended)
- Check browser audio permissions
- Ensure speakers/headphones are connected

**5. "Speech-to-text not working"**
- Verify Hugging Face API token is valid
- Check internet connection
- Try uploading smaller audio files

### Performance Tips

- Use Chrome or Firefox for best compatibility
- Ensure stable internet connection for AI services
- Keep audio files under 10MB for faster processing
- Close unused browser tabs to free memory

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

For support, feature requests, or bug reports:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Include error messages and system information

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent question generation and feedback
- **Hugging Face** for speech processing capabilities  
- **Streamlit** for the amazing web framework
- **OpenAI Whisper** for speech-to-text technology
- **Google Text-to-Speech** for audio generation

---

**Happy Interviewing! 🎤✨**

Built with ❤️ for job seekers everywhere.

# InterVue AI 🎯

**AI-Powered Interview Practice Platform**

InterVue AI is a comprehensive full-stack web application that helps users practice interviews with real-time AI analysis. Get instant feedback on your speaking skills, eye contact, voice quality, and answer content using advanced AI technologies.

![InterVue AI](https://img.shields.io/badge/InterVue-AI%20Powered-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)

## ✨ Features

### 🎤 **Real-Time Analysis**
- **Speech-to-Text**: Accurate transcription using Google Speech Recognition
- **Voice Analysis**: Real-time voice stability, clarity, and speaking rate analysis
- **Emotion Detection**: Facial expression and confidence level analysis using OpenCV
- **Eye Contact Tracking**: Camera engagement monitoring with percentage feedback

### 🤖 **AI-Powered Feedback**
- **Fresh Questions**: Dynamic question generation using Gemini AI for every session
- **Answer Rating**: Individual answer scoring (1-10) with detailed AI feedback
- **Comprehensive Analysis**: Overall performance scoring with component breakdowns
- **Personalized Tips**: Actionable improvement suggestions based on your performance

### 📊 **Advanced Analytics**
- **Performance Dashboard**: Visual charts and metrics for all interview aspects
- **Progress Tracking**: Detailed analytics with eye contact, voice, and speech metrics
- **Export Functionality**: Download results in JSON/CSV format
- **Share Results**: Easy sharing of interview performance

### 🎯 **Interview Customization**
- **Multiple Roles**: Software Engineer, HR, Data Analyst, and more
- **Experience Levels**: Tailored questions for Fresher and Experienced candidates
- **Question Count**: Choose 3-10 questions per session
- **Real-Time Feedback**: Instant analysis during and after each response

## 🚀 Live Demo

**🌐 [Try InterVue AI Live](https://intervue-ai-main.vercel.app/)**

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Interactive data visualization
- **Lucide React** - Beautiful icons
- **WebRTC** - Real-time media capture

### Backend
- **FastAPI** - High-performance Python API
- **OpenCV** - Computer vision processing
- **Librosa** - Audio analysis and processing
- **Google Gemini AI** - Question generation
- **SpeechRecognition** - Speech-to-text conversion

### Deployment
- **Vercel** - Serverless deployment platform

## 📋 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/ramandeep-singh77/IntervueAi.git
cd IntervueAi
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your API keys
GEMINI_API_KEY=your_gemini_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start backend server (Port 8000)
python main.py
```

### 4. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server (Port 3000)
npm start
```

### 5. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs



📖 **Detailed deployment guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🎯 How It Works

### 1. **Interview Setup**
- Select role (Software Engineer, HR, Data Analyst)
- Choose experience level (Fresher/Experienced)
- Set number of questions (3-10)
- Test camera and microphone

### 2. **AI Question Generation**
- Gemini AI creates unique questions
- Role and experience-specific content
- Behavioral, technical, and situational questions
- Fallback to curated questions if needed

### 3. **Real-Time Analysis**
- **Audio**: WebM → WAV conversion → Speech analysis
- **Video**: Frame-by-frame face and emotion detection
- **Processing**: Real-time metrics calculation
- **Storage**: Session data management

### 4. **Comprehensive Feedback**
- **Confidence Score**: Multi-factor calculation
- **Detailed Analytics**: Speech, voice, emotion metrics
- **AI Feedback**: Personalized improvement suggestions
- **Export Options**: JSON/CSV reports

## 📊 Analysis Capabilities

### Audio Analysis
- ✅ **Real Speech Recognition**: Google Speech API
- ✅ **Speaking Rate**: Accurate WPM calculation
- ✅ **Filler Word Detection**: "um", "uh", "like" identification
- ✅ **Voice Stability**: Pitch and energy analysis
- ✅ **Silence Detection**: 0 WPM when not speaking

### Video Analysis
- ✅ **Face Detection**: OpenCV Haar cascades
- ✅ **Eye Contact**: Camera engagement measurement
- ✅ **Confidence Metrics**: Facial expression analysis
- ✅ **Position Tracking**: Movement and stability
- ✅ **Privacy First**: Local processing only

## 🔧 Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
DEEPGRAM_API_KEY=your_deepgram_api_key

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

### Customization
- **Questions**: Modify `backend/utils/interview_questions.py`
- **Roles**: Add new roles in question generator
- **Styling**: Update Tailwind classes
- **Analytics**: Extend metrics in analyzers

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md).

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - Question generation
- **OpenCV** - Computer vision capabilities
- **Librosa** - Audio processing
- **React Team** - Frontend framework
- **FastAPI** - Backend framework
- **Vercel** - Deployment platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ramandeep-singh77/IntervueAi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ramandeep-singh77/IntervueAi/discussions)
- **Email**: ramandeepsinghrds2006@gmail.com

## 🎉 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ramandeep-singh77/IntervueAi&type=Date)](https://star-history.com/#ramandeep-singh77/IntervueAi&Date)

---

**Made with ❤️ by [Ramandeep Singh](https://github.com/ramandeep-singh77)**

*Empowering interview success through AI-powered practice and feedback*

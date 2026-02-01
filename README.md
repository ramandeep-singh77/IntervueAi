# InterVue AI 🎯

**AI-Powered Interview Practice Platform**

A comprehensive full-stack web application that helps users practice and improve their interview skills using advanced AI analysis for real-time feedback on confidence, emotions, voice tone, and communication patterns.

![InterVue AI](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/Frontend-React-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)

## 🌟 Features

### 🎥 **Real-Time Video Analysis**
- **Face Detection**: Advanced OpenCV-based facial recognition
- **Eye Contact Tracking**: Measures engagement and confidence
- **Emotion Analysis**: Real-time confidence and nervousness detection
- **Position Stability**: Tracks posture and movement consistency

### 🎤 **Advanced Audio Processing**
- **Speech-to-Text**: Google Speech Recognition integration
- **Speaking Rate Analysis**: Words per minute calculation
- **Filler Word Detection**: Identifies "um", "uh", "like" patterns
- **Voice Stability**: Pitch and energy consistency analysis
- **Real Analysis**: 0 WPM when silent, actual metrics when speaking

### 🤖 **AI-Powered Intelligence**
- **Dynamic Questions**: Gemini AI generates unique questions every session
- **Role-Specific Content**: Tailored for Software Engineer, HR, Data Analyst roles
- **Experience-Based**: Different questions for Fresher vs Experienced levels
- **Personalized Feedback**: AI-generated improvement suggestions

### 📊 **Comprehensive Analytics**
- **Interactive Dashboards**: Real-time performance visualization
- **Confidence Scoring**: Multi-factor confidence calculation
- **Detailed Metrics**: Speech, voice, and emotion analytics
- **Export Functionality**: JSON and CSV report generation
- **Share Results**: Social sharing capabilities

### ⚙️ **Technical Excellence**
- **Serverless Architecture**: Optimized for Vercel deployment
- **Real-Time Processing**: WebRTC for audio/video capture
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: Graceful fallbacks for all scenarios
- **Performance Optimized**: Fast loading and smooth interactions

## 🚀 Live Demo

**🌐 [Try InterVue AI Live](https://intervue-ai.vercel.app)**

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
- **GitHub Actions** - CI/CD pipeline
- **Environment Variables** - Secure configuration

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

# Start backend server
python backend/main.py
```

### 4. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 5. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001

## 🌐 Deployment

### Vercel Deployment (Recommended)

1. **Fork this repository**
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel auto-detects configuration

3. **Set Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ```

4. **Deploy**: Automatic deployment from `vercel.json`

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

# Frontend (Production)
REACT_APP_API_URL=https://intervue-ai.vercel.app/api
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
- **Email**: ramandeep.singh77@example.com

## 🎉 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ramandeep-singh77/IntervueAi&type=Date)](https://star-history.com/#ramandeep-singh77/IntervueAi&Date)

---

**Made with ❤️ by [Ramandeep Singh](https://github.com/ramandeep-singh77)**

*Empowering interview success through AI-powered practice and feedback*
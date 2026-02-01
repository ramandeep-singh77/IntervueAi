# InterVue AI - AI-Powered Interview Practice Platform

🏆 **Hackathon-Ready** | 🤖 **AI-Powered** | 🎯 **Production-Structured**

An intelligent interview practice platform that evaluates confidence, emotion, tone, and communication skills using webcam and audio analysis. Built with cutting-edge AI technologies for comprehensive interview performance assessment.

## 🎯 Core Features

### 🎤 Mock Interview System
- **Role-Based Questions**: Software Engineer, HR Professional, Data Analyst
- **Experience Levels**: Fresher (0-2 years) and Experienced (2+ years)
- **Dynamic Question Generation**: AI-powered questions via Google Gemini
- **Timer-Based Sessions**: Realistic interview simulation

### 📹 Real-Time Analysis
- **WebRTC Integration**: Seamless camera and microphone capture
- **Live Processing**: Real-time audio and video analysis
- **Instant Feedback**: Immediate insights during interview

### 🧠 AI-Powered Assessment
- **Speech-to-Text**: Deepgram API for accurate transcription
- **Emotion Detection**: DeepFace library for facial expression analysis
- **Voice Analysis**: librosa for pitch, energy, and speech pattern analysis
- **Confidence Scoring**: Multi-factor algorithm with explainable results

### 📊 Comprehensive Analytics
- **Performance Dashboard**: Visual insights with Chart.js
- **Detailed Metrics**: Voice stability, eye contact, emotion consistency
- **Personalized Feedback**: AI-generated improvement suggestions
- **Progress Tracking**: Session-based performance monitoring

## 🏗️ Technology Stack

### Frontend
- **React 18**: Modern UI with hooks and context
- **Tailwind CSS**: Responsive, utility-first styling
- **Chart.js**: Interactive data visualizations
- **WebRTC**: Native browser media capture
- **Axios**: HTTP client for API communication

### Backend
- **FastAPI**: High-performance async Python framework
- **Uvicorn**: ASGI server for production deployment
- **Modular Architecture**: Separated services for scalability

### AI/ML Technologies
- **Google Gemini API**: Advanced language model for feedback generation
- **Deepgram API**: Professional-grade speech-to-text
- **DeepFace**: State-of-the-art facial emotion recognition
- **librosa**: Audio analysis and feature extraction

## 🚀 Quick Start

### Automated Setup (Recommended)

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh && ./start.sh
```

### Manual Setup

1. **Prerequisites**:
   - Python 3.8+ with pip
   - Node.js 16+ with npm
   - API keys for Gemini and Deepgram

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

4. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🎯 Demo Flow (Optimized for Judges)

1. **Setup** (30 seconds):
   - Select interview role and experience level
   - Test camera and microphone permissions
   - View real-time video preview

2. **Interview** (2-3 minutes):
   - Answer 1-2 AI-generated questions
   - Real-time emotion detection visible
   - Live transcription display

3. **Analysis** (1 minute):
   - Comprehensive confidence scoring
   - Detailed performance breakdown
   - AI-generated feedback and insights

4. **Results Dashboard** (1 minute):
   - Interactive analytics charts
   - Personalized improvement recommendations
   - Exportable performance reports

## 📊 Confidence Scoring Algorithm

Our proprietary scoring system evaluates multiple factors:

- **Voice Stability (40%)**: Pitch consistency, energy levels, speaking rate
- **Eye Contact (25%)**: Camera engagement, face detection consistency
- **Emotion Consistency (20%)**: Confidence vs. nervousness indicators
- **Filler Word Frequency (15%)**: "Um", "uh", "like" detection and scoring

**Score Ranges**:
- 85-100: Excellent (Outstanding confidence)
- 70-84: Good (Strong performance)
- 55-69: Average (Room for improvement)
- 40-54: Below Average (Significant development needed)
- 0-39: Poor (Major improvement required)

## 🔧 API Architecture

### Core Endpoints
- `POST /api/interview/start` - Initialize session with role-specific questions
- `POST /api/analyze/audio` - Process speech-to-text and voice metrics
- `POST /api/analyze/video` - Analyze facial expressions and emotions
- `GET /api/feedback/{session_id}` - Generate comprehensive AI feedback
- `GET /api/session/{session_id}` - Retrieve session data and progress

### Service Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │────│   FastAPI Backend │────│   AI Services   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
    ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
    │ WebRTC  │              │ Session │              │ Gemini  │
    │ Media   │              │ Manager │              │   API   │
    └─────────┘              └─────────┘              └─────────┘
                                   │                        │
                              ┌────▼────┐              ┌────▼────┐
                              │ Analysis│              │Deepgram │
                              │ Engine  │              │   API   │
                              └─────────┘              └─────────┘
```

## 🎨 User Experience

### Modern, Intuitive Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Accessibility**: WCAG 2.1 compliant components
- **Real-time Feedback**: Live indicators and progress tracking
- **Professional Aesthetics**: Clean, modern design suitable for professional use

### Performance Optimizations
- **Lazy Loading**: Components loaded on demand
- **Efficient State Management**: Optimized React hooks and context
- **Caching**: API responses cached for better performance
- **Error Handling**: Graceful degradation and user-friendly error messages

## 🔒 Security & Privacy

- **No Data Persistence**: Recordings processed and deleted immediately
- **API Key Security**: Environment-based configuration
- **CORS Protection**: Configured for development and production
- **Input Validation**: Comprehensive request validation and sanitization

## 📈 Scalability Features

### Modular Backend Architecture
- **Service Separation**: Independent modules for each analysis type
- **Async Processing**: Non-blocking API endpoints
- **Error Isolation**: Failures in one service don't affect others
- **Easy Extension**: Simple to add new analysis types or AI models

### Production-Ready
- **Docker Support**: Containerized deployment ready
- **Environment Configuration**: Separate dev/staging/production configs
- **Monitoring**: Structured logging and error tracking
- **Performance**: Optimized for concurrent users

## 🏆 Hackathon Highlights

### Technical Innovation
- **Multi-Modal AI Analysis**: Combines video, audio, and text processing
- **Real-Time Processing**: Live analysis during interview simulation
- **Advanced Scoring Algorithm**: Proprietary confidence assessment
- **Modern Tech Stack**: Latest versions of React, FastAPI, and AI APIs

### Business Value
- **Market Ready**: Addresses real need in interview preparation
- **Scalable Solution**: Architecture supports growth to thousands of users
- **Monetization Potential**: Premium features, enterprise licensing
- **Social Impact**: Democratizes access to interview coaching

### Demo Excellence
- **Quick Setup**: Automated installation and configuration
- **Reliable Performance**: Fallback systems for demo stability
- **Visual Impact**: Impressive real-time analysis and dashboards
- **Judge-Friendly**: Clear value proposition and technical depth

## 📚 Documentation

- **[Setup Guide](SETUP.md)**: Detailed installation and configuration
- **[API Documentation](http://localhost:8000/docs)**: Interactive API explorer
- **[Architecture Overview](docs/architecture.md)**: System design and components
- **[Deployment Guide](docs/deployment.md)**: Production deployment instructions

## 🤝 Contributing

This project is structured for easy contribution and extension:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini**: Advanced AI language model
- **Deepgram**: Professional speech-to-text API
- **DeepFace**: Open-source facial recognition library
- **React Team**: Excellent frontend framework
- **FastAPI**: High-performance Python web framework

---

**Built with ❤️ for the hackathon community**

*InterVue AI - Where AI meets interview excellence*
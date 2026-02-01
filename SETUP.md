# InterVue AI - Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **API Keys**:
  - Google Gemini API Key
  - Deepgram API Key

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd intervue-ai

# Copy environment file
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` file and add your API keys:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
DEEPGRAM_API_KEY=your_actual_deepgram_api_key_here
```

### 3. Automated Setup (Recommended)

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 4. Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm start
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Configuration

### API Keys Setup

#### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`

#### Deepgram API
1. Sign up at [Deepgram](https://console.deepgram.com/)
2. Create a new API key
3. Add to `.env` as `DEEPGRAM_API_KEY`

### Browser Requirements

- **Chrome/Edge**: Recommended (best WebRTC support)
- **Firefox**: Supported
- **Safari**: Limited support
- **HTTPS**: Required for production (camera/mic access)

## 🧪 Testing the Application

### 1. System Check
- Visit http://localhost:3000
- Check that both frontend and backend are running
- Verify API health status on setup page

### 2. Camera/Microphone Test
1. Go to "Practice Interview" page
2. Click "Test Camera & Microphone"
3. Grant permissions when prompted
4. Verify video preview appears

### 3. Interview Flow Test
1. Select a role (e.g., "Software Engineer")
2. Choose experience level ("Fresher" or "Experienced")
3. Start interview
4. Record a short answer (10-15 seconds)
5. Check that analysis appears
6. Complete interview to see results

### 4. API Testing
Visit http://localhost:8000/docs for interactive API documentation.

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies manually
cd backend
pip install -r requirements.txt

# Check for missing dependencies
pip list
```

#### Frontend Won't Start
```bash
# Check Node.js version
node --version  # Should be 16+

# Clear npm cache
npm cache clean --force

# Install dependencies
cd frontend
npm install
```

#### Camera/Microphone Issues
- **Chrome**: Go to Settings > Privacy > Camera/Microphone
- **Firefox**: Click camera icon in address bar
- **HTTPS Required**: Use `https://localhost:3000` in production

#### API Key Issues
- Verify keys are correctly set in `.env`
- Check API key permissions and quotas
- Restart backend after changing `.env`

#### Analysis Failures
- Check backend logs for detailed errors
- Verify all Python dependencies are installed
- Ensure sufficient disk space for temporary files

### Performance Issues

#### Slow Analysis
- **Video Analysis**: Can take 30-60 seconds for longer recordings
- **Audio Analysis**: Usually completes in 10-20 seconds
- **Feedback Generation**: May take 20-30 seconds

#### Memory Usage
- **DeepFace**: Requires ~2GB RAM for model loading
- **Video Processing**: Additional 1-2GB during analysis
- **Recommended**: 8GB+ RAM for smooth operation

## 📁 Project Structure

```
intervue-ai/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main application entry
│   ├── stt/                # Speech-to-text services
│   ├── emotion_detection/  # Facial emotion analysis
│   ├── voice_analysis/     # Voice pattern analysis
│   ├── scoring_engine/     # Confidence scoring
│   ├── feedback_generator/ # AI feedback generation
│   └── utils/              # Utilities and helpers
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   └── services/       # API and media services
│   └── public/             # Static assets
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🔒 Security Notes

- **API Keys**: Never commit real API keys to version control
- **HTTPS**: Required for camera/microphone access in production
- **CORS**: Configured for localhost development only
- **File Upload**: Temporary files are cleaned up automatically

## 🚀 Production Deployment

### Environment Variables
```env
# Production settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
REACT_APP_API_URL=https://your-domain.com/api
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### HTTPS Setup
- Use reverse proxy (nginx/Apache)
- SSL certificate required for camera/microphone
- Update CORS settings for production domain

## 📊 Demo Data

For hackathon demonstrations:

1. **Quick Demo**: Use 10-15 second responses
2. **Sample Questions**: Pre-loaded for each role
3. **Mock Analysis**: Fallback data if APIs fail
4. **Performance Metrics**: Realistic scoring ranges

## 🆘 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review backend logs in terminal
3. Check browser console for frontend errors
4. Verify API key validity and quotas
5. Ensure all dependencies are installed

## 📈 Performance Optimization

### For Demos
- Pre-warm AI models by running a test analysis
- Use shorter recordings (10-30 seconds)
- Close unnecessary browser tabs
- Ensure stable internet connection

### For Development
- Use development API keys with higher quotas
- Enable debug logging in backend
- Use browser dev tools for frontend debugging
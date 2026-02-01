# 🚂 InterVue AI - Railway Deployment Guide

## 🌟 **Why Railway?**

Railway is perfect for InterVue AI because it:
- ✅ **Supports full-stack apps** with both Python backend and React frontend
- ✅ **Handles AI/ML libraries** like OpenCV, librosa, numpy seamlessly
- ✅ **Auto-scales** based on usage
- ✅ **Built-in PostgreSQL** for production database
- ✅ **Simple deployment** from GitHub with zero config
- ✅ **Environment variables** management
- ✅ **Custom domains** and SSL certificates

## 📋 **Prerequisites**

1. **GitHub Repository**: Code pushed to GitHub
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **API Keys**: 
   - Google Gemini API Key (for AI question generation)
   - Deepgram API Key (for advanced speech recognition)

## 🚀 **Deployment Steps**

### **1. Connect GitHub Repository**

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose repository: `ramandeep-singh77/IntervueAi`
5. Railway will auto-detect the Dockerfile and start building

### **2. Configure Environment Variables**

In Railway dashboard → **Variables** tab, add:

**🔑 Required API Keys:**
```
GEMINI_API_KEY=your_google_gemini_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

**🔧 Optional Configuration:**
```
PORT=8000
PYTHONPATH=/app
NODE_ENV=production
```

### **3. Build Process (Automatic)**

Railway will automatically:
- ✅ **Use Dockerfile** for consistent builds
- ✅ **Install Python 3.9** and system dependencies
- ✅ **Install Node.js 18** for frontend building
- ✅ **Install FFmpeg** for audio processing
- ✅ **Install Python dependencies** from `requirements.txt`
- ✅ **Install Node.js dependencies** from `frontend/package.json`
- ✅ **Build React frontend** with `npm run build`
- ✅ **Start FastAPI server** with `python start_railway.py`

## 🔧 **Fixed Issues**

### **✅ Frontend Build Process**
- **Enhanced Dockerfile**: Better build verification and error handling
- **Improved railway.json**: Uses dockerfile builder for consistency
- **Build Verification**: Checks if frontend build exists and is valid
- **Startup Script**: `start_railway.py` ensures robust deployment

### **✅ Frontend Serving**
- **Static File Serving**: Properly configured for React Router
- **API Integration**: Correct API URLs for production
- **Error Handling**: Graceful fallback if frontend build fails
- **Debug Information**: Detailed logging for troubleshooting

## 🎯 **What Gets Deployed**

### **🎨 Frontend (React)**
- **Built from**: `/frontend` directory
- **Served as**: Static files integrated with FastAPI
- **Available at**: Root URL (`/`)
- **Features**: Complete interview practice interface

### **🤖 Backend (FastAPI + AI)**
- **Real Audio Analysis**: librosa, SpeechRecognition, FFmpeg
- **Real Video Analysis**: OpenCV, face detection, emotion analysis
- **AI Question Generation**: Google Gemini AI integration
- **Advanced Speech Recognition**: Deepgram API integration
- **API Endpoints**: Available at `/api/*`

## 🌐 **Available Features**

### **🔥 Full AI-Powered Analysis**
- ✅ **Real Speech Recognition** - Actual transcription and WPM calculation
- ✅ **Voice Analysis** - Pitch, energy, stability, filler word detection
- ✅ **Face Detection** - Real-time facial recognition with OpenCV
- ✅ **Eye Contact Tracking** - Camera engagement measurement
- ✅ **Emotion Analysis** - Confidence and nervousness detection
- ✅ **AI Question Generation** - Dynamic questions using Gemini AI

### **📊 Advanced Analytics**
- ✅ **Interactive Dashboards** - Real-time performance visualization
- ✅ **Comprehensive Metrics** - Speech, voice, and emotion analytics
- ✅ **Export Functionality** - JSON and CSV report generation
- ✅ **Progress Tracking** - Session history and improvement trends

## 🔗 **API Endpoints**

### **Frontend Routes**
- `/` - Homepage
- `/setup` - Interview setup
- `/interview/:sessionId` - Interview session
- `/results/:sessionId` - Results and analytics

### **Backend API**
- `GET /api/health` - Health check with system status
- `POST /api/interview/start` - Start interview with AI questions
- `POST /api/analyze/audio` - Real audio analysis
- `POST /api/analyze/video` - Real video analysis
- `GET /api/feedback/{session_id}` - AI-generated feedback
- `GET /api/export/{session_id}` - Export results
- `GET /api/roles` - Available interview roles
- `GET /api/experience-levels` - Experience levels

## 🔍 **Testing Your Deployment**

After deployment, test these URLs:

1. **🏠 Homepage**: `https://your-app-name.up.railway.app`
2. **🔧 API Health**: `https://your-app-name.up.railway.app/api/health`
3. **🎯 Start Interview**: Test the complete interview flow
4. **📊 Analytics**: Verify real-time analysis features

## 🐛 **Troubleshooting**

### **Build Issues**
- **Check build logs** in Railway dashboard
- **Verify dependencies** in `requirements.txt` and `package.json`
- **Frontend build verification** - Look for "✅ Frontend build found" in logs

### **Frontend Not Loading**
- **Check build directory** - Should contain `index.html` and `static/` folder
- **Verify API URLs** - Frontend should use relative URLs in production
- **Check browser console** - Look for 404 errors or API failures

### **API Key Issues**
- **Verify environment variables** are set correctly in Railway dashboard
- **Test API keys** independently before deployment
- **Check logs** for authentication errors

### **Performance Issues**
- **Monitor resource usage** in Railway dashboard
- **Scale up** if needed (Railway auto-scales)
- **Check database connections** if using PostgreSQL

## 🚀 **Production Optimizations**

### **Database Integration**
```python
# Add PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Use PostgreSQL instead of in-memory storage
    pass
```

### **File Storage**
```python
# Use Railway's persistent storage or cloud storage
UPLOAD_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "/tmp")
```

### **Caching**
```python
# Add Redis for session caching
REDIS_URL = os.getenv("REDIS_URL")
```

## 📊 **Monitoring & Analytics**

### **Railway Dashboard**
- **📈 Metrics**: CPU, memory, network usage
- **📋 Logs**: Real-time application logs
- **🔄 Deployments**: Build and deployment history
- **⚙️ Settings**: Environment variables and scaling

### **Application Health**
- **Health Check**: `/api/health` endpoint
- **Status Monitoring**: Automatic restart on failures
- **Performance Metrics**: Response times and error rates

## 🔒 **Security Features**

- **🔐 HTTPS**: Automatic SSL certificates
- **🛡️ Environment Variables**: Secure API key storage
- **🚫 CORS**: Configured for production domain
- **🔒 Input Validation**: FastAPI automatic validation

## 💰 **Pricing & Scaling**

### **Railway Pricing**
- **🆓 Free Tier**: $5 credit monthly (perfect for testing)
- **💳 Pro Plan**: Pay-as-you-use (scales automatically)
- **📊 Usage-based**: CPU, memory, network, storage

### **Auto-scaling**
- **🔄 Automatic**: Scales based on traffic
- **⚡ Fast**: Sub-second scaling
- **💰 Cost-effective**: Pay only for what you use

## 🎉 **Go Live!**

Your InterVue AI will be available at:
**🌐 `https://your-app-name.up.railway.app`**

## 📞 **Support**

- **📚 Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **💬 Railway Discord**: Community support
- **🐛 GitHub Issues**: [Project Issues](https://github.com/ramandeep-singh77/IntervueAi/issues)

---

**🎯 Ready to deploy? Just push to GitHub and Railway handles the rest!**

**Made with ❤️ for seamless AI-powered interview practice**
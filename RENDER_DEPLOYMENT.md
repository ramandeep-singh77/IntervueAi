# 🚀 InterVue AI - Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Repository**: Code pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)

## 🔧 Deployment Steps

### 1. Connect GitHub Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select repository: `ramandeep-singh77/IntervueAi`

### 2. Configure Web Service

**Basic Settings:**
- **Name**: `intervue-ai`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy Settings:**

**Build Command:**
```bash
pip install -r requirements.txt && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs && cd frontend && npm install && npm run build && cd ..
```

**Start Command:**
```bash
python main.py
```

### 3. Environment Variables (Optional)

**Required:**
- `PORT`: `10000` (Render sets this automatically)

**Optional (for AI features):**
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEEPGRAM_API_KEY`: Your Deepgram API key

### 4. Advanced Settings

- **Auto-Deploy**: `Yes` (deploys on git push)
- **Health Check Path**: `/api/health`

## 🌐 What Gets Deployed

### **Frontend (React)**
- Built from `/frontend` directory
- Served as static files
- Available at root URL (`/`)

### **Backend (FastAPI)**
- Python API server
- Available at `/api/*` endpoints
- Handles all interview functionality

## 🎯 Available Endpoints

### **Frontend Routes**
- `/` - Homepage
- `/setup` - Interview setup
- `/interview/:sessionId` - Interview session
- `/results/:sessionId` - Results page

### **API Endpoints**
- `GET /api/health` - Health check
- `POST /api/interview/start` - Start interview
- `POST /api/analyze/audio` - Audio analysis
- `POST /api/analyze/video` - Video analysis
- `GET /api/feedback/{session_id}` - Get feedback
- `GET /api/export/{session_id}` - Export results

## ✅ Features Available

### **Demo Mode (No API Keys Required)**
- ✅ Dynamic question generation
- ✅ Audio analysis with realistic metrics
- ✅ Video analysis with face detection simulation
- ✅ Comprehensive feedback generation
- ✅ Export functionality (JSON/CSV)
- ✅ Interactive analytics dashboard

### **Full Mode (With API Keys)**
- ✅ All demo features +
- ✅ AI-powered question generation (Gemini)
- ✅ Advanced speech recognition (Deepgram)
- ✅ Real-time analysis capabilities

## 🔍 Testing Deployment

After deployment, test these URLs:

1. **Frontend**: `https://your-app-name.onrender.com`
2. **API Health**: `https://your-app-name.onrender.com/api/health`
3. **Start Interview**: Test the interview flow

## 🐛 Troubleshooting

### **Build Fails**
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Try the alternative build command below

### **Alternative Build Command (if above fails):**
```bash
pip install -r requirements.txt && apt-get update && apt-get install -y curl && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs && cd frontend && npm install && npm run build && cd ..
```

### **Frontend Not Loading**
- Check if `frontend/build` directory exists
- Verify React build completed successfully
- Check browser console for errors

### **API Errors**
- Check application logs in Render dashboard
- Verify environment variables are set
- Test API endpoints directly

## 🚀 Performance Optimization

### **For Production**
1. **Database**: Replace in-memory storage with PostgreSQL
2. **File Storage**: Use cloud storage for audio/video files
3. **Caching**: Implement Redis for session management
4. **CDN**: Use Render's CDN for static assets

## 📊 Monitoring

- **Health Check**: `/api/health` endpoint
- **Logs**: Available in Render dashboard
- **Metrics**: Monitor response times and errors

## 🔒 Security

- **CORS**: Configured for production domain
- **Environment Variables**: Secure API key storage
- **HTTPS**: Automatic SSL certificate

---

**🎉 Your InterVue AI application will be live at:**
`https://your-app-name.onrender.com`

**📧 Support**: Check GitHub issues for help and updates.
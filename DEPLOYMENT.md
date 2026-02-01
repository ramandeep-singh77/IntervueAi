# InterVue AI - Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **API Keys**: Obtain your API keys:
   - `GEMINI_API_KEY`: From Google AI Studio
   - `DEEPGRAM_API_KEY`: From Deepgram (optional)

## Deployment Steps

### 1. Connect to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository containing InterVue AI

### 2. Configure Environment Variables

In Vercel dashboard, go to your project settings and add these environment variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here (optional)
```

### 3. Update Frontend API URL

After deployment, update `frontend/.env.production`:

```
REACT_APP_API_URL=https://your-actual-vercel-url.vercel.app/api
```

Replace `your-actual-vercel-url` with your actual Vercel deployment URL.

### 4. Deploy

1. Vercel will automatically detect the configuration from `vercel.json`
2. The build process will:
   - Build the React frontend
   - Deploy the Python backend as serverless functions
   - Set up routing between frontend and API

### 5. Test Deployment

1. Visit your Vercel URL
2. Test all features:
   - Interview setup
   - Audio/video recording
   - Analysis results
   - Export functionality

## Project Structure for Vercel

```
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
├── frontend/
│   ├── package.json           # Frontend dependencies
│   ├── .env.production        # Production environment
│   └── src/                   # React source code
└── backend/
    └── api/
        └── index.py           # Serverless API entry point
```

## Serverless Considerations

### Limitations
- **Cold Starts**: First request may be slower
- **Memory Limits**: 1GB RAM limit for free tier
- **Execution Time**: 10s limit for free tier, 60s for pro
- **File Storage**: Use `/tmp` for temporary files only

### Optimizations Applied
- **Lightweight Dependencies**: Using `opencv-python-headless`
- **Error Handling**: Graceful fallbacks when ML libraries fail
- **Efficient Imports**: Conditional imports to reduce cold start time
- **Memory Management**: Automatic cleanup of temporary files

### Fallback Behavior
If ML analysis fails in serverless environment:
- Audio analysis returns basic metrics
- Video analysis returns placeholder data
- Core functionality (questions, UI) continues to work
- User experience remains smooth

## Monitoring

### Check Deployment Status
1. Vercel Dashboard → Your Project → Functions
2. Monitor function execution times and errors
3. Check logs for any issues

### Performance Tips
1. **Warm-up**: First request may be slow due to cold start
2. **File Size**: Keep uploaded files reasonable (<10MB)
3. **Timeout**: Increase function timeout if needed (Pro plan)

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Check if all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **API Timeouts**
   - Increase timeout in `vercel.json`
   - Optimize ML processing code

3. **CORS Issues**
   - Verify API URL in frontend environment variables
   - Check CORS configuration in backend

4. **Environment Variables**
   - Ensure all required env vars are set in Vercel dashboard
   - Check variable names match exactly

### Debug Steps

1. Check Vercel function logs
2. Test API endpoints directly
3. Verify frontend can reach backend
4. Test with smaller files first

## Production Recommendations

### For High Traffic
1. **Upgrade to Pro Plan**: Higher limits and better performance
2. **Use Database**: Replace in-memory sessions with Redis/PostgreSQL
3. **CDN**: Use Vercel's edge network for static assets
4. **Monitoring**: Set up error tracking and performance monitoring

### Security
1. **Environment Variables**: Never commit API keys to code
2. **CORS**: Restrict to your domain in production
3. **Rate Limiting**: Implement API rate limiting
4. **File Validation**: Validate uploaded file types and sizes

## Cost Optimization

### Free Tier Limits
- 100GB bandwidth/month
- 100 serverless function invocations/day
- 10s execution time limit

### Pro Tier Benefits
- Unlimited bandwidth
- 1000 serverless function invocations/day
- 60s execution time limit
- Better performance and priority support

## Support

If you encounter issues:
1. Check Vercel documentation
2. Review function logs in Vercel dashboard
3. Test locally first to isolate issues
4. Consider the serverless limitations mentioned above

The application is designed to work reliably in serverless environments with appropriate fallbacks for all critical functionality.
/**
 * API Service for InterVue AI
 * Handles all communication with the backend FastAPI server
 */

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || (
    process.env.NODE_ENV === 'production' 
      ? '/api' 
      : 'http://localhost:8000/api'
  ),
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    
    // Handle specific error cases
    if (error.response?.status === 404) {
      console.error('Resource not found');
    } else if (error.response?.status === 500) {
      console.error('Server error');
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    }
    
    return Promise.reject(error);
  }
);

/**
 * Interview API endpoints
 */
export const interviewAPI = {
  /**
   * Start a new interview session
   * @param {string} role - Interview role
   * @param {string} experienceLevel - Experience level
   * @param {number} numQuestions - Number of questions (default: 5)
   * @returns {Promise} Session data with questions
   */
  startInterview: async (role, experienceLevel, numQuestions = 5) => {
    const formData = new FormData();
    formData.append('role', role);
    formData.append('experience_level', experienceLevel);
    formData.append('num_questions', numQuestions.toString());
    
    const response = await api.post('/api/interview/start', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Get session data
   * @param {string} sessionId - Session ID
   * @returns {Promise} Session data
   */
  getSession: async (sessionId) => {
    const response = await api.get(`/api/session/${sessionId}`);
    return response.data;
  },
};

/**
 * Analysis API endpoints
 */
export const analysisAPI = {
  /**
   * Analyze audio recording
   * @param {string} sessionId - Session ID
   * @param {number} questionIndex - Question index
   * @param {Blob} audioBlob - Audio recording blob
   * @returns {Promise} Audio analysis results
   */
  analyzeAudio: async (sessionId, questionIndex, audioBlob) => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('question_index', questionIndex);
    formData.append('audio_file', audioBlob, 'recording.wav');
    
    const response = await api.post('/api/analyze/audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 seconds for audio processing
    });
    return response.data;
  },

  /**
   * Analyze video recording
   * @param {string} sessionId - Session ID
   * @param {number} questionIndex - Question index
   * @param {Blob} videoBlob - Video recording blob
   * @returns {Promise} Video analysis results
   */
  analyzeVideo: async (sessionId, questionIndex, videoBlob) => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('question_index', questionIndex);
    formData.append('video_file', videoBlob, 'recording.webm');
    
    const response = await api.post('/api/analyze/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 120000, // 120 seconds for video processing
    });
    return response.data;
  },
};

/**
 * Feedback API endpoints
 */
export const feedbackAPI = {
  /**
   * Get comprehensive feedback for a session
   * @param {string} sessionId - Session ID
   * @returns {Promise} Feedback and analytics data
   */
  getFeedback: async (sessionId) => {
    const response = await api.get(`/api/feedback/${sessionId}`, {
      timeout: 60000, // 60 seconds for feedback generation
    });
    return response.data;
  },
};

/**
 * Utility functions
 */
export const apiUtils = {
  /**
   * Check if API is healthy
   * @returns {Promise<boolean>} API health status
   */
  checkHealth: async () => {
    try {
      const response = await api.get('/', { timeout: 5000 });
      return response.status === 200;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  },

  /**
   * Convert blob to base64
   * @param {Blob} blob - Blob to convert
   * @returns {Promise<string>} Base64 string
   */
  blobToBase64: (blob) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  },

  /**
   * Create audio blob from MediaRecorder
   * @param {MediaRecorder} mediaRecorder - MediaRecorder instance
   * @returns {Promise<Blob>} Audio blob
   */
  createAudioBlob: (chunks) => {
    return new Blob(chunks, { type: 'audio/wav' });
  },

  /**
   * Create video blob from MediaRecorder
   * @param {Array} chunks - Recorded chunks
   * @returns {Blob} Video blob
   */
  createVideoBlob: (chunks) => {
    return new Blob(chunks, { type: 'video/webm' });
  },

  /**
   * Format error message for display
   * @param {Error} error - Error object
   * @returns {string} Formatted error message
   */
  formatError: (error) => {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    } else if (error.response?.data?.message) {
      return error.response.data.message;
    } else if (error.message) {
      return error.message;
    } else {
      return 'An unexpected error occurred';
    }
  },

  /**
   * Retry API call with exponential backoff
   * @param {Function} apiCall - API call function
   * @param {number} maxRetries - Maximum number of retries
   * @param {number} baseDelay - Base delay in milliseconds
   * @returns {Promise} API call result
   */
  retryApiCall: async (apiCall, maxRetries = 3, baseDelay = 1000) => {
    let lastError;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await apiCall();
      } catch (error) {
        lastError = error;
        
        if (attempt === maxRetries) {
          break;
        }
        
        // Exponential backoff
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`API call failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${maxRetries + 1})`);
        
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
    
    throw lastError;
  },
};

/**
 * Export API endpoints
 */
export const exportAPI = {
  /**
   * Export interview results
   * @param {string} sessionId - Session ID
   * @param {string} format - Export format ('json' or 'csv')
   * @returns {Promise} Export data
   */
  exportResults: async (sessionId, format = 'json') => {
    const response = await api.get(`/api/export/${sessionId}?format=${format}`, {
      timeout: 30000, // 30 seconds for export generation
    });
    return response.data;
  },
};

/**
 * Configuration API endpoints
 */
export const configAPI = {
  /**
   * Get available interview roles
   * @returns {Promise} Available roles
   */
  getRoles: async () => {
    const response = await api.get('/api/roles');
    return response.data;
  },

  /**
   * Get available experience levels
   * @returns {Promise} Available experience levels
   */
  getExperienceLevels: async () => {
    const response = await api.get('/api/experience-levels');
    return response.data;
  },
};

export default api;
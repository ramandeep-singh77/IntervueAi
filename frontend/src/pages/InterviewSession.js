import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { 
  Camera, 
  Mic, 
  Square, 
  Play, 
  Pause,
  SkipForward,
  Clock,
  AlertCircle,
  CheckCircle,
  Brain
} from 'lucide-react';
import { useMedia } from '../contexts/MediaContext';
import { analysisAPI, interviewAPI, apiUtils } from '../services/api';
import { sessionStorage } from '../utils/sessionStorage';
import VideoPreview from '../components/VideoPreview';

const InterviewSession = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Use media context
  const { mediaService, stream, initializeMedia } = useMedia();
  
  // Try to get session data from localStorage first, then from navigation state
  const [sessionInfo, setSessionInfo] = useState(() => {
    return sessionStorage.getSessionData(sessionId) || location.state?.sessionData || null;
  });
  
  // Session state
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [questions, setQuestions] = useState(sessionInfo?.questions || []);
  
  // Recording state
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [recordingTimer, setRecordingTimer] = useState(null);
  
  // Analysis state
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [realTimeEmotions, setRealTimeEmotions] = useState([]);
  
  // UI state
  const [error, setError] = useState('');
  const [showTranscript, setShowTranscript] = useState(false);
  
  // Refs
  const videoRef = useRef(null);
  const recordedChunks = useRef([]);

  useEffect(() => {
    if (!sessionInfo) {
      // If no session data, try to fetch it or redirect to setup
      if (sessionId) {
        fetchSessionData();
      } else {
        navigate('/setup');
      }
      return;
    }

    // Initialize media if not already available
    if (!stream && mediaService) {
      initializeMediaForSession();
    }
    
    return () => {
      cleanup();
    };
  }, [sessionId, sessionInfo, navigate, stream, mediaService]);

  const initializeMediaForSession = async () => {
    try {
      if (!stream) {
        await initializeMedia();
      }
    } catch (error) {
      console.error('Failed to initialize media for session:', error);
      setError('Failed to access camera/microphone. Please check permissions.');
    }
  };

  useEffect(() => {
    // Update timer
    let interval;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const fetchSessionData = async () => {
    try {
      const data = await interviewAPI.getSession(sessionId);
      setSessionInfo(data);
      setQuestions(data.questions || []);
      setCurrentQuestionIndex(data.current_question || 0);
    } catch (error) {
      console.error('Failed to fetch session data:', error);
      setError('Failed to load interview session. Please try again.');
      setTimeout(() => navigate('/setup'), 3000);
    }
  };

  const startRecording = async () => {
    if (!mediaService) {
      setError('Media service not available');
      return;
    }

    try {
      setError('');
      setIsRecording(true);
      setRecordingTime(0);
      recordedChunks.current = [];
      
      // Start recording both audio and video
      await mediaService.startRecording('both');
      
      console.log('Recording started for question:', currentQuestionIndex);
    } catch (error) {
      console.error('Failed to start recording:', error);
      setError('Failed to start recording. Please try again.');
      setIsRecording(false);
    }
  };

  const stopRecording = async () => {
    if (!mediaService || !isRecording) {
      return;
    }

    try {
      setIsRecording(false);
      setIsAnalyzing(true);
      
      // Stop recording and get blob
      const recordingBlob = await mediaService.stopRecording();
      
      console.log('Recording stopped. Blob size:', recordingBlob.size);
      
      // Analyze the recording
      await analyzeRecording(recordingBlob);
      
    } catch (error) {
      console.error('Failed to stop recording:', error);
      setError('Failed to process recording. Please try again.');
      setIsAnalyzing(false);
    }
  };

  const analyzeRecording = async (recordingBlob) => {
    try {
      // Split blob into audio and video for separate analysis
      // For demo purposes, we'll send the same blob to both endpoints
      
      // Analyze audio (speech-to-text and voice metrics)
      const audioAnalysisPromise = analysisAPI.analyzeAudio(
        sessionId, 
        currentQuestionIndex, 
        recordingBlob
      );
      
      // Analyze video (emotion detection)
      const videoAnalysisPromise = analysisAPI.analyzeVideo(
        sessionId, 
        currentQuestionIndex, 
        recordingBlob
      );
      
      // Wait for both analyses to complete
      const [audioResults, videoResults] = await Promise.all([
        audioAnalysisPromise,
        videoAnalysisPromise
      ]);
      
      console.log('Analysis completed:', { audioResults, videoResults });
      
      // Combine results
      const combinedAnalysis = {
        transcript: audioResults.transcript,
        voice_metrics: audioResults.voice_metrics,
        emotion_analysis: videoResults.emotion_analysis,
        answer_rating: audioResults.answer_rating, // Add answer rating from audio analysis
        timestamp: new Date().toISOString()
      };
      
      setCurrentAnalysis(combinedAnalysis);
      
      // Show transcript if available
      if (audioResults.transcript && audioResults.transcript.transcript) {
        setShowTranscript(true);
      }
      
      // Move to next question after a delay
      setTimeout(() => {
        nextQuestion();
      }, 3000);
      
    } catch (error) {
      console.error('Analysis failed:', error);
      setError(`Analysis failed: ${apiUtils.formatError(error)}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setCurrentAnalysis(null);
      setShowTranscript(false);
      setRecordingTime(0);
    } else {
      // Interview completed, navigate to results
      navigate(`/results/${sessionId}`);
    }
  };

  const skipQuestion = () => {
    if (isRecording) {
      stopRecording();
    } else {
      nextQuestion();
    }
  };

  const cleanup = () => {
    if (recordingTimer) {
      clearInterval(recordingTimer);
    }
    if (mediaService && isRecording) {
      mediaService.stopRecording().catch(console.error);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getCurrentQuestion = () => {
    return questions[currentQuestionIndex];
  };

  const getProgressPercentage = () => {
    return ((currentQuestionIndex + 1) / questions.length) * 100;
  };

  if (!sessionInfo || questions.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading interview session...</p>
        </div>
      </div>
    );
  }

  const currentQuestion = getCurrentQuestion();

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {sessionInfo.role} Interview
            </h1>
            <p className="text-gray-600">
              {sessionInfo.experience_level} Level • Question {currentQuestionIndex + 1} of {questions.length}
            </p>
          </div>
          
          <div className="text-right">
            <div className="text-sm text-gray-500">Progress</div>
            <div className="text-lg font-semibold text-primary-600">
              {Math.round(getProgressPercentage())}%
            </div>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full progress-bar"
            style={{ width: `${getProgressPercentage()}%` }}
          ></div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - Video and Controls */}
        <div className="lg:col-span-2 space-y-6">
          {/* Video Preview */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="aspect-video bg-gray-900 rounded-lg overflow-hidden relative">
              <VideoPreview 
                stream={stream}
                className="w-full h-full"
                showPlaceholder={true}
              />
              
              {/* Recording Indicator */}
              {isRecording && (
                <div className="absolute top-4 left-4 flex items-center bg-red-600 text-white px-3 py-1 rounded-full recording-pulse">
                  <div className="w-2 h-2 bg-white rounded-full mr-2"></div>
                  <span className="text-sm font-medium">REC {formatTime(recordingTime)}</span>
                </div>
              )}
              
              {/* Analysis Indicator */}
              {isAnalyzing && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                  <div className="text-center text-white">
                    <Brain className="w-12 h-12 mx-auto mb-4 animate-pulse" />
                    <p className="text-lg font-medium">Analyzing your response...</p>
                    <p className="text-sm opacity-75">This may take a moment</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Controls */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-center space-x-4">
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  disabled={isAnalyzing}
                  className="flex items-center px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Play className="w-5 h-5 mr-2" />
                  Start Recording
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="flex items-center px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors"
                >
                  <Square className="w-5 h-5 mr-2" />
                  Stop Recording
                </button>
              )}
              
              <button
                onClick={skipQuestion}
                disabled={isAnalyzing}
                className="flex items-center px-4 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <SkipForward className="w-5 h-5 mr-2" />
                Skip
              </button>
            </div>
            
            {isRecording && (
              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  Recording your response... Speak naturally and maintain eye contact with the camera.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column - Question and Analysis */}
        <div className="space-y-6">
          {/* Current Question */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Question {currentQuestionIndex + 1}
            </h2>
            
            {currentQuestion && (
              <div>
                <p className="text-gray-800 text-lg leading-relaxed mb-4">
                  {currentQuestion.question}
                </p>
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span className="px-2 py-1 bg-gray-100 rounded">
                    {currentQuestion.type || 'General'}
                  </span>
                  <span className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    ~{currentQuestion.expected_duration || 60}s
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Real-time Analysis */}
          {currentAnalysis && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Analysis Results
              </h3>
              
              {/* Transcript */}
              {showTranscript && currentAnalysis.transcript && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Transcript:</h4>
                  <div className="bg-gray-50 p-3 rounded text-sm">
                    {currentAnalysis.transcript.transcript || 'No speech detected'}
                  </div>
                  
                  {currentAnalysis.transcript.confidence && (
                    <div className="mt-2 text-xs text-gray-500">
                      Confidence: {Math.round(currentAnalysis.transcript.confidence * 100)}%
                    </div>
                  )}
                </div>
              )}

              {/* Answer Rating */}
              {currentAnalysis.answer_rating && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">AI Answer Rating:</h4>
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center">
                        <div className="text-2xl font-bold text-blue-600 mr-2">
                          {currentAnalysis.answer_rating.overall_rating?.score || 0}/10
                        </div>
                        <div className="text-sm text-gray-600">
                          {currentAnalysis.answer_rating.overall_rating?.level || 'Not Rated'}
                        </div>
                      </div>
                      <div className="text-xs text-gray-500">
                        AI-Powered Rating
                      </div>
                    </div>
                    
                    {currentAnalysis.answer_rating.feedback && (
                      <div className="text-sm text-gray-700 mb-2">
                        <strong>Feedback:</strong> {currentAnalysis.answer_rating.feedback}
                      </div>
                    )}
                    
                    {currentAnalysis.answer_rating.improvements && currentAnalysis.answer_rating.improvements.length > 0 && (
                      <div className="text-sm">
                        <strong className="text-gray-700">Improvements:</strong>
                        <ul className="list-disc list-inside mt-1 text-gray-600">
                          {currentAnalysis.answer_rating.improvements.slice(0, 2).map((improvement, index) => (
                            <li key={index}>{improvement}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Voice Metrics */}
              {currentAnalysis.voice_metrics && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Voice Analysis:</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Stability:</span>
                      <span className="font-medium">
                        {Math.round(currentAnalysis.voice_metrics.stability_score || 0)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Clarity:</span>
                      <span className="font-medium">
                        {Math.round(currentAnalysis.voice_metrics.clarity_score || 0)}%
                      </span>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Emotion Analysis */}
              {currentAnalysis.emotion_analysis && currentAnalysis.emotion_analysis.metrics && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Emotion Analysis:</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Confidence:</span>
                      <span className="font-medium">
                        {Math.round(currentAnalysis.emotion_analysis.metrics.confidence_score || 0)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Eye Contact:</span>
                      <span className="font-medium">
                        {Math.round(currentAnalysis.emotion_analysis.metrics.eye_contact_percentage || 0)}%
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tips */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h3 className="font-medium text-blue-900 mb-2">💡 Tips</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Look directly at the camera</li>
              <li>• Speak clearly and at a steady pace</li>
              <li>• Take your time to think before answering</li>
              <li>• Use specific examples when possible</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            <span className="text-red-700">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewSession;
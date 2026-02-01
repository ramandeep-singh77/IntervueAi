import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Camera, Mic, Brain, BarChart3, X, Play, CheckCircle, AlertCircle } from 'lucide-react';

const Header = () => {
  const location = useLocation();
  const [activeModal, setActiveModal] = useState(null);

  const isActive = (path) => {
    return location.pathname === path;
  };

  const openModal = (modalType) => {
    setActiveModal(modalType);
  };

  const closeModal = () => {
    setActiveModal(null);
  };

  const VideoAnalysisModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Camera className="w-6 h-6 text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Video Analysis</h2>
            </div>
            <button onClick={closeModal} className="p-2 hover:bg-gray-100 rounded-lg">
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Real-Time Facial Analysis</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Face Detection</span>
                  </div>
                  <p className="text-sm text-gray-600">Detects your face position and presence throughout the interview</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Eye Contact</span>
                  </div>
                  <p className="text-sm text-gray-600">Measures how often you maintain eye contact with the camera</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Confidence Level</span>
                  </div>
                  <p className="text-sm text-gray-600">Analyzes facial expressions to gauge confidence</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Position Stability</span>
                  </div>
                  <p className="text-sm text-gray-600">Tracks head movement and posture consistency</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">How It Works</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                  <p className="text-gray-700">Camera captures your video during the interview</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                  <p className="text-gray-700">OpenCV processes frames for face and eye detection</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                  <p className="text-gray-700">AI calculates confidence metrics and eye contact percentage</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">4</div>
                  <p className="text-gray-700">Results are displayed in your analytics dashboard</p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800">Privacy Note</h4>
                  <p className="text-sm text-yellow-700 mt-1">
                    All video analysis is performed locally in your browser. No video data is stored or transmitted to our servers.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <Link
                to="/setup"
                onClick={closeModal}
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Play className="w-4 h-4 mr-2" />
                Try Video Analysis
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const VoiceAnalysisModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Mic className="w-6 h-6 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Voice Analysis</h2>
            </div>
            <button onClick={closeModal} className="p-2 hover:bg-gray-100 rounded-lg">
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Speech Recognition & Analysis</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Speech-to-Text</span>
                  </div>
                  <p className="text-sm text-gray-600">Converts your speech to text using Google Speech Recognition</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Speaking Rate</span>
                  </div>
                  <p className="text-sm text-gray-600">Calculates your words per minute (WPM) for pacing analysis</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Filler Words</span>
                  </div>
                  <p className="text-sm text-gray-600">Detects "um", "uh", "like" and other filler words</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Voice Stability</span>
                  </div>
                  <p className="text-sm text-gray-600">Analyzes pitch and energy consistency</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Audio Processing Pipeline</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                  <p className="text-gray-700">Microphone captures your audio in WebM format</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                  <p className="text-gray-700">FFmpeg converts audio to WAV format for processing</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                  <p className="text-gray-700">Librosa analyzes pitch, energy, and voice activity</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">4</div>
                  <p className="text-gray-700">Google Speech API transcribes speech to text</p>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-blue-800">Real Analysis</h4>
                  <p className="text-sm text-blue-700 mt-1">
                    Our voice analysis provides real metrics - 0 WPM when silent, actual word counts when speaking, and genuine filler word detection.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <Link
                to="/setup"
                onClick={closeModal}
                className="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors"
              >
                <Play className="w-4 h-4 mr-2" />
                Try Voice Analysis
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const AIFeedbackModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BarChart3 className="w-6 h-6 text-purple-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">AI Feedback</h2>
            </div>
            <button onClick={closeModal} className="p-2 hover:bg-gray-100 rounded-lg">
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Comprehensive Analysis</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Confidence Scoring</span>
                  </div>
                  <p className="text-sm text-gray-600">Overall confidence score based on voice, video, and speech metrics</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Personalized Tips</span>
                  </div>
                  <p className="text-sm text-gray-600">AI-generated improvement suggestions tailored to your performance</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Strengths & Areas</span>
                  </div>
                  <p className="text-sm text-gray-600">Identifies what you did well and areas for improvement</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="font-medium">Action Plan</span>
                  </div>
                  <p className="text-sm text-gray-600">Step-by-step recommendations for skill improvement</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Analytics Dashboard</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">📊</div>
                  <p className="text-gray-700">Interactive charts showing performance breakdown</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">📈</div>
                  <p className="text-gray-700">Speech analytics with word count and speaking rate</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">🎯</div>
                  <p className="text-gray-700">Emotion distribution and confidence trends</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">📋</div>
                  <p className="text-gray-700">Exportable reports in JSON and CSV formats</p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-green-800">Dynamic Questions</h4>
                  <p className="text-sm text-green-700 mt-1">
                    AI generates unique interview questions every time, tailored to your selected role and experience level.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <Link
                to="/setup"
                onClick={closeModal}
                className="inline-flex items-center px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors"
              >
                <Play className="w-4 h-4 mr-2" />
                Experience AI Feedback
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">InterVue AI</h1>
              <p className="text-xs text-gray-500">AI-Powered Interview Practice</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'text-primary-600 bg-primary-50' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <Brain className="w-4 h-4" />
              <span>Home</span>
            </Link>

            <Link
              to="/setup"
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/setup') 
                  ? 'text-primary-600 bg-primary-50' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <Camera className="w-4 h-4" />
              <span>Practice</span>
            </Link>
          </nav>

          {/* Features Icons */}
          <div className="flex items-center space-x-4">
            <div className="hidden lg:flex items-center space-x-6 text-sm text-gray-500">
              <button 
                onClick={() => openModal('video')}
                className="flex items-center space-x-1 hover:text-blue-600 transition-colors cursor-pointer"
              >
                <Camera className="w-4 h-4" />
                <span>Video Analysis</span>
              </button>
              <button 
                onClick={() => openModal('voice')}
                className="flex items-center space-x-1 hover:text-green-600 transition-colors cursor-pointer"
              >
                <Mic className="w-4 h-4" />
                <span>Voice Analysis</span>
              </button>
              <button 
                onClick={() => openModal('ai')}
                className="flex items-center space-x-1 hover:text-purple-600 transition-colors cursor-pointer"
              >
                <BarChart3 className="w-4 h-4" />
                <span>AI Feedback</span>
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button className="md:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-50">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-gray-200">
          <div className="py-2 space-y-1">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/') 
                  ? 'text-primary-600 bg-primary-50' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <Brain className="w-4 h-4" />
              <span>Home</span>
            </Link>

            <Link
              to="/setup"
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/setup') 
                  ? 'text-primary-600 bg-primary-50' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <Camera className="w-4 h-4" />
              <span>Practice Interview</span>
            </Link>

            {/* Mobile Feature Buttons */}
            <div className="pt-2 border-t border-gray-100">
              <button 
                onClick={() => openModal('video')}
                className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 w-full text-left"
              >
                <Camera className="w-4 h-4" />
                <span>Video Analysis</span>
              </button>
              <button 
                onClick={() => openModal('voice')}
                className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 w-full text-left"
              >
                <Mic className="w-4 h-4" />
                <span>Voice Analysis</span>
              </button>
              <button 
                onClick={() => openModal('ai')}
                className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 w-full text-left"
              >
                <BarChart3 className="w-4 h-4" />
                <span>AI Feedback</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      {activeModal === 'video' && <VideoAnalysisModal />}
      {activeModal === 'voice' && <VoiceAnalysisModal />}
      {activeModal === 'ai' && <AIFeedbackModal />}
    </header>
  );
};

export default Header;
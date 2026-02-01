import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Camera, 
  Mic, 
  Settings, 
  Play, 
  AlertCircle, 
  CheckCircle,
  Briefcase,
  BarChart3
} from 'lucide-react';
import { MediaRecorderService } from '../services/mediaRecorder';
import { useMedia } from '../contexts/MediaContext';
import { interviewAPI, apiUtils } from '../services/api';
import { sessionStorage } from '../utils/sessionStorage';
import VideoPreview from '../components/VideoPreview';

const InterviewSetup = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Use media context instead of local state
  const { 
    stream, 
    permissions, 
    devices, 
    requestPermissions: contextRequestPermissions,
    initializeMedia 
  } = useMedia();
  
  // Form state
  const [selectedRole, setSelectedRole] = useState(location.state?.selectedRole || '');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [numQuestions, setNumQuestions] = useState(5); // Default to 5 questions
  
  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isTestingDevices, setIsTestingDevices] = useState(false);
  const [apiHealthy, setApiHealthy] = useState(null);

  const roles = [
    { 
      value: 'Software Engineer', 
      label: 'Software Engineer', 
      icon: '💻',
      description: 'Technical interviews, coding challenges, system design'
    },
    { 
      value: 'HR', 
      label: 'HR Professional', 
      icon: '👥',
      description: 'People management, communication, conflict resolution'
    },
    { 
      value: 'Data Analyst', 
      label: 'Data Analyst', 
      icon: '📊',
      description: 'Data interpretation, statistical analysis, insights'
    }
  ];

  const experienceLevels = [
    { 
      value: 'Fresher', 
      label: 'Fresher (0-2 years)', 
      description: 'Entry-level positions, foundational questions'
    },
    { 
      value: 'Experienced', 
      label: 'Experienced (2+ years)', 
      description: 'Advanced questions, leadership scenarios'
    }
  ];

  useEffect(() => {
    checkApiHealth();
    checkCompatibility();
  }, []);

  const checkApiHealth = async () => {
    try {
      const healthy = await apiUtils.checkHealth();
      setApiHealthy(healthy);
      if (!healthy) {
        setError('Backend API is not available. Please ensure the server is running.');
      }
    } catch (error) {
      setApiHealthy(false);
      setError('Failed to connect to the backend server.');
    }
  };

  const checkCompatibility = async () => {
    const compatibility = MediaRecorderService.checkCompatibility();
    if (!compatibility.isCompatible) {
      setError(`Browser compatibility issues: ${compatibility.issues.join(', ')}`);
    }
  };

  const requestPermissions = async () => {
    setIsTestingDevices(true);
    setError('');
    
    try {
      // Use context method for requesting permissions
      await contextRequestPermissions();

      // Small delay to ensure permissions are fully granted
      await new Promise(resolve => setTimeout(resolve, 500));

      // Initialize media stream for preview
      await initializeMedia();

    } catch (error) {
      console.error('Permission/device setup failed:', error);
      setError(`Camera/microphone setup failed: ${error.message}`);
    } finally {
      setIsTestingDevices(false);
    }
  };

  const startInterview = async () => {
    if (!selectedRole || !experienceLevel) {
      setError('Please select both role and experience level');
      return;
    }

    if (!apiHealthy) {
      setError('Backend server is not available. Please try again later.');
      return;
    }

    if (permissions.camera !== 'granted' || permissions.microphone !== 'granted') {
      setError('Camera and microphone permissions are required');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Start interview session with question count
      const sessionData = await interviewAPI.startInterview(selectedRole, experienceLevel, numQuestions);
      
      // Store session data in localStorage
      sessionStorage.setSessionData(sessionData.session_id, sessionData);
      
      // Small delay to ensure everything is ready
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Navigate to interview session without passing any objects in state
      navigate(`/interview/${sessionData.session_id}`, {
        replace: true
      });

    } catch (error) {
      console.error('Failed to start interview:', error);
      setError(apiUtils.formatError(error));
    } finally {
      setIsLoading(false);
    }
  };

  const getPermissionIcon = (status) => {
    switch (status) {
      case 'granted':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'denied':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Settings className="w-5 h-5 text-gray-400" />;
    }
  };

  const getPermissionText = (status) => {
    switch (status) {
      case 'granted':
        return 'Granted';
      case 'denied':
        return 'Denied';
      default:
        return 'Not requested';
    }
  };

  const canStartInterview = selectedRole && 
                           experienceLevel && 
                           permissions.camera === 'granted' && 
                           permissions.microphone === 'granted' &&
                           apiHealthy;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Setup Your Interview Practice
        </h1>
        <p className="text-lg text-gray-600">
          Configure your interview settings and test your camera and microphone
        </p>
      </div>

      {/* API Health Status */}
      {apiHealthy !== null && (
        <div className={`mb-6 p-4 rounded-lg border ${
          apiHealthy 
            ? 'bg-green-50 border-green-200 text-green-700' 
            : 'bg-red-50 border-red-200 text-red-700'
        }`}>
          <div className="flex items-center">
            {apiHealthy ? (
              <CheckCircle className="w-5 h-5 mr-2" />
            ) : (
              <AlertCircle className="w-5 h-5 mr-2" />
            )}
            <span className="font-medium">
              {apiHealthy ? 'Backend Connected' : 'Backend Unavailable'}
            </span>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Left Column - Settings */}
        <div className="space-y-6">
          {/* Role Selection */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Briefcase className="w-5 h-5 mr-2" />
              Interview Role
            </h2>
            <div className="space-y-3">
              {roles.map((role) => (
                <label
                  key={role.value}
                  className={`flex items-start p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedRole === role.value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="role"
                    value={role.value}
                    checked={selectedRole === role.value}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    className="mt-1 text-primary-600 focus:ring-primary-500"
                  />
                  <div className="ml-3 flex-1">
                    <div className="flex items-center">
                      <span className="text-lg mr-2">{role.icon}</span>
                      <span className="font-medium text-gray-900">{role.label}</span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{role.description}</p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Experience Level */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2" />
              Experience Level
            </h2>
            <div className="space-y-3">
              {experienceLevels.map((level) => (
                <label
                  key={level.value}
                  className={`flex items-start p-4 border rounded-lg cursor-pointer transition-colors ${
                    experienceLevel === level.value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="experience"
                    value={level.value}
                    checked={experienceLevel === level.value}
                    onChange={(e) => setExperienceLevel(e.target.value)}
                    className="mt-1 text-primary-600 focus:ring-primary-500"
                  />
                  <div className="ml-3 flex-1">
                    <span className="font-medium text-gray-900">{level.label}</span>
                    <p className="text-sm text-gray-600 mt-1">{level.description}</p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Question Count Selection */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Settings className="w-5 h-5 mr-2" />
              Interview Length
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Questions: {numQuestions}
                </label>
                <input
                  type="range"
                  min="3"
                  max="10"
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>3 (Quick)</span>
                  <span>5 (Standard)</span>
                  <span>10 (Comprehensive)</span>
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <p>
                  <strong>Estimated time:</strong> {Math.round(numQuestions * 1.5)} - {numQuestions * 2} minutes
                </p>
                <p className="mt-1">
                  Each question allows 60-120 seconds for your response
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column - Media Setup */}
        <div className="space-y-6">
          {/* Camera Preview */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Camera className="w-5 h-5 mr-2" />
              Camera Preview
            </h2>
            
            <div className="aspect-video bg-gray-100 rounded-lg overflow-hidden mb-4">
              <VideoPreview 
                stream={stream}
                className="w-full h-full"
                showPlaceholder={true}
              />
            </div>

            {!stream && (
              <button
                onClick={requestPermissions}
                disabled={isTestingDevices}
                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isTestingDevices ? (
                  <div className="flex items-center justify-center">
                    <div className="spinner mr-2"></div>
                    Testing Devices...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <Settings className="w-5 h-5 mr-2" />
                    Test Camera & Microphone
                  </div>
                )}
              </button>
            )}
          </div>

          {/* Permissions Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Device Permissions
            </h2>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <Camera className="w-5 h-5 text-gray-600 mr-3" />
                  <span className="font-medium">Camera</span>
                </div>
                <div className="flex items-center">
                  {getPermissionIcon(permissions.camera)}
                  <span className="ml-2 text-sm">{getPermissionText(permissions.camera)}</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <Mic className="w-5 h-5 text-gray-600 mr-3" />
                  <span className="font-medium">Microphone</span>
                </div>
                <div className="flex items-center">
                  {getPermissionIcon(permissions.microphone)}
                  <span className="ml-2 text-sm">{getPermissionText(permissions.microphone)}</span>
                </div>
              </div>
            </div>

            {/* Device Info */}
            {devices.videoInputs.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  <strong>Camera:</strong> {devices.videoInputs[0].label || 'Default Camera'}
                </p>
                <p className="text-sm text-gray-600">
                  <strong>Microphone:</strong> {devices.audioInputs[0]?.label || 'Default Microphone'}
                </p>
              </div>
            )}
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

      {/* Start Interview Button */}
      <div className="mt-8 text-center">
        <button
          onClick={startInterview}
          disabled={!canStartInterview || isLoading}
          className={`inline-flex items-center px-8 py-4 text-lg font-semibold rounded-lg transition-colors ${
            canStartInterview && !isLoading
              ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg hover:shadow-xl'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center">
              <div className="spinner mr-2"></div>
              Starting Interview...
            </div>
          ) : (
            <div className="flex items-center">
              <Play className="w-6 h-6 mr-2" />
              Start Interview Practice
            </div>
          )}
        </button>

        {!canStartInterview && !isLoading && (
          <p className="mt-3 text-sm text-gray-500">
            Please complete all setup steps above to start your interview
          </p>
        )}
      </div>
    </div>
  );
};

export default InterviewSetup;
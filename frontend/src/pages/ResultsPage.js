import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  BarChart3, 
  TrendingUp, 
  Brain,
  Camera,
  Mic,
  MessageSquare,
  ArrowRight,
  Download,
  Share2,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Target
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { feedbackAPI, apiUtils, exportAPI } from '../services/api';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const ResultsPage = () => {
  const { sessionId } = useParams();
  
  // State
  const [feedbackData, setFeedbackData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [isExporting, setIsExporting] = useState(false);

  useEffect(() => {
    const fetchFeedback = async () => {
      setIsLoading(true);
      setError('');
      
      try {
        const data = await feedbackAPI.getFeedback(sessionId);
        setFeedbackData(data);
        console.log('Feedback data:', data);
      } catch (error) {
        console.error('Failed to fetch feedback:', error);
        setError(apiUtils.formatError(error));
      } finally {
        setIsLoading(false);
      }
    };

    if (sessionId) {
      fetchFeedback();
    }
  }, [sessionId]);

  const retryFeedback = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const data = await feedbackAPI.getFeedback(sessionId);
      setFeedbackData(data);
      console.log('Feedback data:', data);
    } catch (error) {
      console.error('Failed to fetch feedback:', error);
      setError(apiUtils.formatError(error));
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async (format = 'json') => {
    setIsExporting(true);
    try {
      const exportData = await exportAPI.exportResults(sessionId, format);
      
      if (format === 'csv') {
        // Download CSV file
        const blob = new Blob([exportData.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = exportData.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        // Download JSON file
        const blob = new Blob([JSON.stringify(exportData.data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = exportData.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Export failed:', error);
      setError('Failed to export results. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleShare = async () => {
    if (navigator.share && feedbackData) {
      try {
        await navigator.share({
          title: 'InterVue AI - Interview Results',
          text: `I just completed an interview practice session and scored ${Math.round(feedbackData.confidence_score?.overall_score || 0)}/100!`,
          url: window.location.href
        });
      } catch (error) {
        // Fallback to copying URL
        navigator.clipboard.writeText(window.location.href);
        alert('Results URL copied to clipboard!');
      }
    } else {
      // Fallback to copying URL
      navigator.clipboard.writeText(window.location.href);
      alert('Results URL copied to clipboard!');
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 55) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBackground = (score) => {
    if (score >= 85) return 'bg-green-100';
    if (score >= 70) return 'bg-blue-100';
    if (score >= 55) return 'bg-yellow-100';
    if (score >= 40) return 'bg-orange-100';
    return 'bg-red-100';
  };

  const renderOverviewTab = () => {
    if (!feedbackData) return null;

    const overallScore = feedbackData.confidence_score?.overall_score || 0;
    const componentScores = feedbackData.confidence_score?.component_scores || {};

    // Prepare chart data for component scores
    const componentChartData = {
      labels: ['Voice Stability', 'Eye Contact', 'Speech Quality'],
      datasets: [
        {
          label: 'Score',
          data: [
            componentScores.voice_stability?.score || 0,
            componentScores.eye_contact?.score || 0,
            componentScores.speech_quality?.score || 0
          ],
          backgroundColor: [
            'rgba(59, 130, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(139, 92, 246, 0.8)'
          ],
          borderColor: [
            'rgba(59, 130, 246, 1)',
            'rgba(16, 185, 129, 1)',
            'rgba(139, 92, 246, 1)'
          ],
          borderWidth: 2
        }
      ]
    };

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Performance Breakdown'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: function(value) {
              return value + '%';
            }
          }
        }
      }
    };

    return (
      <div className="space-y-6">
        {/* Overall Score */}
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="mb-4">
            <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full ${getScoreBackground(overallScore)} mb-4`}>
              <span className={`text-3xl font-bold ${getScoreColor(overallScore)}`}>
                {Math.round(overallScore)}
              </span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Overall Confidence Score
            </h2>
            <p className="text-lg text-gray-600">
              {feedbackData.confidence_score?.score_interpretation?.level || 'Unknown'} Performance
            </p>
            <p className="text-sm text-gray-500 mt-2">
              {feedbackData.confidence_score?.score_interpretation?.description || ''}
            </p>
          </div>
        </div>

        {/* Component Scores Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance Breakdown</h3>
          <div className="h-64">
            <Bar data={componentChartData} options={chartOptions} />
          </div>
        </div>

        {/* Component Details */}
        <div className="grid md:grid-cols-2 gap-6">
          {Object.entries(componentScores).map(([key, data]) => {
            const titles = {
              voice_stability: 'Voice Stability',
              eye_contact: 'Eye Contact',
              speech_quality: 'Speech Quality'
            };
            
            const icons = {
              voice_stability: Mic,
              eye_contact: Camera,
              speech_quality: MessageSquare
            };
            
            const Icon = icons[key];
            const score = data?.score || 0;
            
            if (!Icon) return null; // Skip unknown components
            
            return (
              <div key={key} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center mb-4">
                  <div className={`p-2 rounded-lg ${getScoreBackground(score)} mr-3`}>
                    <Icon className={`w-5 h-5 ${getScoreColor(score)}`} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">{titles[key]}</h4>
                    <p className="text-sm text-gray-500">Weight: {Math.round((data?.weight || 0) * 100)}%</p>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${score >= 70 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`}
                        style={{ width: `${score}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className={`ml-4 text-lg font-semibold ${getScoreColor(score)}`}>
                    {Math.round(score)}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderFeedbackTab = () => {
    if (!feedbackData?.feedback) return null;

    const feedback = feedbackData.feedback;

    return (
      <div className="space-y-6">
        {/* Overall Feedback */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Brain className="w-5 h-5 mr-2" />
            AI-Generated Feedback
          </h3>
          <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed">
              {feedback.overall_feedback}
            </p>
          </div>
        </div>

        {/* Strengths */}
        {feedback.strengths && feedback.strengths.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
              Your Strengths
            </h3>
            <ul className="space-y-3">
              {feedback.strengths.map((strength, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Areas for Improvement */}
        {feedback.areas_for_improvement && feedback.areas_for_improvement.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2 text-blue-600" />
              Areas for Improvement
            </h3>
            <ul className="space-y-3">
              {feedback.areas_for_improvement.map((area, index) => (
                <li key={index} className="flex items-start">
                  <AlertCircle className="w-5 h-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{area}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Plan */}
        {feedback.action_plan && feedback.action_plan.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-purple-600" />
              Action Plan
            </h3>
            <ol className="space-y-3">
              {feedback.action_plan.map((action, index) => (
                <li key={index} className="flex items-start">
                  <span className="inline-flex items-center justify-center w-6 h-6 bg-purple-100 text-purple-600 rounded-full text-sm font-medium mr-3 mt-0.5 flex-shrink-0">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{action}</span>
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Personalized Tips */}
        {feedback.personalized_tips && feedback.personalized_tips.length > 0 && (
          <div className="bg-blue-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-4">💡 Personalized Tips</h3>
            <ul className="space-y-2">
              {feedback.personalized_tips.map((tip, index) => (
                <li key={index} className="text-blue-800 text-sm">
                  • {tip}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderAnalyticsTab = () => {
    if (!feedbackData?.analytics) return null;

    const analytics = feedbackData.analytics;

    // Prepare emotion distribution chart
    const emotionData = analytics.emotion_analytics?.emotion_distribution || {};
    const emotionChartData = {
      labels: Object.keys(emotionData),
      datasets: [
        {
          data: Object.values(emotionData),
          backgroundColor: [
            '#10B981', // green
            '#3B82F6', // blue
            '#F59E0B', // yellow
            '#EF4444', // red
            '#8B5CF6', // purple
            '#F97316', // orange
          ],
          borderWidth: 2,
          borderColor: '#fff'
        }
      ]
    };

    const emotionChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        title: {
          display: true,
          text: 'Emotion Distribution'
        }
      }
    };

    return (
      <div className="space-y-6">
        {/* Analytics Summary */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {analytics.voice_analytics?.average_stability?.toFixed(1) || 0}%
            </div>
            <div className="text-sm text-gray-600">Average Voice Stability</div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {analytics.emotion_analytics?.average_confidence_level?.toFixed(1) || 0}%
            </div>
            <div className="text-sm text-gray-600">Average Confidence</div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {analytics.speech_analytics?.average_speaking_rate?.toFixed(0) || 0}
            </div>
            <div className="text-sm text-gray-600">Words Per Minute</div>
          </div>
        </div>

        {/* Emotion Distribution */}
        {Object.keys(emotionData).length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Emotion Analysis</h3>
            <div className="h-64">
              <Doughnut data={emotionChartData} options={emotionChartOptions} />
            </div>
          </div>
        )}

        {/* Speech Analytics */}
        {analytics.speech_analytics && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Speech Analytics</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {analytics.speech_analytics.total_words || 0}
                </div>
                <div className="text-sm text-gray-600">Total Words Spoken</div>
              </div>
              
              <div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {analytics.speech_analytics.filler_word_percentage?.toFixed(1) || 0}%
                </div>
                <div className="text-sm text-gray-600">Filler Word Percentage</div>
              </div>
              
              <div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {analytics.speech_analytics.total_filler_words || 0}
                </div>
                <div className="text-sm text-gray-600">Total Filler Words</div>
              </div>
              
              <div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {analytics.response_count || 0}
                </div>
                <div className="text-sm text-gray-600">Questions Answered</div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Generating your feedback...</p>
          <p className="text-sm text-gray-500 mt-2">This may take a moment</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto text-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-8">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-red-900 mb-2">
            Failed to Load Results
          </h2>
          <p className="text-red-700 mb-6">{error}</p>
          <div className="space-x-4">
            <button
              onClick={retryFeedback}
              className="btn-primary"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </button>
            <Link to="/setup" className="btn-secondary">
              Start New Interview
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Interview Results
            </h1>
            <p className="text-gray-600">
              Your AI-powered interview analysis and feedback
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="relative">
              <button 
                onClick={() => handleExport('json')}
                disabled={isExporting}
                className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                <Download className="w-4 h-4 mr-2" />
                {isExporting ? 'Exporting...' : 'Export JSON'}
              </button>
            </div>
            <div className="relative">
              <button 
                onClick={() => handleExport('csv')}
                disabled={isExporting}
                className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                <Download className="w-4 h-4 mr-2" />
                {isExporting ? 'Exporting...' : 'Export CSV'}
              </button>
            </div>
            <button 
              onClick={handleShare}
              className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'feedback', label: 'AI Feedback', icon: Brain },
              { id: 'analytics', label: 'Analytics', icon: TrendingUp }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="mb-8">
        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'feedback' && renderFeedbackTab()}
        {activeTab === 'analytics' && renderAnalyticsTab()}
      </div>

      {/* Actions */}
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Ready for Another Practice Session?
        </h3>
        <div className="space-x-4">
          <Link
            to="/setup"
            className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
          >
            Practice Again
            <ArrowRight className="w-4 h-4 ml-2" />
          </Link>
          <Link
            to="/"
            className="inline-flex items-center px-6 py-3 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Camera, 
  Mic, 
  Brain, 
  BarChart3, 
  Target,
  ArrowRight,
  CheckCircle,
  Play
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: Camera,
      title: 'Video Analysis',
      description: 'AI-powered facial expression and emotion detection using advanced computer vision',
      color: 'text-blue-600 bg-blue-100'
    },
    {
      icon: Mic,
      title: 'Voice Analysis',
      description: 'Speech-to-text conversion with voice tone, pitch, and filler word detection',
      color: 'text-green-600 bg-green-100'
    },
    {
      icon: Brain,
      title: 'AI Feedback',
      description: 'Personalized improvement suggestions powered by Google Gemini AI',
      color: 'text-purple-600 bg-purple-100'
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Comprehensive performance metrics and confidence scoring',
      color: 'text-orange-600 bg-orange-100'
    }
  ];

  const roles = [
    { name: 'Software Engineer', icon: '💻', description: 'Technical and coding interviews' },
    { name: 'HR Professional', icon: '👥', description: 'People management and communication' },
    { name: 'Data Analyst', icon: '📊', description: 'Data-driven problem solving' }
  ];

  const benefits = [
    'Real-time emotion and confidence analysis',
    'Speech pattern and filler word detection',
    'Personalized AI-generated feedback',
    'Role-specific interview questions',
    'Comprehensive performance analytics',
    'Practice anytime, anywhere'
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-purple-50 py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex justify-center mb-6">
              <div className="flex items-center justify-center w-20 h-20 bg-primary-600 rounded-2xl shadow-lg">
                <Brain className="w-10 h-10 text-white" />
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Master Your
              <span className="text-primary-600 block">Interview Skills</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              AI-powered interview practice platform that analyzes your confidence, emotions, 
              voice tone, and communication skills in real-time.
            </p>
            
            <div className="flex justify-center">
              <Link
                to="/setup"
                className="inline-flex items-center px-8 py-4 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl"
              >
                <Play className="w-5 h-5 mr-2" />
                Start Practice Interview
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI Technology
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our platform combines cutting-edge AI models to provide comprehensive 
              interview analysis and personalized feedback.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center group">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl ${feature.color} mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Interview Roles Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Practice for Your Dream Role
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Choose from specialized interview scenarios tailored to different roles and experience levels.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {roles.map((role, index) => (
              <div key={index} className="bg-white rounded-xl p-8 shadow-md hover:shadow-lg transition-shadow border border-gray-100">
                <div className="text-4xl mb-4 text-center">{role.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">
                  {role.name}
                </h3>
                <p className="text-gray-600 text-center mb-6">
                  {role.description}
                </p>
                <div className="flex justify-center">
                  <Link
                    to="/setup"
                    state={{ selectedRole: role.name }}
                    className="inline-flex items-center text-primary-600 font-medium hover:text-primary-700"
                  >
                    Practice Now
                    <ArrowRight className="w-4 h-4 ml-1" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                  Why Choose InterVue AI?
                </h2>
                <p className="text-lg text-gray-600 mb-8">
                  Get instant, actionable feedback on your interview performance with 
                  our comprehensive AI analysis system.
                </p>
                
                <div className="space-y-4">
                  {benefits.map((benefit, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-8">
                  <Link
                    to="/setup"
                    className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    Get Started Now
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </Link>
                </div>
              </div>

              <div className="lg:pl-8">
                <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-2xl p-8">
                  <div className="grid grid-cols-2 gap-6">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-primary-600 mb-2">95%</div>
                      <div className="text-sm text-gray-600">Accuracy Rate</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600 mb-2">4.8/5</div>
                      <div className="text-sm text-gray-600">User Rating</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-600 mb-2">10k+</div>
                      <div className="text-sm text-gray-600">Interviews</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
                      <div className="text-sm text-gray-600">Available</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Simple 4-step process to improve your interview skills with AI-powered analysis.
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-4 gap-8">
              {[
                { step: '1', title: 'Choose Role', description: 'Select your target role and experience level', icon: Target },
                { step: '2', title: 'Start Interview', description: 'Answer questions with camera and mic enabled', icon: Camera },
                { step: '3', title: 'AI Analysis', description: 'Our AI analyzes your performance in real-time', icon: Brain },
                { step: '4', title: 'Get Feedback', description: 'Receive detailed insights and improvement tips', icon: BarChart3 }
              ].map((item, index) => (
                <div key={index} className="text-center">
                  <div className="relative mb-6">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-xl font-bold mb-4">
                      {item.step}
                    </div>
                    <div className="inline-flex items-center justify-center w-12 h-12 bg-white rounded-full shadow-md -mt-6 ml-8">
                      <item.icon className="w-6 h-6 text-primary-600" />
                    </div>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {item.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Ace Your Next Interview?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of professionals who have improved their interview skills with InterVue AI.
          </p>
          <Link
            to="/setup"
            className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-50 transition-colors shadow-lg"
          >
            <Play className="w-5 h-5 mr-2" />
            Start Your First Interview
            <ArrowRight className="w-5 h-5 ml-2" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
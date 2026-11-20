import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Shield, 
  Flame, 
  Users, 
  Bell, 
  FileText,
  ArrowRight,
  CheckCircle,
  Sparkles,
  Zap,
  Eye
} from 'lucide-react';

export default function LandingPage() {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: Flame,
      title: 'Fire & Smoke Detection',
      description: 'Real-time detection of fire hazards and smoke with instant alerts',
      gradient: 'from-orange-500 to-rose-500'
    },
    {
      icon: Users,
      title: 'Face Recognition',
      description: 'Identify authorized and unauthorized personnel automatically',
      gradient: 'from-violet-500 to-purple-500'
    },
    {
      icon: Bell,
      title: 'Instant Alerts',
      description: 'Get immediate notifications via WhatsApp and dashboard',
      gradient: 'from-cyan-500 to-blue-500'
    },
    {
      icon: FileText,
      title: 'FIR Reports',
      description: 'Auto-generated incident reports with evidence documentation',
      gradient: 'from-emerald-500 to-teal-500'
    },
    {
      icon: Eye,
      title: '24/7 Monitoring',
      description: 'Continuous AI-powered surveillance without breaks',
      gradient: 'from-pink-500 to-rose-500'
    },
    {
      icon: Zap,
      title: 'Instant Response',
      description: 'Lightning-fast threat detection and alert system',
      gradient: 'from-amber-500 to-orange-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-950 overflow-hidden relative">
      {/* Animated background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>

      {/* Header */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-700 ${isVisible ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0'}`}>
        <div className="absolute inset-0 bg-gray-950/80 backdrop-blur-xl"></div>
        <nav className="relative max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 group cursor-pointer">
              <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 shadow-lg shadow-primary-500/30">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-display font-bold gradient-text">
                SmartSentinel
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="px-6 py-2.5 rounded-xl text-white hover:bg-white/10 transition-all duration-300 font-medium"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="group relative px-6 py-2.5 rounded-xl overflow-hidden"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-500 transition-all duration-300 group-hover:scale-110"></span>
                <span className="relative flex items-center space-x-2 text-white font-medium">
                  <span>Get Started</span>
                  <Sparkles className="w-4 h-4 group-hover:animate-wiggle" />
                </span>
              </Link>
            </div>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-8">
            {/* Badge */}
            <div 
              className={`inline-flex items-center space-x-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-primary-900/50 to-accent-900/50 border border-primary-500/30 backdrop-blur-sm transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
            >
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shadow-lg shadow-emerald-400/50"></div>
              <span className="text-sm text-primary-200 font-medium">
                AI-Powered Security System
              </span>
              <Sparkles className="w-4 h-4 text-accent-400 animate-pulse" />
            </div>

            {/* Main heading */}
            <h1 
              className={`text-5xl md:text-7xl font-display font-bold text-white leading-tight transition-all duration-1000 delay-200 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
            >
              Intelligent Security
              <br />
              <span className="relative">
                <span className="gradient-text text-glow">
                  Powered by AI
                </span>
              </span>
            </h1>

            {/* Description */}
            <p 
              className={`text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed transition-all duration-1000 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
            >
              Advanced AI detection system that monitors for fire, unauthorized access, 
              and accidents in real-time. Protecting what matters most with 
              cutting-edge computer vision technology.
            </p>

            {/* CTA Buttons */}
            <div 
              className={`flex items-center justify-center flex-wrap gap-4 pt-8 transition-all duration-1000 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
            >
              <Link
                to="/register"
                className="group relative flex items-center space-x-2 px-8 py-4 rounded-2xl overflow-hidden transform hover:scale-105 transition-all duration-300"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-primary-500 via-purple-500 to-accent-500 animate-gradient-x"></span>
                <span className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-r from-primary-600 via-purple-600 to-accent-600"></span>
                <span className="relative flex items-center space-x-2 text-white font-semibold text-lg">
                  <span>Start Monitoring</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </span>
              </Link>
              <Link
                to="/login"
                className="group px-8 py-4 rounded-2xl bg-white/5 backdrop-blur-sm text-white font-semibold text-lg hover:bg-white/10 transition-all duration-300 border border-white/10 hover:border-primary-500/50 hover:shadow-lg hover:shadow-primary-500/10"
              >
                <span className="flex items-center space-x-2">
                  <Eye className="w-5 h-5 group-hover:animate-pulse" />
                  <span>View Demo</span>
                </span>
              </Link>
            </div>
          </div>
        </div>

        {/* Floating decorative elements */}
        <div className="absolute top-1/2 left-10 w-20 h-20 rounded-full bg-primary-500/20 blur-xl animate-float"></div>
        <div className="absolute top-1/3 right-10 w-32 h-32 rounded-full bg-accent-500/20 blur-xl animate-float" style={{ animationDelay: '2s' }}></div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className={`text-4xl md:text-5xl font-display font-bold text-white mb-4 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              Complete Security <span className="gradient-text">Solution</span>
            </h2>
            <p className="text-lg text-gray-400">
              Everything you need to keep your premises safe and secure
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className={`group relative p-8 rounded-2xl bg-gray-900/50 backdrop-blur-sm border border-gray-800 hover:border-primary-500/50 transition-all duration-500 hover:-translate-y-2 opacity-0 animate-fade-in-up`}
                  style={{ animationDelay: `${index * 100 + 600}ms`, animationFillMode: 'forwards' }}
                >
                  {/* Glow effect on hover */}
                  <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-primary-500/10 to-accent-500/10"></div>
                  
                  <div className={`relative w-14 h-14 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="relative text-xl font-display font-bold text-white mb-3 group-hover:text-primary-300 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="relative text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors">
                    {feature.description}
                  </p>
                  
                  {/* Arrow indicator */}
                  <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transform translate-x-2 group-hover:translate-x-0 transition-all duration-300">
                    <ArrowRight className="w-5 h-5 text-primary-400" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-6 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary-950/20 to-transparent"></div>
        <div className="max-w-7xl mx-auto relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <h2 className="text-4xl md:text-5xl font-display font-bold text-white">
                Why Choose <span className="gradient-text">SmartSentinel?</span>
              </h2>
              <div className="space-y-4">
                {[
                  'Real-time AI detection with 99% accuracy',
                  'Automatic evidence capture and storage',
                  'Instant WhatsApp alerts for critical events',
                  'Auto-generated FIR reports with documentation',
                  'Live dashboard with comprehensive analytics',
                  'Easy integration with existing camera systems'
                ].map((benefit, index) => (
                  <div 
                    key={index} 
                    className="group flex items-start space-x-4 p-4 rounded-xl bg-gray-900/30 border border-gray-800 hover:border-primary-500/30 hover:bg-gray-900/50 transition-all duration-300 cursor-default"
                  >
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-emerald-500/20">
                      <CheckCircle className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-gray-300 text-lg group-hover:text-white transition-colors">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Stats Card */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary-600/30 to-accent-600/30 blur-3xl animate-pulse"></div>
              <div className="relative p-8 rounded-3xl bg-gray-900/80 backdrop-blur-xl border border-gray-800 shadow-2xl">
                <div className="space-y-6">
                  {/* Status indicator */}
                  <div className="flex items-center justify-between p-4 rounded-xl bg-emerald-900/30 border border-emerald-500/30">
                    <span className="text-emerald-400 font-semibold">System Status</span>
                    <div className="flex items-center space-x-2">
                      <div className="relative">
                        <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                        <div className="absolute inset-0 w-3 h-3 rounded-full bg-emerald-500 animate-ping"></div>
                      </div>
                      <span className="text-emerald-400 text-sm font-medium">Active</span>
                    </div>
                  </div>
                  
                  {/* Stats grid */}
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { value: '24/7', label: 'Monitoring', gradient: 'from-violet-500 to-purple-500' },
                      { value: '99%', label: 'Accuracy', gradient: 'from-cyan-500 to-blue-500' },
                      { value: '<1s', label: 'Detection', gradient: 'from-amber-500 to-orange-500' },
                      { value: '100%', label: 'Automated', gradient: 'from-pink-500 to-rose-500' }
                    ].map((stat, index) => (
                      <div 
                        key={index}
                        className="group p-4 rounded-xl bg-gray-800/50 border border-gray-700 hover:border-primary-500/30 transition-all duration-300 cursor-default"
                      >
                        <p className={`text-3xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent group-hover:scale-105 transition-transform inline-block`}>
                          {stat.value}
                        </p>
                        <p className="text-sm text-gray-400 mt-1">{stat.label}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="relative p-12 rounded-3xl overflow-hidden">
            {/* Animated gradient background */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary-900/50 via-purple-900/50 to-accent-900/50 animate-gradient-xy"></div>
            <div className="absolute inset-0 backdrop-blur-sm border border-primary-500/20 rounded-3xl"></div>
            
            <div className="relative space-y-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-4 animate-bounce-in shadow-lg shadow-primary-500/30">
                <Shield className="w-8 h-8 text-white" />
              </div>
              
              <h2 className="text-4xl md:text-5xl font-display font-bold text-white">
                Ready to Upgrade Your Security?
              </h2>
              <p className="text-xl text-gray-300">
                Join organizations using AI-powered surveillance to protect their assets
              </p>
              <Link
                to="/register"
                className="group inline-flex items-center space-x-2 px-8 py-4 rounded-2xl bg-white text-gray-900 font-semibold text-lg hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-white/20"
              >
                <span>Get Started Free</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-gray-800">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-2">
            <Shield className="w-5 h-5 text-primary-500" />
            <span className="text-gray-400">&copy; 2026 SmartSentinel. All rights reserved.</span>
          </div>
          <div className="flex items-center space-x-6">
            <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Terms</a>
            <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

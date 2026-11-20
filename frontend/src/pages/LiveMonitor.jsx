import React from 'react';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { Video, AlertCircle, Radio, Wifi } from 'lucide-react';

export default function LiveMonitor() {
  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Video className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">Live Monitor</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Real-time AI-powered surveillance feed</p>
        </div>

        {/* Video Card */}
        <div 
          className="card-glow p-6 opacity-0 animate-fade-in-up"
          style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
                <Wifi className="w-5 h-5 text-white" />
              </div>
              <span className="font-display font-bold text-lg">Camera Feed</span>
            </div>
            <div className="flex items-center space-x-3 px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
              <div className="relative">
                <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                <div className="absolute inset-0 w-3 h-3 rounded-full bg-emerald-500 animate-ping"></div>
              </div>
              <span className="text-sm font-semibold text-emerald-400">Live</span>
              <Radio className="w-4 h-4 text-emerald-400 animate-pulse" />
            </div>
          </div>

          <div className="relative bg-gray-900 rounded-2xl overflow-hidden group" style={{ paddingBottom: '56.25%' }}>
            {/* Decorative corner accents */}
            <div className="absolute top-0 left-0 w-16 h-16 border-t-2 border-l-2 border-primary-500/50 rounded-tl-2xl z-10"></div>
            <div className="absolute top-0 right-0 w-16 h-16 border-t-2 border-r-2 border-primary-500/50 rounded-tr-2xl z-10"></div>
            <div className="absolute bottom-0 left-0 w-16 h-16 border-b-2 border-l-2 border-primary-500/50 rounded-bl-2xl z-10"></div>
            <div className="absolute bottom-0 right-0 w-16 h-16 border-b-2 border-r-2 border-primary-500/50 rounded-br-2xl z-10"></div>
            
            <img
              src={`${API_BASE_URL}${API_ENDPOINTS.VIDEO_FEED}`}
              alt="Live video feed"
              className="absolute inset-0 w-full h-full object-contain"
            />
            
            {/* Scanning line animation */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
              <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-primary-500 to-transparent animate-scan"></div>
            </div>
          </div>

          {/* Detection Legend */}
          <div 
            className="mt-6 p-5 rounded-xl bg-gradient-to-r from-primary-500/10 via-transparent to-accent-500/10 border border-primary-500/20 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '300ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-start space-x-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-cyan-500/20">
                <AlertCircle className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-gray-900 dark:text-white mb-3">Detection Legend</p>
                <div className="grid sm:grid-cols-3 gap-3">
                  <div className="flex items-center space-x-2 p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                    <div className="w-4 h-4 rounded bg-emerald-500"></div>
                    <span className="text-sm text-emerald-600 dark:text-emerald-400 font-medium">Authorized Person</span>
                  </div>
                  <div className="flex items-center space-x-2 p-2 rounded-lg bg-rose-500/10 border border-rose-500/20">
                    <div className="w-4 h-4 rounded bg-rose-500"></div>
                    <span className="text-sm text-rose-600 dark:text-rose-400 font-medium">Unauthorized Person</span>
                  </div>
                  <div className="flex items-center space-x-2 p-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
                    <div className="w-4 h-4 rounded bg-amber-500"></div>
                    <span className="text-sm text-amber-600 dark:text-amber-400 font-medium">Fire/Smoke/Accident</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes scan {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100vh); }
        }
        .animate-scan {
          animation: scan 3s linear infinite;
        }
      `}</style>
    </div>
  );
}

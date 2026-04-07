import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { Flame, Users, Image, Calendar, Search } from 'lucide-react';

export default function Evidence() {
  const [activeTab, setActiveTab] = useState('unauthorized');
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvidence();
  }, [activeTab]);

  const fetchEvidence = async () => {
    setLoading(true);
    try {
      let endpoint;
      if (activeTab === 'unauthorized') endpoint = API_ENDPOINTS.EVIDENCE_UNAUTHORIZED;
      else endpoint = API_ENDPOINTS.EVIDENCE_FIRE;

      const response = await axios.get(`${API_BASE_URL}${endpoint}`);
      setEvidence(response.data.files || []);
    } catch (error) {
      console.error('Error fetching evidence:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'unauthorized', label: 'Unauthorized', icon: Users, gradient: 'from-violet-500 to-purple-600' },
    { id: 'fire', label: 'Fire & Accidents', icon: Flame, gradient: 'from-orange-500 to-rose-600' }
  ];

  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center shadow-lg shadow-amber-500/20">
              <Image className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">Evidence Gallery</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Captured incident evidence</p>
        </div>

        {/* Tabs */}
        <div 
          className="flex flex-wrap gap-3 opacity-0 animate-fade-in-up"
          style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
        >
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`group relative flex items-center space-x-2 px-6 py-3.5 rounded-xl font-semibold whitespace-nowrap transition-all duration-300 overflow-hidden ${
                  isActive
                    ? 'text-white shadow-lg'
                    : 'bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                {isActive && (
                  <span className={`absolute inset-0 bg-gradient-to-r ${tab.gradient}`}></span>
                )}
                <Icon className={`relative w-5 h-5 transition-transform duration-300 ${isActive ? '' : 'group-hover:scale-110'}`} />
                <span className="relative">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex justify-center py-16">
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-4 border-primary-500/30 border-t-primary-500 animate-spin"></div>
              <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-accent-500/20 border-b-accent-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
            </div>
          </div>
        ) : evidence.length === 0 ? (
          <div 
            className="card-glow p-16 text-center opacity-0 animate-fade-in-up"
            style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}
          >
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center mx-auto mb-4">
              <Search className="w-10 h-10 text-gray-400" />
            </div>
            <p className="text-gray-500 dark:text-gray-400 text-lg">No evidence found</p>
            <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">Evidence will appear here when incidents are detected</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {evidence.map((item, index) => (
              <div 
                key={index} 
                className="group card-glow overflow-hidden opacity-0 animate-fade-in-up"
                style={{ animationDelay: `${index * 50 + 200}ms`, animationFillMode: 'forwards' }}
              >
                <div className="relative overflow-hidden">
                  <img
                    src={`${API_BASE_URL}${item.path}`}
                    alt={item.filename}
                    className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  
                  {/* Badge overlay */}
                  <div className="absolute top-3 right-3">
                    <span className={`px-3 py-1 rounded-lg text-xs font-semibold text-white ${activeTab === 'unauthorized' ? 'bg-violet-500' : 'bg-orange-500'}`}>
                      {activeTab === 'unauthorized' ? 'Unauthorized' : 'Fire/Accident'}
                    </span>
                  </div>
                </div>
                
                <div className="p-4">
                  <p className="text-sm font-semibold truncate mb-2 group-hover:text-primary-500 transition-colors">{item.filename}</p>
                  <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(item.timestamp).toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

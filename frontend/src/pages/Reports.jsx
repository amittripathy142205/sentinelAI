import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { FileText, Download, Calendar, HardDrive, FileWarning } from 'lucide-react';

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.REPORTS}`);
      setReports(response.data);
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-rose-500 to-pink-500 flex items-center justify-center shadow-lg shadow-rose-500/20">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">FIR Reports</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Auto-generated incident reports</p>
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex justify-center py-16">
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-4 border-primary-500/30 border-t-primary-500 animate-spin"></div>
              <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-accent-500/20 border-b-accent-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
            </div>
          </div>
        ) : reports.length === 0 ? (
          <div 
            className="card-glow p-16 text-center opacity-0 animate-fade-in-up"
            style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
          >
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center mx-auto mb-4">
              <FileWarning className="w-10 h-10 text-gray-400" />
            </div>
            <p className="text-gray-500 dark:text-gray-400 text-lg">No reports available</p>
            <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">Reports will be generated automatically when incidents occur</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {reports.map((report, index) => (
              <div 
                key={index} 
                className="group card-glow p-6 opacity-0 animate-fade-in-up hover:-translate-y-1 transition-all duration-300"
                style={{ animationDelay: `${index * 50 + 100}ms`, animationFillMode: 'forwards' }}
              >
                <div className="flex items-start justify-between mb-6">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center shadow-lg shadow-rose-500/20 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
                    <FileText className="w-7 h-7 text-white" />
                  </div>
                  <a
                    href={`${API_BASE_URL}${report.path}`}
                    download
                    className="p-3 rounded-xl bg-gradient-to-br from-primary-500/10 to-accent-500/10 text-primary-600 dark:text-primary-400 hover:from-primary-500 hover:to-accent-500 hover:text-white transition-all duration-300 group/btn"
                    title="Download Report"
                  >
                    <Download className="w-5 h-5 group-hover/btn:animate-bounce" />
                  </a>
                </div>
                
                <h3 className="font-semibold mb-4 truncate group-hover:text-primary-500 transition-colors" title={report.filename}>
                  {report.filename}
                </h3>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                    <HardDrive className="w-4 h-4" />
                    <span>Size: {(report.size / 1024).toFixed(2)} KB</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-500">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(report.timestamp).toLocaleString()}</span>
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

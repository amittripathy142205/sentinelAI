import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { AlertTriangle, CheckCircle, Clock, TrendingUp, Shield, Activity } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, alertsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}${API_ENDPOINTS.STATS}`),
        axios.get(`${API_BASE_URL}${API_ENDPOINTS.ALERTS}?limit=10`)
      ]);
      setStats(statsRes.data);
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="lg:ml-64 p-8 flex items-center justify-center min-h-screen">
        <div className="relative">
          <div className="w-16 h-16 rounded-full border-4 border-primary-500/30 border-t-primary-500 animate-spin"></div>
          <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-accent-500/20 border-b-accent-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        </div>
      </div>
    );
  }

  const statCards = [
    { label: 'Total Incidents', value: stats?.total_incidents || 0, icon: AlertTriangle, gradient: 'from-violet-500 to-purple-600', bgGradient: 'from-violet-500/10 to-purple-600/10' },
    { label: 'Total Alerts', value: stats?.total_alerts || 0, icon: CheckCircle, gradient: 'from-emerald-500 to-teal-600', bgGradient: 'from-emerald-500/10 to-teal-600/10' },
    { label: 'Unread Alerts', value: stats?.unread_alerts || 0, icon: Clock, gradient: 'from-amber-500 to-orange-600', bgGradient: 'from-amber-500/10 to-orange-600/10' }
  ];

  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-lg shadow-primary-500/20">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">Dashboard</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Monitor your security system in real-time</p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {statCards.map((card, index) => {
            const Icon = card.icon;
            return (
              <div 
                key={index} 
                className="card-glow p-6 hover:-translate-y-1 transition-all duration-300 opacity-0 animate-fade-in-up group"
                style={{ animationDelay: `${index * 100 + 100}ms`, animationFillMode: 'forwards' }}
              >
                <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${card.bgGradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300`}></div>
                <div className="relative flex items-center justify-between mb-4">
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center shadow-lg transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <span className={`text-4xl font-bold bg-gradient-to-r ${card.gradient} bg-clip-text text-transparent`}>
                    {card.value}
                  </span>
                </div>
                <p className="relative text-sm font-semibold text-gray-600 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-gray-200 transition-colors">{card.label}</p>
              </div>
            );
          })}
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Incidents by Type */}
          <div 
            className="card-glow p-6 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '400ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center shadow-lg shadow-rose-500/20">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-display font-bold">Incidents by Type</h2>
            </div>
            <div className="space-y-3">
              {stats?.incidents_by_type && Object.entries(stats.incidents_by_type).filter(([type]) => type.toLowerCase() !== 'tailgating').length > 0 ? (
                Object.entries(stats.incidents_by_type)
                  .filter(([type]) => type.toLowerCase() !== 'tailgating')
                  .map(([type, count], index) => (
                  <div 
                    key={type} 
                    className="group flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-accent-500/10 transition-all duration-300 cursor-default"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 rounded-full bg-gradient-to-r from-primary-500 to-accent-500"></div>
                      <span className="font-medium capitalize group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">{type}</span>
                    </div>
                    <span className="px-3 py-1 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold text-sm">
                      {count}
                    </span>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <Shield className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
                  <p className="text-gray-500 dark:text-gray-400">No incidents recorded yet</p>
                </div>
              )}
            </div>
          </div>

          {/* Recent Alerts */}
          <div 
            className="card-glow p-6 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '500ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                <AlertTriangle className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-display font-bold">Recent Alerts</h2>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
              {alerts && alerts.length > 0 ? (
                alerts.map((alert, index) => (
                  <div 
                    key={alert.id} 
                    className="group p-4 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all duration-300"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-semibold mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">{alert.alert_type}</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{alert.message}</p>
                      </div>
                      <span className={`badge ml-2 ${
                        alert.priority === 'high' ? 'badge-danger' : 
                        alert.priority === 'medium' ? 'badge-warning' : 'badge-info'
                      }`}>
                        {alert.priority}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-2 flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(alert.timestamp).toLocaleString()}</span>
                    </p>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
                  <p className="text-gray-500 dark:text-gray-400">No alerts to display</p>
                  <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">All systems running smoothly</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

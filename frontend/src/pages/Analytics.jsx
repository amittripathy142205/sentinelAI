import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, Activity, AlertTriangle, Shield, Clock, Zap } from 'lucide-react';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.STATS}`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return (
      <div className="lg:ml-64 p-8 flex items-center justify-center min-h-screen">
        <div className="relative">
          <div className="w-16 h-16 rounded-full border-4 border-primary-500/30 border-t-primary-500 animate-spin"></div>
          <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-accent-500/20 border-b-accent-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        </div>
      </div>
    );
  }

  const chartData = Object.entries(stats.incidents_by_type || {}).map(([type, count]) => ({
    name: type.charAt(0).toUpperCase() + type.slice(1),
    incidents: count
  }));

  const gradientColors = ['#d946ef', '#a855f7', '#8b5cf6', '#6366f1', '#3b82f6', '#06b6d4'];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-3 shadow-xl">
          <p className="text-white font-semibold">{label}</p>
          <p className="text-primary-400">{payload[0].value} incidents</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">Analytics</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Security system insights and trends</p>
        </div>

        {/* Chart Card */}
        <div 
          className="card-glow p-6 opacity-0 animate-fade-in-up"
          style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-xl font-display font-bold">Incidents by Type</h2>
          </div>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#d946ef" />
                  <stop offset="100%" stopColor="#06b6d4" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.5} />
              <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="incidents" 
                radius={[8, 8, 0, 0]}
                fill="url(#barGradient)"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={gradientColors[index % gradientColors.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* System Statistics */}
          <div 
            className="card-glow p-6 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-display font-bold">System Statistics</h2>
            </div>
            <div className="space-y-4">
              {[
                { label: 'Total Incidents', value: stats.total_incidents, gradient: 'from-violet-500 to-purple-600', icon: AlertTriangle },
                { label: 'Active Incidents', value: stats.active_incidents, gradient: 'from-rose-500 to-pink-600', icon: Activity },
                { label: 'Total Alerts', value: stats.total_alerts, gradient: 'from-emerald-500 to-teal-600', icon: Shield }
              ].map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div 
                    key={stat.label}
                    className="group flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-accent-500/10 transition-all duration-300"
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className="w-5 h-5 text-gray-500 group-hover:text-primary-500 transition-colors" />
                      <span className="font-medium group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">{stat.label}</span>
                    </div>
                    <span className={`text-2xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent`}>
                      {stat.value}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recent Activity */}
          <div 
            className="card-glow p-6 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '300ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg shadow-amber-500/20">
                <Clock className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-display font-bold">Recent Activity</h2>
            </div>
            <div className="space-y-3 max-h-80 overflow-y-auto pr-2">
              {stats.recent_activity && stats.recent_activity.length > 0 ? (
                stats.recent_activity.map((activity, index) => (
                  <div 
                    key={activity.id} 
                    className="group p-4 rounded-xl border border-gray-200 dark:border-gray-800 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all duration-300"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className={`badge ${activity.severity === 'high' ? 'badge-danger' : 'badge-warning'}`}>
                        {activity.type}
                      </span>
                      <span className="text-xs text-gray-500 flex items-center space-x-1">
                        <Clock className="w-3 h-3" />
                        <span>{new Date(activity.timestamp).toLocaleTimeString()}</span>
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-gray-200 transition-colors">{activity.description}</p>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <Shield className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
                  <p className="text-gray-500 dark:text-gray-400">No recent activity</p>
                  <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">System is running smoothly</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

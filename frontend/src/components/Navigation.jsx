import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Home, 
  Video, 
  Image, 
  FileText, 
  MapPin, 
  BarChart3, 
  LogOut, 
  Menu, 
  X,
  Moon,
  Sun,
  Shield,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navigation({ darkMode, toggleDarkMode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Live Monitor', href: '/live', icon: Video },
    { name: 'Evidence', href: '/evidence', icon: Image },
    { name: 'Reports', href: '/reports', icon: FileText },
    { name: 'Location Map', href: '/map', icon: MapPin },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <>
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden transition-opacity duration-300"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transform transition-all duration-500 ease-out lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Gradient overlay for dark mode */}
        <div className="absolute inset-0 bg-gradient-to-b from-primary-500/5 via-transparent to-accent-500/5 pointer-events-none"></div>
        
        <div className="relative flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-800">
            <Link to="/dashboard" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 shadow-lg shadow-primary-500/30">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-display font-bold gradient-text">
                SmartSentinel
              </span>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            {navigation.map((item, index) => {
              const Icon = item.icon;
              const active = isActive(item.href);
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setSidebarOpen(false)}
                  className={`group relative flex items-center space-x-3 px-4 py-3.5 rounded-xl transition-all duration-300 overflow-hidden ${
                    active
                      ? 'text-white'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/50'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {/* Active background */}
                  {active && (
                    <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-500 animate-gradient-x"></div>
                  )}
                  
                  {/* Hover glow effect */}
                  <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 ${!active && 'bg-gradient-to-r from-primary-500/10 to-accent-500/10'}`}></div>
                  
                  <Icon className={`relative w-5 h-5 transition-transform duration-300 group-hover:scale-110 ${active ? '' : 'group-hover:text-primary-500 dark:group-hover:text-primary-400'}`} />
                  <span className="relative font-medium">{item.name}</span>
                  
                  {/* Active indicator dot */}
                  {active && (
                    <div className="absolute right-4 w-2 h-2 rounded-full bg-white animate-pulse"></div>
                  )}
                </Link>
              );
            })}
          </nav>

          {/* User section */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-800">
            <div className="flex items-center justify-between mb-4 p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-lg shadow-primary-500/20">
                    <span className="text-white font-semibold">
                      {user?.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  {/* Online indicator */}
                  <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-white dark:border-gray-800"></div>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                    {user?.username}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate max-w-[120px]">
                    {user?.email}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={toggleDarkMode}
                className="flex-1 flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300 group"
              >
                {darkMode ? (
                  <Sun className="w-4 h-4 text-amber-500 group-hover:rotate-90 transition-transform duration-500" />
                ) : (
                  <Moon className="w-4 h-4 text-indigo-500 group-hover:-rotate-12 transition-transform duration-300" />
                )}
                <span className="text-sm font-medium">
                  {darkMode ? 'Light' : 'Dark'}
                </span>
              </button>

              <button
                onClick={handleLogout}
                className="p-2.5 rounded-xl bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 hover:bg-rose-200 dark:hover:bg-rose-900/50 transition-all duration-300 hover:scale-105"
                title="Logout"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between p-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <Menu className="w-6 h-6" />
          </button>
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <span className="font-display font-bold text-lg gradient-text">SmartSentinel</span>
          </div>
          <div className="w-10" /> {/* Spacer */}
        </div>
      </div>

      {/* Main content spacer for mobile */}
      <div className="lg:hidden h-16" />
    </>
  );
}

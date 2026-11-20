import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, AlertCircle, Eye, EyeOff, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-6 overflow-hidden relative">
      {/* Animated background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
      </div>

      <div className={`w-full max-w-md relative transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
        {/* Logo section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-6 shadow-2xl shadow-primary-500/30 animate-bounce-in">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-display font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-gray-400">Sign in to your SmartSentinel account</p>
        </div>

        {/* Form card */}
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-primary-500/20 to-accent-500/20 blur-xl rounded-3xl"></div>
          <div className="relative p-8 rounded-3xl bg-gray-900/80 backdrop-blur-xl border border-gray-800">
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="flex items-center space-x-3 p-4 rounded-xl bg-rose-900/30 border border-rose-500/30 text-rose-400 animate-scale-in">
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-300">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="input-field bg-gray-800/50 border-gray-700 focus:border-primary-500"
                  placeholder="Enter your username"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-300">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input-field bg-gray-800/50 border-gray-700 focus:border-primary-500 pr-12"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-primary-400 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="group relative w-full py-4 rounded-xl overflow-hidden transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-primary-500 via-purple-500 to-accent-500 animate-gradient-x"></span>
                <span className="relative flex items-center justify-center space-x-2 text-white font-semibold text-lg">
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span>Signing in...</span>
                    </>
                  ) : (
                    <>
                      <span>Sign In</span>
                      <Sparkles className="w-5 h-5 group-hover:animate-wiggle" />
                    </>
                  )}
                </span>
              </button>
            </form>

            <div className="mt-8 pt-6 border-t border-gray-800 text-center">
              <p className="text-gray-400">
                Don't have an account?{' '}
                <Link to="/register" className="text-primary-400 hover:text-primary-300 font-semibold transition-colors">
                  Sign up
                </Link>
              </p>
            </div>
          </div>
        </div>

        {/* Back to home link */}
        <div className="mt-6 text-center">
          <Link to="/" className="text-gray-500 hover:text-primary-400 transition-colors text-sm">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}

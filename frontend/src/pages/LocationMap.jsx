import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config';
import { MapPin, ExternalLink, Navigation, Globe, Compass } from 'lucide-react';
import 'leaflet/dist/leaflet.css';

export default function LocationMap() {
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLocation();
  }, []);

  const fetchLocation = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.LOCATION}`);
      setLocation(response.data);
    } catch (error) {
      console.error('Error fetching location:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !location) {
    return (
      <div className="lg:ml-64 p-8 flex items-center justify-center min-h-screen">
        <div className="relative">
          <div className="w-16 h-16 rounded-full border-4 border-primary-500/30 border-t-primary-500 animate-spin"></div>
          <div className="absolute inset-0 w-16 h-16 rounded-full border-4 border-accent-500/20 border-b-accent-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="lg:ml-64 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="animate-fade-in-up">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-bold gradient-text">Location Map</h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400 ml-13">Geographic view of security incidents</p>
        </div>

        {/* Map Card */}
        <div 
          className="card-glow p-6 opacity-0 animate-fade-in-up"
          style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
        >
          {/* Location Info Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center shadow-lg shadow-rose-500/20 flex-shrink-0">
                <MapPin className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="font-semibold text-lg mb-1">{location.address}</p>
                <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center space-x-1">
                    <Compass className="w-4 h-4" />
                    <span>Lat: {location.latitude.toFixed(4)}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Navigation className="w-4 h-4" />
                    <span>Lng: {location.longitude.toFixed(4)}</span>
                  </div>
                </div>
              </div>
            </div>
            <a
              href={location.google_maps_url}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-primary-500/10 to-accent-500/10 hover:from-primary-500 hover:to-accent-500 text-primary-600 dark:text-primary-400 hover:text-white font-semibold transition-all duration-300"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Open in Google Maps</span>
            </a>
          </div>

          {/* Map Container */}
          <div className="relative rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800">
            {/* Decorative corners */}
            <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-primary-500/50 rounded-tl-2xl z-10 pointer-events-none"></div>
            <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-primary-500/50 rounded-tr-2xl z-10 pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-primary-500/50 rounded-bl-2xl z-10 pointer-events-none"></div>
            <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-primary-500/50 rounded-br-2xl z-10 pointer-events-none"></div>
            
            <div className="h-96">
              <MapContainer
                center={[location.latitude, location.longitude]}
                zoom={13}
                style={{ height: '100%', width: '100%' }}
                className="z-0"
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <Marker position={[location.latitude, location.longitude]}>
                  <Popup>
                    <div className="p-2">
                      <p className="font-semibold">{location.address}</p>
                      <p className="text-sm text-gray-500">SmartSentinel Location</p>
                    </div>
                  </Popup>
                </Marker>
              </MapContainer>
            </div>
          </div>

          {/* Info Box */}
          <div 
            className="mt-6 p-5 rounded-xl bg-gradient-to-r from-cyan-500/10 via-transparent to-blue-500/10 border border-cyan-500/20 opacity-0 animate-fade-in-up"
            style={{ animationDelay: '300ms', animationFillMode: 'forwards' }}
          >
            <div className="flex items-start space-x-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-cyan-500/20">
                <MapPin className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-gray-900 dark:text-white mb-1">Incident Location Tracking</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  This map displays the geographic location where security incidents are detected. 
                  All incidents are tagged with precise coordinates for accurate reporting and response.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

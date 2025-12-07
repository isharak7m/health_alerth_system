import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { AlertTriangle, Shield, MessageCircle, Settings, LogOut } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [healthData, setHealthData] = useState(null);
  const [notifications, setNotifications] = useState(false);
  const [filterLocation, setFilterLocation] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [showAlerts, setShowAlerts] = useState(false);
  const [showAllOutbreaks, setShowAllOutbreaks] = useState(false);
  const [showAllVaccinations, setShowAllVaccinations] = useState(false);
  const [allOutbreaks, setAllOutbreaks] = useState([]);
  const [allVaccinations, setAllVaccinations] = useState([]);
  const [outbreakPage, setOutbreakPage] = useState(1);
  const [vaccinationPage, setVaccinationPage] = useState(1);
  const [outbreakPagination, setOutbreakPagination] = useState({});
  const [vaccinationPagination, setVaccinationPagination] = useState({});

  useEffect(() => {
    fetchHealthData();
    fetchAlerts();
    setNotifications(user?.notifications || false);
  }, [user, filterLocation]);

  useEffect(() => {
    if (showAllOutbreaks) {
      fetchAllOutbreaks();
    }
  }, [outbreakPage, showAllOutbreaks]);

  useEffect(() => {
    if (showAllVaccinations) {
      fetchAllVaccinations();
    }
  }, [vaccinationPage, showAllVaccinations]);

  const fetchHealthData = async () => {
    try {
      const response = await axios.get(`/api/health/location-data?filter_location=${filterLocation}`);
      setHealthData(response.data);
    } catch (error) {
      console.error('Failed to fetch health data:', error);
    }
  };

  const fetchAlerts = async () => {
    try {
      const response = await axios.get('/api/health/alerts');
      setAlerts(response.data.alerts);
      if (response.data.alerts.length > 0) {
        setShowAlerts(true);
      }
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    }
  };

  const toggleNotifications = async () => {
    try {
      await axios.put('/api/users/me', { notifications: !notifications });
      setNotifications(!notifications);
    } catch (error) {
      console.error('Failed to update notifications:', error);
    }
  };

  const fetchAllOutbreaks = async () => {
    try {
      const response = await axios.get(`/api/health/outbreaks?page=${outbreakPage}&limit=10`);
      setAllOutbreaks(response.data.items || response.data);
      setOutbreakPagination(response.data);
    } catch (error) {
      console.error('Failed to fetch all outbreaks:', error);
    }
  };

  const fetchAllVaccinations = async () => {
    try {
      const response = await axios.get(`/api/health/vaccinations?page=${vaccinationPage}&limit=10`);
      setAllVaccinations(response.data.items || response.data);
      setVaccinationPagination(response.data);
    } catch (error) {
      console.error('Failed to fetch all vaccinations:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Health Monitoring System</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.full_name}</span>
              {user?.role === 'admin' && (
                <Link to="/admin" className="text-indigo-600 hover:text-indigo-500">
                  Admin Panel
                </Link>
              )}
              <Link to="/chat" className="text-indigo-600 hover:text-indigo-500">
                <MessageCircle className="h-5 w-5" />
              </Link>
              <button onClick={logout} className="text-gray-500 hover:text-gray-700">
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-6 flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900">Health Dashboard</h2>
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={filterLocation}
                  onChange={(e) => setFilterLocation(e.target.checked)}
                  className="mr-2"
                />
                <span className="text-sm text-gray-700">Filter by my location</span>
              </label>
            </div>
          </div>

          {showAlerts && alerts.length > 0 && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-semibold text-red-800">⚠️ Health Alerts</h3>
                <button
                  onClick={() => setShowAlerts(false)}
                  className="text-red-600 hover:text-red-800"
                >
                  ✕
                </button>
              </div>
              <div className="space-y-2">
                {alerts.map((alert, index) => (
                  <div key={index} className={`p-2 rounded ${
                    alert.severity === 'high' ? 'bg-red-100' :
                    alert.severity === 'moderate' ? 'bg-yellow-100' : 'bg-blue-100'
                  }`}>
                    <p className="font-medium">{alert.title}</p>
                    <p className="text-sm">{alert.message}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <AlertTriangle className="h-6 w-6 text-red-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Active Outbreaks
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {healthData?.outbreaks?.length || 0}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Shield className="h-6 w-6 text-green-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Vaccination Campaigns
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {healthData?.vaccinations?.length || 0}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Settings className="h-6 w-6 text-blue-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Notifications
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        <button
                          onClick={toggleNotifications}
                          className={`px-3 py-1 rounded-full text-sm ${
                            notifications 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {notifications ? 'Enabled' : 'Disabled'}
                        </button>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    {filterLocation ? `Recent Outbreaks in ${user?.district}, ${user?.state}` : 'Recent Outbreaks (All Regions)'}
                  </h3>
                  <button
                    onClick={() => {
                      if (!showAllOutbreaks) {
                        fetchAllOutbreaks();
                      }
                      setShowAllOutbreaks(!showAllOutbreaks);
                    }}
                    className="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                  >
                    {showAllOutbreaks ? 'Show Less' : 'View All'}
                  </button>
                </div>
                <div className="space-y-3">
                  {(showAllOutbreaks ? allOutbreaks : healthData?.outbreaks?.slice(0, 5))?.map((outbreak) => (
                    <div key={outbreak.id} className="border-l-4 border-red-400 pl-4">
                      <div className="flex justify-between">
                        <p className="text-sm font-medium text-gray-900">{outbreak.disease}</p>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          outbreak.severity === 'high' ? 'bg-red-100 text-red-800' :
                          outbreak.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {outbreak.severity}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500">{outbreak.cases_reported} cases in {outbreak.district}, {outbreak.state}</p>
                    </div>
                  ))}
                </div>
                {showAllOutbreaks && outbreakPagination.pages > 1 && (
                  <div className="mt-4 flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                      Showing {((outbreakPage - 1) * 10) + 1} to {Math.min(outbreakPage * 10, outbreakPagination.total)} of {outbreakPagination.total} results
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setOutbreakPage(Math.max(1, outbreakPage - 1))}
                        disabled={outbreakPage === 1}
                        className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                      >
                        Previous
                      </button>
                      <span className="px-3 py-1 text-sm">
                        Page {outbreakPage} of {outbreakPagination.pages}
                      </span>
                      <button
                        onClick={() => setOutbreakPage(Math.min(outbreakPagination.pages, outbreakPage + 1))}
                        disabled={outbreakPage === outbreakPagination.pages}
                        className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    {filterLocation ? `Vaccination Campaigns in ${user?.district}, ${user?.state}` : 'Vaccination Campaigns (All Regions)'}
                  </h3>
                  <button
                    onClick={() => {
                      if (!showAllVaccinations) {
                        fetchAllVaccinations();
                      }
                      setShowAllVaccinations(!showAllVaccinations);
                    }}
                    className="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                  >
                    {showAllVaccinations ? 'Show Less' : 'View All'}
                  </button>
                </div>
                <div className="space-y-3">
                  {(showAllVaccinations ? allVaccinations : healthData?.vaccinations?.slice(0, 5))?.map((vaccination) => (
                    <div key={vaccination.id} className="border-l-4 border-green-400 pl-4">
                      <p className="text-sm font-medium text-gray-900">{vaccination.vaccine_name}</p>
                      <p className="text-sm text-gray-500">{vaccination.target_population} in {vaccination.district}, {vaccination.state}</p>
                      <p className="text-xs text-gray-400">
                        {vaccination.doses_administered}/{vaccination.doses_allocated} doses
                      </p>
                    </div>
                  ))}
                </div>
                {showAllVaccinations && vaccinationPagination.pages > 1 && (
                  <div className="mt-4 flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                      Showing {((vaccinationPage - 1) * 10) + 1} to {Math.min(vaccinationPage * 10, vaccinationPagination.total)} of {vaccinationPagination.total} results
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setVaccinationPage(Math.max(1, vaccinationPage - 1))}
                        disabled={vaccinationPage === 1}
                        className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                      >
                        Previous
                      </button>
                      <span className="px-3 py-1 text-sm">
                        Page {vaccinationPage} of {vaccinationPagination.pages}
                      </span>
                      <button
                        onClick={() => setVaccinationPage(Math.min(vaccinationPagination.pages, vaccinationPage + 1))}
                        disabled={vaccinationPage === vaccinationPagination.pages}
                        className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
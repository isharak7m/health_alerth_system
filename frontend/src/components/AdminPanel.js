import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Plus, Edit, Trash2, Users, AlertTriangle, Shield, Upload } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [outbreaks, setOutbreaks] = useState([]);
  const [vaccinations, setVaccinations] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersRes, outbreaksRes, vaccinationsRes] = await Promise.all([
        axios.get('/api/admin/users'),
        axios.get('/api/health/outbreaks?limit=100'),
        axios.get('/api/health/vaccinations?limit=100')
      ]);
      setUsers(Array.isArray(usersRes.data) ? usersRes.data : []);
      setOutbreaks(outbreaksRes.data?.items || []);
      setVaccinations(vaccinationsRes.data?.items || []);
    } catch (error) {
      toast.error('Failed to fetch data');
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await axios.delete(`/api/admin/users/${userId}`);
        setUsers(users.filter(u => u.id !== userId));
        toast.success('User deleted successfully');
      } catch (error) {
        toast.error('Failed to delete user');
      }
    }
  };

  const deleteOutbreak = async (outbreakId) => {
    if (window.confirm('Are you sure you want to delete this outbreak?')) {
      try {
        await axios.delete(`/api/admin/outbreaks/${outbreakId}`);
        setOutbreaks(outbreaks.filter(o => o.id !== outbreakId));
        toast.success('Outbreak deleted successfully');
      } catch (error) {
        toast.error('Failed to delete outbreak');
      }
    }
  };

  const deleteVaccination = async (vaccinationId) => {
    if (window.confirm('Are you sure you want to delete this vaccination?')) {
      try {
        await axios.delete(`/api/admin/vaccinations/${vaccinationId}`);
        setVaccinations(vaccinations.filter(v => v.id !== vaccinationId));
        toast.success('Vaccination deleted successfully');
      } catch (error) {
        toast.error('Failed to delete vaccination');
      }
    }
  };

  const openModal = (type, item = null) => {
    setModalType(type);
    setEditingItem(item);
    setShowModal(true);
  };

  const uploadCSV = async (event, type) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = type === 'outbreaks' ? '/api/admin/outbreaks/upload-csv' : '/api/admin/vaccinations/upload-csv';
      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success(response.data.message);
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'CSV upload failed');
    }
    
    // Reset file input
    event.target.value = '';
  };

  const Modal = () => {
    const [formData, setFormData] = useState(editingItem || {});

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        if (editingItem) {
          // Update
          if (modalType === 'outbreak') {
            await axios.put(`/api/admin/outbreaks/${editingItem.id}`, formData);
            toast.success('Outbreak updated successfully');
          } else if (modalType === 'vaccination') {
            await axios.put(`/api/admin/vaccinations/${editingItem.id}`, formData);
            toast.success('Vaccination updated successfully');
          }
        } else {
          // Create
          if (modalType === 'outbreak') {
            await axios.post('/api/admin/outbreaks', formData);
            toast.success('Outbreak created successfully');
          } else if (modalType === 'vaccination') {
            await axios.post('/api/admin/vaccinations', formData);
            toast.success('Vaccination created successfully');
          }
        }
        setShowModal(false);
        fetchData();
      } catch (error) {
        toast.error('Operation failed');
      }
    };

    return (
      <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 className="text-lg font-medium mb-4">
            {editingItem ? 'Edit' : 'Create'} {modalType}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            {modalType === 'outbreak' && (
              <>
                <input
                  type="text"
                  placeholder="Outbreak ID"
                  className="w-full p-2 border rounded"
                  value={formData.outbreak_id || ''}
                  onChange={(e) => setFormData({...formData, outbreak_id: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="Disease"
                  className="w-full p-2 border rounded"
                  value={formData.disease || ''}
                  onChange={(e) => setFormData({...formData, disease: e.target.value})}
                  required
                />
                <input
                  type="datetime-local"
                  placeholder="Report Date"
                  className="w-full p-2 border rounded"
                  value={formData.report_date || ''}
                  onChange={(e) => setFormData({...formData, report_date: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="State"
                  className="w-full p-2 border rounded"
                  value={formData.state || ''}
                  onChange={(e) => setFormData({...formData, state: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="District"
                  className="w-full p-2 border rounded"
                  value={formData.district || ''}
                  onChange={(e) => setFormData({...formData, district: e.target.value})}
                  required
                />
                <input
                  type="number"
                  placeholder="Cases Reported"
                  className="w-full p-2 border rounded"
                  value={formData.cases_reported || ''}
                  onChange={(e) => setFormData({...formData, cases_reported: parseInt(e.target.value) || 0})}
                  required
                />
                <input
                  type="number"
                  placeholder="Deaths"
                  className="w-full p-2 border rounded"
                  value={formData.deaths || ''}
                  onChange={(e) => setFormData({...formData, deaths: parseInt(e.target.value) || 0})}
                  required
                />
                <input
                  type="text"
                  placeholder="Country"
                  className="w-full p-2 border rounded"
                  value={formData.country || 'India'}
                  onChange={(e) => setFormData({...formData, country: e.target.value})}
                  required
                />
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.confirmed || false}
                    onChange={(e) => setFormData({...formData, confirmed: e.target.checked})}
                    className="mr-2"
                  />
                  Confirmed
                </label>
                <select
                  className="w-full p-2 border rounded"
                  value={formData.severity || ''}
                  onChange={(e) => setFormData({...formData, severity: e.target.value})}
                  required
                >
                  <option value="">Select Severity</option>
                  <option value="low">Low</option>
                  <option value="moderate">Moderate</option>
                  <option value="high">High</option>
                </select>
              </>
            )}
            {modalType === 'vaccination' && (
              <>
                <input
                  type="text"
                  placeholder="Campaign ID"
                  className="w-full p-2 border rounded"
                  value={formData.campaign_id || ''}
                  onChange={(e) => setFormData({...formData, campaign_id: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="Country"
                  className="w-full p-2 border rounded"
                  value={formData.country || 'India'}
                  onChange={(e) => setFormData({...formData, country: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="Vaccine Name"
                  className="w-full p-2 border rounded"
                  value={formData.vaccine_name || ''}
                  onChange={(e) => setFormData({...formData, vaccine_name: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="State"
                  className="w-full p-2 border rounded"
                  value={formData.state || ''}
                  onChange={(e) => setFormData({...formData, state: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="District"
                  className="w-full p-2 border rounded"
                  value={formData.district || ''}
                  onChange={(e) => setFormData({...formData, district: e.target.value})}
                  required
                />
                <input
                  type="datetime-local"
                  placeholder="Start Date"
                  className="w-full p-2 border rounded"
                  value={formData.start_date || ''}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  required
                />
                <input
                  type="datetime-local"
                  placeholder="End Date"
                  className="w-full p-2 border rounded"
                  value={formData.end_date || ''}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="Target Population"
                  className="w-full p-2 border rounded"
                  value={formData.target_population || ''}
                  onChange={(e) => setFormData({...formData, target_population: e.target.value})}
                  required
                />
                <input
                  type="number"
                  placeholder="Doses Allocated"
                  className="w-full p-2 border rounded"
                  value={formData.doses_allocated || ''}
                  onChange={(e) => setFormData({...formData, doses_allocated: parseInt(e.target.value) || 0})}
                  required
                />
                <input
                  type="number"
                  placeholder="Doses Administered"
                  className="w-full p-2 border rounded"
                  value={formData.doses_administered || ''}
                  onChange={(e) => setFormData({...formData, doses_administered: parseInt(e.target.value) || 0})}
                  required
                />
              </>
            )}
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-gray-600 border rounded hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                {editingItem ? 'Update' : 'Create'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/dashboard" className="mr-4">
                <ArrowLeft className="h-5 w-5" />
              </Link>
              <h1 className="text-xl font-semibold">Admin Panel</h1>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('users')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'users'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Users className="h-5 w-5 inline mr-2" />
                Users
              </button>
              <button
                onClick={() => setActiveTab('outbreaks')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'outbreaks'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <AlertTriangle className="h-5 w-5 inline mr-2" />
                Outbreaks
              </button>
              <button
                onClick={() => setActiveTab('vaccinations')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'vaccinations'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Shield className="h-5 w-5 inline mr-2" />
                Vaccinations
              </button>
            </nav>
          </div>

          <div className="mt-6">
            {activeTab === 'users' && (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Users</h3>
                </div>
                <ul className="divide-y divide-gray-200">
                  {Array.isArray(users) && users.map((user) => (
                    <li key={user.id} className="px-4 py-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{user.full_name}</p>
                        <p className="text-sm text-gray-500">{user.email} • {user.role}</p>
                        <p className="text-sm text-gray-500">{user.district}, {user.state}</p>
                      </div>
                      <button
                        onClick={() => deleteUser(user.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {activeTab === 'outbreaks' && (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Outbreaks</h3>
                  <div className="flex space-x-2">
                    <label className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 cursor-pointer">
                      <Upload className="h-4 w-4 inline mr-2" />
                      Upload CSV
                      <input
                        type="file"
                        accept=".csv"
                        className="hidden"
                        onChange={(e) => uploadCSV(e, 'outbreaks')}
                      />
                    </label>
                    <button
                      onClick={() => openModal('outbreak')}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
                    >
                      <Plus className="h-4 w-4 inline mr-2" />
                      Add Outbreak
                    </button>
                  </div>
                </div>
                <ul className="divide-y divide-gray-200">
                  {Array.isArray(outbreaks) && outbreaks.map((outbreak) => (
                    <li key={outbreak.id} className="px-4 py-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{outbreak.disease}</p>
                        <p className="text-sm text-gray-500">{outbreak.district}, {outbreak.state}</p>
                        <p className="text-sm text-gray-500">{outbreak.cases_reported} cases • {outbreak.severity}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => openModal('outbreak', outbreak)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => deleteOutbreak(outbreak.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {activeTab === 'vaccinations' && (
              <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Vaccinations</h3>
                  <div className="flex space-x-2">
                    <label className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 cursor-pointer">
                      <Upload className="h-4 w-4 inline mr-2" />
                      Upload CSV
                      <input
                        type="file"
                        accept=".csv"
                        className="hidden"
                        onChange={(e) => uploadCSV(e, 'vaccinations')}
                      />
                    </label>
                    <button
                      onClick={() => openModal('vaccination')}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
                    >
                      <Plus className="h-4 w-4 inline mr-2" />
                      Add Vaccination
                    </button>
                  </div>
                </div>
                <ul className="divide-y divide-gray-200">
                  {Array.isArray(vaccinations) && vaccinations.map((vaccination) => (
                    <li key={vaccination.id} className="px-4 py-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{vaccination.vaccine_name}</p>
                        <p className="text-sm text-gray-500">{vaccination.district}, {vaccination.state}</p>
                        <p className="text-sm text-gray-500">{vaccination.target_population}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => openModal('vaccination', vaccination)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => deleteVaccination(vaccination.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>

      {showModal && <Modal />}
    </div>
  );
};

export default AdminPanel;
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
  requestPasswordReset: (email) => api.post('/auth/password-reset-request', { email }),
  confirmPasswordReset: (resetData) => api.post('/auth/password-reset-confirm', resetData),
  changePassword: (passwordData) => api.post('/auth/change-password', passwordData),
};

export const jobsAPI = {
  createJob: (jobData) => api.post('/jobs', jobData),
  getJobs: () => api.get('/jobs'),
  getJob: (id) => api.get(`/jobs/${id}`),
  updateJob: (id, jobData) => api.put(`/jobs/${id}`, jobData),
  deleteJob: (id) => api.delete(`/jobs/${id}`),
};

export const evaluationsAPI = {
  uploadCV: (jobId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/evaluations/${jobId}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getEvaluation: (id) => api.get(`/evaluations/${id}`),
  getJobCandidates: (jobId) => api.get(`/evaluations/job/${jobId}/candidates`),
  deleteEvaluation: (id) => api.delete(`/evaluations/${id}`),
};

export const usersAPI = {
  getProfile: () => api.get('/users/me'),
  getCompanyUsers: () => api.get('/users'),
  createCompany: (companyData) => api.post('/users/companies', companyData),
  getCompanies: () => api.get('/users/companies'),
};

export default api;
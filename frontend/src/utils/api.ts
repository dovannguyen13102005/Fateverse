import axios from 'axios';

const API_BASE_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Remove invalid token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('userInfo');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API endpoints
export const authAPI = {
  googleLogin: (credential: string) =>
    apiClient.post('/api/auth/google', { credential }),
  
  emailLogin: (email: string, password: string) =>
    apiClient.post('/api/auth/login', { email, password }),
  
  emailRegister: (data: { email: string; password: string; name: string; birth_date?: string; gender?: string }) =>
    apiClient.post('/api/auth/register', data),
  
  register: (userData: any) =>
    apiClient.post('/api/users/register', userData),
  
  getProfile: (userId: string) =>
    apiClient.get(`/api/users/profile/${userId}`),
  
  updateProfile: (userId: string, userData: any) =>
    apiClient.put(`/api/users/profile/${userId}`, userData),
  
  getStatistics: (userId: string) =>
    apiClient.get(`/api/users/statistics/${userId}`),
  
  exportData: (userId: string) =>
    apiClient.get(`/api/users/export/${userId}`),
  
  deleteAccount: (userId: string) =>
    apiClient.delete(`/api/users/account/${userId}`),
  
  logout: () =>
    apiClient.post('/api/auth/logout'),
};

// Fortune telling API endpoints
export const fortuneAPI = {
  numerology: (userId: string, data: any) =>
    apiClient.post(`/api/numerology/${userId}`, data),
  
  zodiac: (userId: string, data: any) =>
    apiClient.post(`/api/zodiac/${userId}`, data),
  
  loveMatch: (userId: string, data: any) =>
    apiClient.post(`/api/love/${userId}`, data),
  
  tarot: (userId: string, data: any) =>
    apiClient.post(`/api/tarot/${userId}`, data),
  
  dailyFortune: (userId: string) =>
    apiClient.get(`/api/fortune/${userId}`),
};

// History API endpoints
export const historyAPI = {
  getHistory: (userId: string, limit?: number) =>
    apiClient.get(`/api/history/${userId}`, { params: { limit } }),
  
  getHistoryByType: (userId: string, type: string, limit?: number) =>
    apiClient.get(`/api/history/type/${userId}/${type}`, { params: { limit } }),
  
  deleteHistory: (historyId: string) =>
    apiClient.delete(`/api/history/${historyId}`),
  
  deleteAllHistory: (userId: string) =>
    apiClient.delete(`/api/history/user/${userId}/all`),
  
  toggleFavorite: (historyId: string) =>
    apiClient.post(`/api/history/${historyId}/favorite`),
  
  getFavorites: (userId: string, limit?: number) =>
    apiClient.get(`/api/history/${userId}/favorites`, { params: { limit } }),
  
  createShareLink: (historyId: string) =>
    apiClient.post(`/api/history/${historyId}/share`),
  
  getSharedFortune: (shareToken: string) =>
    apiClient.get(`/api/history/share/${shareToken}`),
  
  removeShareLink: (historyId: string) =>
    apiClient.delete(`/api/history/${historyId}/share`),
};

export default apiClient;
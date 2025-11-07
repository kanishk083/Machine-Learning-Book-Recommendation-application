// src/api.js - API Service Layer
import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Methods
export const bookAPI = {
  // Get all books with optional filters
  getAllBooks: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.category && filters.category !== 'All') {
      params.append('category', filters.category);
    }
    if (filters.search) {
      params.append('search', filters.search);
    }
    return api.get(`/books?${params.toString()}`);
  },

  // Get a specific book by ID
  getBookById: async (bookId) => {
    return api.get(`/book/${bookId}`);
  },

  // Get book recommendations
  getRecommendations: async (ratings, method = 'hybrid', n = 6) => {
    return api.post('/recommend', {
      ratings,
      method,
      n,
    });
  },

  // Get similar books
  getSimilarBooks: async (bookId, n = 5) => {
    return api.get(`/similar/${bookId}?n=${n}`);
  },

  // Get all categories
  getCategories: async () => {
    return api.get('/categories');
  },

  // Add user rating
  addRating: async (userId, bookId, rating) => {
    return api.post('/ratings', {
      user_id: userId,
      book_id: bookId,
      rating,
    });
  },

  // Get user ratings
  getUserRatings: async (userId) => {
    return api.get(`/ratings/${userId}`);
  },
};

export default api;


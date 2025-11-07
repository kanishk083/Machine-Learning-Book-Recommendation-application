// src/hooks/useBooks.js - Custom React Hooks
import { useState, useEffect } from 'react';
import { bookAPI } from '../api';

export const useBooks = (initialFilters = {}) => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(initialFilters);

  useEffect(() => {
    fetchBooks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  const fetchBooks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await bookAPI.getAllBooks(filters);
      setBooks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    books,
    loading,
    error,
    filters,
    setFilters,
    refetch: fetchBooks,
  };
};

export const useRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getRecommendations = async (ratings, method = 'hybrid', n = 6) => {
    setLoading(true);
    setError(null);
    try {
      const data = await bookAPI.getRecommendations(ratings, method, n);
      setRecommendations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    recommendations,
    loading,
    error,
    getRecommendations,
  };
};
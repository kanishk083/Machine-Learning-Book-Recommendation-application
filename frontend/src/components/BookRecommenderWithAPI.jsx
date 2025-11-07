// src/components/BookRecommenderWithAPI.jsx
import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Star, Brain, TrendingUp, Filter, X, Loader } from 'lucide-react';
import { bookAPI } from '../api';

const BookRecommenderWithAPI = () => {
  const [books, setBooks] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [categories, setCategories] = useState(['All']);
  const [recommendations, setRecommendations] = useState([]);
  const [view, setView] = useState('browse');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load books and categories on mount
  useEffect(() => {
    loadInitialData();
  }, []);

  // Reload books when filters change (skip initial mount)
  useEffect(() => {
    // Skip if this is the initial mount (books haven't been loaded yet)
    if (books.length > 0 || searchTerm !== '' || selectedCategory !== 'All') {
      loadBooks();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm, selectedCategory]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [booksData, categoriesData] = await Promise.all([
        bookAPI.getAllBooks(),
        bookAPI.getCategories(),
      ]);
      setBooks(booksData);
      setCategories(categoriesData);
    } catch (err) {
      setError('Failed to load data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadBooks = async () => {
    try {
      setLoading(true);
      const data = await bookAPI.getAllBooks({
        category: selectedCategory,
        search: searchTerm,
      });
      setBooks(data);
    } catch (err) {
      setError('Failed to load books: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRating = (bookId, rating) => {
    setUserRatings({ ...userRatings, [bookId]: rating });
  };

  const generateRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await bookAPI.getRecommendations(userRatings, 'hybrid', 6);
      setRecommendations(data);
      setView('recommendations');
    } catch (err) {
      setError('Failed to generate recommendations: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return 'bg-green-100 text-green-700';
      case 'Intermediate': return 'bg-blue-100 text-blue-700';
      case 'Advanced': return 'bg-purple-100 text-purple-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6 flex items-center justify-center">
        <div className="bg-red-500/20 border border-red-500 rounded-lg p-6 max-w-md">
          <h2 className="text-red-200 text-xl font-bold mb-2">Error</h2>
          <p className="text-red-100">{error}</p>
          <button
            onClick={loadInitialData}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Brain className="w-12 h-12 text-purple-400" />
            <h1 className="text-5xl font-bold text-white">Tech Book Recommender</h1>
          </div>
          <p className="text-purple-200 text-lg">ML • DL • DS • RL • Python • Algorithms & More</p>
        </div>

        {/* Navigation */}
        <div className="flex gap-4 mb-6 justify-center">
          <button
            onClick={() => setView('browse')}
            className={`px-6 py-3 rounded-lg font-semibold transition flex items-center gap-2 ${
              view === 'browse' ? 'bg-purple-600 text-white' : 'bg-white/10 text-white hover:bg-white/20'
            }`}
          >
            <BookOpen className="w-5 h-5" />
            Browse & Rate
          </button>
          <button
            onClick={generateRecommendations}
            disabled={Object.keys(userRatings).length === 0 || loading}
            className={`px-6 py-3 rounded-lg font-semibold transition flex items-center gap-2 ${
              view === 'recommendations' ? 'bg-purple-600 text-white' : 'bg-white/10 text-white hover:bg-white/20'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {loading ? <Loader className="w-5 h-5 animate-spin" /> : <TrendingUp className="w-5 h-5" />}
            Get Recommendations ({Object.keys(userRatings).length})
          </button>
        </div>

        {view === 'browse' && (
          <div className="space-y-6">
            {/* Search & Filter */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-3.5 text-purple-300 w-5 h-5" />
                  <input
                    type="text"
                    placeholder="Search by title or author..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>
                <div className="relative">
                  <Filter className="absolute left-3 top-3.5 text-purple-300 w-5 h-5" />
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    {categories.map(cat => (
                      <option key={cat} value={cat} className="bg-slate-800">{cat}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Loading State */}
            {loading && (
              <div className="flex items-center justify-center py-12">
                <Loader className="w-8 h-8 text-purple-400 animate-spin" />
                <span className="ml-3 text-purple-200">Loading books...</span>
              </div>
            )}

            {/* Books Grid */}
            {!loading && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {books.map(book => (
                  <div key={book.book_id} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 hover:bg-white/15 transition">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="font-bold text-lg text-white mb-1">{book.title}</h3>
                        <p className="text-purple-200 text-sm mb-2">{book.author}</p>
                        <div className="flex flex-wrap gap-2 mb-3">
                          <span className="text-xs px-2 py-1 bg-purple-500/30 text-purple-200 rounded">
                            {book.category}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ${getLevelColor(book.level)}`}>
                            {book.level}
                          </span>
                          <span className="text-xs px-2 py-1 bg-white/10 text-white rounded">
                            {book.year}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 mb-3">
                          <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                          <span className="text-sm font-semibold text-white">{book.rating}</span>
                          <span className="text-xs text-purple-300 ml-1">avg rating</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="border-t border-white/20 pt-3">
                      <p className="text-sm text-purple-200 mb-2">Your Rating:</p>
                      <div className="flex gap-2">
                        {[1, 2, 3, 4, 5].map(star => (
                          <button
                            key={star}
                            onClick={() => handleRating(book.book_id, star)}
                            className="transition hover:scale-110"
                          >
                            <Star
                              className={`w-7 h-7 ${
                                userRatings[book.book_id] >= star
                                  ? 'text-yellow-400 fill-yellow-400'
                                  : 'text-white/30'
                              }`}
                            />
                          </button>
                        ))}
                        {userRatings[book.book_id] && (
                          <button
                            onClick={() => {
                              const newRatings = { ...userRatings };
                              delete newRatings[book.book_id];
                              setUserRatings(newRatings);
                            }}
                            className="ml-2 text-red-400 hover:text-red-300"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {view === 'recommendations' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
            <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
              <Brain className="w-8 h-8 text-purple-400" />
              Recommended for You
            </h2>
            
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader className="w-8 h-8 text-purple-400 animate-spin" />
                <span className="ml-3 text-purple-200">Generating recommendations...</span>
              </div>
            ) : recommendations.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-purple-200 text-lg mb-4">Rate some books with 4+ stars to get personalized recommendations!</p>
                <button
                  onClick={() => setView('browse')}
                  className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition"
                >
                  Start Rating Books
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {recommendations.map((book, index) => (
                  <div key={book.book_id} className="bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl p-6 border border-purple-400/30 hover:border-purple-400/50 transition">
                    <div className="flex items-start gap-3 mb-3">
                      <div className="bg-purple-500 text-white font-bold text-xl w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-white mb-1 leading-tight">{book.title}</h3>
                        <p className="text-purple-200 text-sm mb-2">{book.author}</p>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-2 mb-3">
                      <span className="text-xs px-2 py-1 bg-purple-500/30 text-purple-200 rounded">
                        {book.category}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded ${getLevelColor(book.level)}`}>
                        {book.level}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                      <span className="text-sm font-semibold text-white">{book.rating}</span>
                      <span className="text-xs text-purple-300 ml-1">• {book.year}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            <button
              onClick={() => setView('browse')}
              className="w-full mt-6 bg-white/10 text-white py-3 rounded-lg font-semibold hover:bg-white/20 transition border border-white/20"
            >
              Back to Browse
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BookRecommenderWithAPI;
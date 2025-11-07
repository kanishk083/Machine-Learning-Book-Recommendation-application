// Placeholder file for `BookRecommender.jsx` component. No implementation code as requested.
// BookRecommender.jsx
// Save this as: frontend/src/components/BookRecommender.jsx

import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Star, Code, Brain, TrendingUp, Filter, X } from 'lucide-react';

const TechBookRecommender = () => {
  const [books, setBooks] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [recommendations, setRecommendations] = useState([]);
  const [view, setView] = useState('browse');

  const categories = ['All', 'Machine Learning', 'Deep Learning', 'Data Science', 'Reinforcement Learning', 'Python', 'Algorithms', 'Computer Vision', 'NLP', 'MLOps'];

  const techBooks = [
    { id: 1, title: "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", author: "Aurélien Géron", category: "Machine Learning", level: "Intermediate", rating: 4.6, year: 2022 },
    { id: 2, title: "Deep Learning", author: "Ian Goodfellow, Yoshua Bengio, Aaron Courville", category: "Deep Learning", level: "Advanced", rating: 4.5, year: 2016 },
    { id: 3, title: "Python Machine Learning", author: "Sebastian Raschka", category: "Machine Learning", level: "Intermediate", rating: 4.4, year: 2019 },
    { id: 4, title: "Reinforcement Learning: An Introduction", author: "Richard S. Sutton, Andrew G. Barto", category: "Reinforcement Learning", level: "Advanced", rating: 4.7, year: 2018 },
    { id: 5, title: "Pattern Recognition and Machine Learning", author: "Christopher M. Bishop", category: "Machine Learning", level: "Advanced", rating: 4.6, year: 2006 },
    { id: 6, title: "Deep Learning with Python", author: "François Chollet", category: "Deep Learning", level: "Beginner", rating: 4.5, year: 2021 },
    { id: 7, title: "The Hundred-Page Machine Learning Book", author: "Andriy Burkov", category: "Machine Learning", level: "Beginner", rating: 4.3, year: 2019 },
    { id: 8, title: "Python for Data Analysis", author: "Wes McKinney", category: "Data Science", level: "Beginner", rating: 4.4, year: 2022 },
    { id: 9, title: "Introduction to Statistical Learning", author: "Gareth James, Daniela Witten", category: "Machine Learning", level: "Intermediate", rating: 4.6, year: 2021 },
    { id: 10, title: "Natural Language Processing with Python", author: "Steven Bird, Ewan Klein", category: "NLP", level: "Intermediate", rating: 4.2, year: 2009 },
    { id: 11, title: "Computer Vision: Algorithms and Applications", author: "Richard Szeliski", category: "Computer Vision", level: "Advanced", rating: 4.5, year: 2022 },
    { id: 12, title: "Designing Machine Learning Systems", author: "Chip Huyen", category: "MLOps", level: "Intermediate", rating: 4.7, year: 2022 },
    { id: 13, title: "Grokking Deep Learning", author: "Andrew Trask", category: "Deep Learning", level: "Beginner", rating: 4.4, year: 2019 },
    { id: 14, title: "Data Science from Scratch", author: "Joel Grus", category: "Data Science", level: "Beginner", rating: 4.3, year: 2019 },
    { id: 15, title: "Algorithms", author: "Robert Sedgewick, Kevin Wayne", category: "Algorithms", level: "Intermediate", rating: 4.5, year: 2011 },
    { id: 16, title: "Deep Reinforcement Learning Hands-On", author: "Maxim Lapan", category: "Reinforcement Learning", level: "Intermediate", rating: 4.4, year: 2020 },
    { id: 17, title: "Fluent Python", author: "Luciano Ramalho", category: "Python", level: "Intermediate", rating: 4.7, year: 2022 },
    { id: 18, title: "Speech and Language Processing", author: "Dan Jurafsky, James H. Martin", category: "NLP", level: "Advanced", rating: 4.6, year: 2023 },
    { id: 19, title: "Machine Learning Engineering", author: "Andriy Burkov", category: "MLOps", level: "Intermediate", rating: 4.5, year: 2020 },
    { id: 20, title: "Probabilistic Machine Learning: An Introduction", author: "Kevin Murphy", category: "Machine Learning", level: "Advanced", rating: 4.6, year: 2022 },
    { id: 21, title: "Deep Learning for Computer Vision", author: "Rajalingappaa Shanmugamani", category: "Computer Vision", level: "Intermediate", rating: 4.3, year: 2018 },
    { id: 22, title: "Python Data Science Handbook", author: "Jake VanderPlas", category: "Data Science", level: "Intermediate", rating: 4.5, year: 2016 },
    { id: 23, title: "Introduction to Algorithms", author: "Thomas H. Cormen", category: "Algorithms", level: "Advanced", rating: 4.5, year: 2009 },
    { id: 24, title: "Effective Python", author: "Brett Slatkin", category: "Python", level: "Intermediate", rating: 4.5, year: 2019 },
    { id: 25, title: "Neural Networks and Deep Learning", author: "Michael Nielsen", category: "Deep Learning", level: "Beginner", rating: 4.7, year: 2015 },
  ];

  useEffect(() => {
    setBooks(techBooks);
  }, []);

  const filteredBooks = books.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || book.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleRating = (bookId, rating) => {
    setUserRatings({ ...userRatings, [bookId]: rating });
  };

  const generateRecommendations = () => {
    const ratedBookIds = Object.keys(userRatings).map(Number);
    const ratedBooks = books.filter(b => ratedBookIds.includes(b.id));
    
    // Get highly rated books (4+ stars)
    const likedBooks = ratedBooks.filter(b => userRatings[b.id] >= 4);
    
    if (likedBooks.length === 0) {
      setRecommendations([]);
      setView('recommendations');
      return;
    }

    // Extract preferred categories and levels
    const preferredCategories = [...new Set(likedBooks.map(b => b.category))];
    const preferredLevels = [...new Set(likedBooks.map(b => b.level))];
    
    // Calculate recommendation score
    const unratedBooks = books.filter(b => !ratedBookIds.includes(b.id));
    const scored = unratedBooks.map(book => {
      let score = 0;
      
      // Category match (highest weight)
      if (preferredCategories.includes(book.category)) score += 50;
      
      // Level match
      if (preferredLevels.includes(book.level)) score += 20;
      
      // Book rating
      score += book.rating * 10;
      
      // Recency bonus (newer books get slight boost)
      if (book.year >= 2020) score += 5;
      
      return { ...book, score };
    });

    // Sort by score and take top 6
    const topRecommendations = scored
      .sort((a, b) => b.score - a.score)
      .slice(0, 6);
    
    setRecommendations(topRecommendations);
    setView('recommendations');
  };

  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return 'bg-green-100 text-green-700';
      case 'Intermediate': return 'bg-blue-100 text-blue-700';
      case 'Advanced': return 'bg-purple-100 text-purple-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

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
            disabled={Object.keys(userRatings).length === 0}
            className={`px-6 py-3 rounded-lg font-semibold transition flex items-center gap-2 ${
              view === 'recommendations' ? 'bg-purple-600 text-white' : 'bg-white/10 text-white hover:bg-white/20'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            <TrendingUp className="w-5 h-5" />
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

            {/* Books Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {filteredBooks.map(book => (
                <div key={book.id} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 hover:bg-white/15 transition">
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
                          onClick={() => handleRating(book.id, star)}
                          className="transition hover:scale-110"
                        >
                          <Star
                            className={`w-7 h-7 ${
                              userRatings[book.id] >= star
                                ? 'text-yellow-400 fill-yellow-400'
                                : 'text-white/30'
                            }`}
                          />
                        </button>
                      ))}
                      {userRatings[book.id] && (
                        <button
                          onClick={() => {
                            const newRatings = { ...userRatings };
                            delete newRatings[book.id];
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
          </div>
        )}

        {view === 'recommendations' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
            <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
              <Code className="w-8 h-8 text-purple-400" />
              Recommended for You
            </h2>
            
            {recommendations.length === 0 ? (
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
                  <div key={book.id} className="bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl p-6 border border-purple-400/30 hover:border-purple-400/50 transition">
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

export default TechBookRecommender;
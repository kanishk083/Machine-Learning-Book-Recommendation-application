import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


class ContentBasedRecommender:
    """Content-based filtering using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=100)
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.books_df = None
        
    def fit(self, books_df):
        """Train the model on book features"""
        self.books_df = books_df.copy()
        
        # Create content features
        self.books_df['content'] = (
            self.books_df['title'] + ' ' + 
            self.books_df['category'] + ' ' + 
            self.books_df['level'] + ' ' +
            self.books_df['author']
        )
        
        # Fit TF-IDF
        self.tfidf_matrix = self.tfidf.fit_transform(self.books_df['content'])
        
        # Calculate cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        print(f"✓ Content-based model trained on {len(self.books_df)} books")
        
    def recommend(self, book_ids, n_recommendations=5):
        """Get recommendations based on book IDs"""
        if not book_ids:
            return []
        
        # Get indices
        indices = [self.books_df[self.books_df['book_id'] == bid].index[0] 
                   for bid in book_ids if bid in self.books_df['book_id'].values]
        
        if not indices:
            return []
        
        # Average similarity scores
        sim_scores = np.mean([self.cosine_sim[idx] for idx in indices], axis=0)
        sim_scores = list(enumerate(sim_scores))
        
        # Sort and exclude input books
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] not in indices]
        
        # Get top N
        top_indices = [i[0] for i in sim_scores[:n_recommendations]]
        
        return self.books_df.iloc[top_indices][['book_id', 'title', 'author', 'rating']].to_dict('records')
    
    def save_model(self, path='models/content_based_model.pkl'):
        """Save the trained model"""
        with open(path, 'wb') as f:
            pickle.dump({
                'tfidf': self.tfidf,
                'tfidf_matrix': self.tfidf_matrix,
                'cosine_sim': self.cosine_sim,
                'books_df': self.books_df
            }, f)
        print(f"✓ Model saved to {path}")
    
    def load_model(self, path='models/content_based_model.pkl'):
        """Load a trained model"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.tfidf = data['tfidf']
            self.tfidf_matrix = data['tfidf_matrix']
            self.cosine_sim = data['cosine_sim']
            self.books_df = data['books_df']
        print(f"✓ Model loaded from {path}")
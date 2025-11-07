import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import pickle



class CollaborativeFilteringRecommender:
    """Collaborative filtering using matrix factorization (SVD)"""
    
    def __init__(self, n_components=10):
        self.n_components = n_components
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        self.user_factors = None
        self.item_factors = None
        self.user_item_matrix = None
        self.books_df = None
        
    def fit(self, user_item_matrix, books_df):
        """Train the model on user-item rating matrix"""
        self.user_item_matrix = user_item_matrix
        self.books_df = books_df
        
        # Apply SVD
        self.user_factors = self.svd.fit_transform(user_item_matrix)
        self.item_factors = self.svd.components_.T
        
        print(f"✓ Collaborative filtering model trained with {self.n_components} factors")
        
    def predict_rating(self, user_idx, book_id):
        """Predict rating for a user-book pair"""
        book_idx = self.books_df[self.books_df['book_id'] == book_id].index[0]
        prediction = np.dot(self.user_factors[user_idx], self.item_factors[book_idx])
        return max(0, min(5, prediction))  # Clip to [0, 5]
    
    def recommend_for_user(self, user_idx, n_recommendations=5):
        """Get recommendations for a specific user"""
        # Predict ratings for all books
        predictions = np.dot(self.user_factors[user_idx], self.item_factors.T)
        
        # Get books not yet rated
        rated_books = self.user_item_matrix.iloc[user_idx]
        unrated_indices = rated_books[rated_books == 0].index
        
        # Sort predictions
        unrated_predictions = [(idx, predictions[i]) for i, idx in enumerate(unrated_indices)]
        unrated_predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N
        top_book_ids = [self.books_df.iloc[idx]['book_id'] for idx, _ in unrated_predictions[:n_recommendations]]
        
        return self.books_df[self.books_df['book_id'].isin(top_book_ids)].to_dict('records')
    
    def save_model(self, path='models/collaborative_model.pkl'):
        """Save the trained model"""
        with open(path, 'wb') as f:
            pickle.dump({
                'svd': self.svd,
                'user_factors': self.user_factors,
                'item_factors': self.item_factors,
                'user_item_matrix': self.user_item_matrix,
                'books_df': self.books_df
            }, f)
        print(f"✓ Model saved to {path}")

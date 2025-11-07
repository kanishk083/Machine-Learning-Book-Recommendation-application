from sklearn.neighbors import NearestNeighbors


class KNNRecommender:
    """K-Nearest Neighbors based recommendation"""
    
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
        self.books_df = None
        self.feature_matrix = None
        
    def fit(self, books_df):
        """Train KNN model"""
        self.books_df = books_df.copy()
        
        # Create feature matrix (numerical features)
        from sklearn.preprocessing import LabelEncoder
        
        le_cat = LabelEncoder()
        le_level = LabelEncoder()
        
        self.books_df['category_encoded'] = le_cat.fit_transform(self.books_df['category'])
        self.books_df['level_encoded'] = le_level.fit_transform(self.books_df['level'])
        
        # Normalize year
        self.books_df['year_normalized'] = (
            (self.books_df['year'] - self.books_df['year'].min()) / 
            (self.books_df['year'].max() - self.books_df['year'].min())
        )
        
        # Create feature matrix
        self.feature_matrix = self.books_df[
            ['category_encoded', 'level_encoded', 'rating', 'year_normalized']
        ].values
        
        # Fit KNN
        self.knn.fit(self.feature_matrix)
        
        print(f"✓ KNN model trained with k={self.n_neighbors}")
        
    def recommend(self, book_id, n_recommendations=5):
        """Get similar books using KNN"""
        book_idx = self.books_df[self.books_df['book_id'] == book_id].index[0]
        book_features = self.feature_matrix[book_idx].reshape(1, -1)
        
        # Find nearest neighbors
        distances, indices = self.knn.kneighbors(book_features, n_neighbors=n_recommendations+1)
        
        # Exclude the book itself
        similar_indices = [idx for idx in indices[0] if idx != book_idx][:n_recommendations]
        
        return self.books_df.iloc[similar_indices][['book_id', 'title', 'author', 'rating']].to_dict('records')
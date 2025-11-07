

class HybridRecommender:
    """Hybrid recommendation combining multiple approaches"""
    
    def __init__(self, content_weight=0.5, collab_weight=0.3, popularity_weight=0.2):
        self.content_model = ContentBasedRecommender()
        self.knn_model = KNNRecommender()
        self.content_weight = content_weight
        self.collab_weight = collab_weight
        self.popularity_weight = popularity_weight
        self.books_df = None
        
    def fit(self, books_df, user_ratings=None):
        """Train all sub-models"""
        self.books_df = books_df
        
        # Train content-based
        self.content_model.fit(books_df)
        
        # Train KNN
        self.knn_model.fit(books_df)
        
        print("✓ Hybrid model trained successfully")
        
    def recommend(self, user_ratings, n_recommendations=6):
        """Generate hybrid recommendations"""
        if not user_ratings:
            return self._get_popular_books(n_recommendations)
        
        # Get liked books
        liked_books = [book_id for book_id, rating in user_ratings.items() if rating >= 4]
        
        if not liked_books:
            return self._get_popular_books(n_recommendations)
        
        # Get recommendations from content-based
        content_recs = self.content_model.recommend(liked_books, n_recommendations * 2)
        
        # Get recommendations from KNN
        knn_recs = []
        for book_id in liked_books[:3]:  # Use top 3 liked books
            knn_recs.extend(self.knn_model.recommend(book_id, n_recommendations))
        
        # Combine and score
        all_recs = {}
        
        # Score content-based recommendations
        for i, rec in enumerate(content_recs):
            book_id = rec['book_id']
            score = (len(content_recs) - i) * self.content_weight
            all_recs[book_id] = all_recs.get(book_id, 0) + score
        
        # Score KNN recommendations
        for i, rec in enumerate(knn_recs):
            book_id = rec['book_id']
            score = (len(knn_recs) - i) * self.collab_weight
            all_recs[book_id] = all_recs.get(book_id, 0) + score
        
        # Add popularity score
        for book_id, score in all_recs.items():
            book = self.books_df[self.books_df['book_id'] == book_id]
            if not book.empty:
                popularity_score = book.iloc[0]['rating'] * self.popularity_weight
                all_recs[book_id] += popularity_score
        
        # Sort and return top N
        sorted_recs = sorted(all_recs.items(), key=lambda x: x[1], reverse=True)
        top_book_ids = [book_id for book_id, _ in sorted_recs[:n_recommendations]]
        
        result = self.books_df[self.books_df['book_id'].isin(top_book_ids)]
        return result.to_dict('records')
    
    def _get_popular_books(self, n=6):
        """Fallback to popular books"""
        return self.books_df.nlargest(n, 'rating').to_dict('records')
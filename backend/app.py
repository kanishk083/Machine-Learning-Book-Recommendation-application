import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample tech books dataset
tech_books_data = {
    'book_id': range(1, 26),
    'title': [
        "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
        "Deep Learning", "Python Machine Learning", 
        "Reinforcement Learning: An Introduction",
        "Pattern Recognition and Machine Learning",
        "Deep Learning with Python", "The Hundred-Page Machine Learning Book",
        "Python for Data Analysis", "Introduction to Statistical Learning",
        "Natural Language Processing with Python",
        "Computer Vision: Algorithms and Applications",
        "Designing Machine Learning Systems", "Grokking Deep Learning",
        "Data Science from Scratch", "Algorithms",
        "Deep Reinforcement Learning Hands-On", "Fluent Python",
        "Speech and Language Processing", "Machine Learning Engineering",
        "Probabilistic Machine Learning: An Introduction",
        "Deep Learning for Computer Vision", "Python Data Science Handbook",
        "Introduction to Algorithms", "Effective Python",
        "Neural Networks and Deep Learning"
    ],
    'author': [
        "Aurélien Géron", "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "Sebastian Raschka", "Richard S. Sutton, Andrew G. Barto",
        "Christopher M. Bishop", "François Chollet", "Andriy Burkov",
        "Wes McKinney", "Gareth James, Daniela Witten", "Steven Bird, Ewan Klein",
        "Richard Szeliski", "Chip Huyen", "Andrew Trask", "Joel Grus",
        "Robert Sedgewick, Kevin Wayne", "Maxim Lapan", "Luciano Ramalho",
        "Dan Jurafsky, James H. Martin", "Andriy Burkov", "Kevin Murphy",
        "Rajalingappaa Shanmugamani", "Jake VanderPlas", "Thomas H. Cormen",
        "Brett Slatkin", "Michael Nielsen"
    ],
    'category': [
        "Machine Learning", "Deep Learning", "Machine Learning", 
        "Reinforcement Learning", "Machine Learning", "Deep Learning",
        "Machine Learning", "Data Science", "Machine Learning", "NLP",
        "Computer Vision", "MLOps", "Deep Learning", "Data Science", "Algorithms",
        "Reinforcement Learning", "Python", "NLP", "MLOps", "Machine Learning",
        "Computer Vision", "Data Science", "Algorithms", "Python", "Deep Learning"
    ],
    'level': [
        "Intermediate", "Advanced", "Intermediate", "Advanced", "Advanced",
        "Beginner", "Beginner", "Beginner", "Intermediate", "Intermediate",
        "Advanced", "Intermediate", "Beginner", "Beginner", "Intermediate",
        "Intermediate", "Intermediate", "Advanced", "Intermediate", "Advanced",
        "Intermediate", "Intermediate", "Advanced", "Intermediate", "Beginner"
    ],
    'rating': [4.6, 4.5, 4.4, 4.7, 4.6, 4.5, 4.3, 4.4, 4.6, 4.2, 4.5, 4.7, 
               4.4, 4.3, 4.5, 4.4, 4.7, 4.6, 4.5, 4.6, 4.3, 4.5, 4.5, 4.5, 4.7],
    'year': [2022, 2016, 2019, 2018, 2006, 2021, 2019, 2022, 2021, 2009, 
             2022, 2022, 2019, 2019, 2011, 2020, 2022, 2023, 2020, 2022, 
             2018, 2016, 2009, 2019, 2015]
}

df_books = pd.DataFrame(tech_books_data)

# Creating a content features for similarity
df_books['content'] = df_books['title'] + ' ' + df_books['category'] + ' ' + df_books['level']

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_books['content'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


class BookRecommender:
    def __init__(self, books_df, similarity_matrix):
        self.books_df = books_df
        self.similarity_matrix = similarity_matrix
    
    def content_based_recommendations(self, book_ids, n_recommendations=6):
        """Generate recommendations based on book similarity"""
        if not book_ids:
            return []
        
        # Get indices of input books
        indices = [self.books_df[self.books_df['book_id'] == bid].index[0] 
                   for bid in book_ids if bid in self.books_df['book_id'].values]
        
        if not indices:
            return []
        
        # Calculate average similarity scores
        sim_scores = np.mean([self.similarity_matrix[idx] for idx in indices], axis=0)
        sim_scores = list(enumerate(sim_scores))
        
        # Sort by similarity (excluding input books)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] not in indices]
        
        # Get top N
        top_indices = [i[0] for i in sim_scores[:n_recommendations]]
        
        return self.books_df.iloc[top_indices].to_dict('records')
    
    def collaborative_filtering_recommendations(self, user_ratings, n_recommendations=6):
        """Generate recommendations based on user ratings"""
        if not user_ratings:
            return []
        
        # Get highly rated books (4+)
        liked_books = [book_id for book_id, rating in user_ratings.items() if rating >= 4]
        
        if not liked_books:
            return []
        
        # Get categories and levels from liked books
        liked_df = self.books_df[self.books_df['book_id'].isin(liked_books)]
        preferred_categories = liked_df['category'].value_counts().index.tolist()
        preferred_levels = liked_df['level'].value_counts().index.tolist()
        
        # Score unrated books
        rated_book_ids = list(user_ratings.keys())
        unrated_books = self.books_df[~self.books_df['book_id'].isin(rated_book_ids)].copy()
        
        # Calculate score
        def calculate_score(row):
            score = 0
            # Category match (highest weight)
            if row['category'] in preferred_categories:
                score += 50 * (1 / (preferred_categories.index(row['category']) + 1))
            
            # Level match
            if row['level'] in preferred_levels:
                score += 20
            
            # Book rating
            score += row['rating'] * 10
            
            # Recency bonus
            if row['year'] >= 2020:
                score += 5
            
            return score
        
        unrated_books['score'] = unrated_books.apply(calculate_score, axis=1)
        unrated_books = unrated_books.sort_values('score', ascending=False)
        
        return unrated_books.head(n_recommendations).to_dict('records')
    
    def hybrid_recommendations(self, user_ratings, n_recommendations=6):
        """Combine content-based and collaborative filtering"""
        if not user_ratings:
            return self.get_popular_books(n_recommendations)
        
        # Get recommendations from both methods
        liked_books = [book_id for book_id, rating in user_ratings.items() if rating >= 4]
        
        content_recs = self.content_based_recommendations(liked_books, n_recommendations * 2)
        collab_recs = self.collaborative_filtering_recommendations(user_ratings, n_recommendations * 2)
        
        # Merge and deduplicate
        all_recs = {book['book_id']: book for book in content_recs + collab_recs}
        
        # Sort by rating and return top N
        sorted_recs = sorted(all_recs.values(), 
                            key=lambda x: x['rating'], 
                            reverse=True)
        
        return sorted_recs[:n_recommendations]
    
    def get_popular_books(self, n=6):
        """Get popular books as fallback"""
        return self.books_df.nlargest(n, 'rating').to_dict('records')


# Initialize recommender
recommender = BookRecommender(df_books, cosine_sim)


@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with optional filtering"""
    category = request.args.get('category', 'All')
    search = request.args.get('search', '').lower()
    
    filtered_df = df_books.copy()
    
    if category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category]
    
    if search:
        filtered_df = filtered_df[
            filtered_df['title'].str.lower().str.contains(search) |
            filtered_df['author'].str.lower().str.contains(search)
        ]
    
    return jsonify(filtered_df.to_dict('records'))


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Get personalized recommendations"""
    data = request.json
    user_ratings = data.get('ratings', {})
    method = data.get('method', 'hybrid')  # 'content', 'collaborative', 'hybrid'
    n_recommendations = data.get('n', 6)
    
    # Convert string keys to integers
    user_ratings = {int(k): v for k, v in user_ratings.items()}
    
    if method == 'content':
        liked_books = [book_id for book_id, rating in user_ratings.items() if rating >= 4]
        recommendations = recommender.content_based_recommendations(liked_books, n_recommendations)
    elif method == 'collaborative':
        recommendations = recommender.collaborative_filtering_recommendations(user_ratings, n_recommendations)
    else:  # hybrid
        recommendations = recommender.hybrid_recommendations(user_ratings, n_recommendations)
    
    return jsonify(recommendations)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    categories = ['All'] + sorted(df_books['category'].unique().tolist())
    return jsonify(categories)


@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    """Get details of a specific book"""
    book = df_books[df_books['book_id'] == book_id]
    if book.empty:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_dict('records')[0])


@app.route('/api/similar/<int:book_id>', methods=['GET'])
def get_similar_books(book_id):
    """Get similar books to a given book"""
    n = request.args.get('n', 5, type=int)
    recommendations = recommender.content_based_recommendations([book_id], n)
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
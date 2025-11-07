# tests/test_models.py
"""
Model Testing Suite for Tech Book Recommender
Run with: python test_models.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data for testing
test_books_data = {
    'book_id': range(1, 11),
    'title': [
        "Machine Learning Basics",
        "Deep Learning Advanced",
        "Python for Data Science",
        "Reinforcement Learning Guide",
        "Neural Networks Explained",
        "Data Science Handbook",
        "Computer Vision Basics",
        "NLP with Python",
        "Advanced Algorithms",
        "Machine Learning Fundamentals"
    ],
    'author': [
        "John Doe", "Jane Smith", "Bob Johnson", 
        "Alice Williams", "Charlie Brown", "David Lee",
        "Emma Davis", "Frank Miller", "Grace Taylor", "Henry Wilson"
    ],
    'category': [
        "Machine Learning", "Deep Learning", "Data Science",
        "Reinforcement Learning", "Deep Learning", "Data Science",
        "Computer Vision", "NLP", "Algorithms", "Machine Learning"
    ],
    'level': [
        "Beginner", "Advanced", "Beginner", "Advanced", "Intermediate",
        "Intermediate", "Beginner", "Intermediate", "Advanced", "Beginner"
    ],
    'rating': [4.5, 4.7, 4.4, 4.6, 4.5, 4.3, 4.4, 4.5, 4.6, 4.4],
    'year': [2022, 2021, 2023, 2020, 2022, 2021, 2022, 2023, 2020, 2022]
}

df = pd.DataFrame(test_books_data)


def test_data_loading():
    """Test if data loads correctly"""
    print("\n" + "="*60)
    print("TEST: Data Loading")
    print("="*60)
    
    try:
        assert len(df) == 10, f"Expected 10 books, got {len(df)}"
        assert 'book_id' in df.columns, "Missing book_id column"
        assert 'title' in df.columns, "Missing title column"
        assert 'category' in df.columns, "Missing category column"
        
        print(f"✓ Loaded {len(df)} books")
        print(f"✓ Columns: {', '.join(df.columns)}")
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_content_based_model():
    """Test content-based recommendation model"""
    print("\n" + "="*60)
    print("TEST: Content-Based Model")
    print("="*60)
    
    try:
        # Create content features
        df['content'] = df['title'] + ' ' + df['category'] + ' ' + df['level']
        
        # TF-IDF vectorization
        tfidf = TfidfVectorizer(stop_words='english', max_features=50)
        tfidf_matrix = tfidf.fit_transform(df['content'])
        
        assert tfidf_matrix.shape[0] == len(df), "TF-IDF matrix size mismatch"
        
        # Cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        assert cosine_sim.shape == (len(df), len(df)), "Similarity matrix size mismatch"
        
        # Test recommendation
        book_idx = 0
        sim_scores = list(enumerate(cosine_sim[book_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:4]  # Get top 3 similar books
        
        assert len(sim_scores) == 3, "Should return 3 recommendations"
        
        print(f"✓ TF-IDF matrix shape: {tfidf_matrix.shape}")
        print(f"✓ Cosine similarity matrix shape: {cosine_sim.shape}")
        print(f"✓ Generated recommendations for book 0")
        
        # Show recommendations
        rec_indices = [i[0] for i in sim_scores]
        recommendations = df.iloc[rec_indices][['title', 'category']]
        print("\nRecommendations:")
        for idx, row in recommendations.iterrows():
            print(f"  - {row['title']} ({row['category']})")
        
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_rating_filter():
    """Test filtering by user ratings"""
    print("\n" + "="*60)
    print("TEST: Rating Filter")
    print("="*60)
    
    try:
        # Simulate user ratings
        user_ratings = {1: 5, 2: 4, 3: 3}
        
        # Get highly rated books (4+)
        liked_books = [book_id for book_id, rating in user_ratings.items() if rating >= 4]
        
        assert len(liked_books) == 2, f"Expected 2 liked books, got {len(liked_books)}"
        assert 1 in liked_books, "Book 1 should be in liked books"
        assert 2 in liked_books, "Book 2 should be in liked books"
        assert 3 not in liked_books, "Book 3 should not be in liked books"
        
        print(f"✓ User ratings: {user_ratings}")
        print(f"✓ Liked books (rating >= 4): {liked_books}")
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_category_matching():
    """Test category-based recommendations"""
    print("\n" + "="*60)
    print("TEST: Category Matching")
    print("="*60)
    
    try:
        # Get books in specific category
        category = "Machine Learning"
        ml_books = df[df['category'] == category]
        
        assert len(ml_books) > 0, f"No books found in category: {category}"
        
        # Verify all books are in correct category
        for _, book in ml_books.iterrows():
            assert book['category'] == category, f"Wrong category: {book['category']}"
        
        print(f"✓ Found {len(ml_books)} books in '{category}' category")
        print(f"✓ Books: {', '.join(ml_books['title'].tolist())}")
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_level_filtering():
    """Test filtering by difficulty level"""
    print("\n" + "="*60)
    print("TEST: Level Filtering")
    print("="*60)
    
    try:
        levels = ['Beginner', 'Intermediate', 'Advanced']
        
        for level in levels:
            level_books = df[df['level'] == level]
            assert len(level_books) > 0, f"No books found for level: {level}"
            print(f"✓ {level}: {len(level_books)} books")
        
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_rating_range():
    """Test that ratings are in valid range"""
    print("\n" + "="*60)
    print("TEST: Rating Range")
    print("="*60)
    
    try:
        min_rating = df['rating'].min()
        max_rating = df['rating'].max()
        
        assert min_rating >= 0, f"Minimum rating below 0: {min_rating}"
        assert max_rating <= 5, f"Maximum rating above 5: {max_rating}"
        assert min_rating <= max_rating, "Min rating greater than max rating"
        
        print(f"✓ Rating range: {min_rating} - {max_rating}")
        print(f"✓ Average rating: {df['rating'].mean():.2f}")
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_recommendation_scoring():
    """Test recommendation scoring algorithm"""
    print("\n" + "="*60)
    print("TEST: Recommendation Scoring")
    print("="*60)
    
    try:
        # Simulate user preferences
        preferred_categories = ["Machine Learning", "Deep Learning"]
        preferred_levels = ["Beginner", "Intermediate"]
        
        # Score books
        scores = []
        for _, book in df.iterrows():
            score = 0
            
            # Category match
            if book['category'] in preferred_categories:
                score += 50
            
            # Level match
            if book['level'] in preferred_levels:
                score += 20
            
            # Rating score
            score += book['rating'] * 10
            
            scores.append(score)
        
        df['score'] = scores
        
        # Get top recommendations
        top_books = df.nlargest(3, 'score')
        
        assert len(top_books) == 3, "Should return 3 recommendations"
        assert top_books['score'].is_monotonic_decreasing, "Scores should be in descending order"
        
        print("✓ Scoring algorithm applied")
        print("\nTop 3 Recommendations:")
        for _, book in top_books.iterrows():
            print(f"  - {book['title']} (Score: {book['score']:.1f})")
        
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_recommendation_excludes_rated_books():
    """Test that recommendations exclude already rated books"""
    print("\n" + "="*60)
    print("TEST: Exclude Rated Books")
    print("="*60)
    
    try:
        # User has rated these books
        rated_book_ids = [1, 2, 3]
        
        # Get unrated books
        unrated_books = df[~df['book_id'].isin(rated_book_ids)]
        
        expected_count = len(df) - len(rated_book_ids)
        assert len(unrated_books) == expected_count, f"Expected {expected_count} unrated books, got {len(unrated_books)}"
        
        # Verify no rated books in results
        for _, book in unrated_books.iterrows():
            assert book['book_id'] not in rated_book_ids, f"Rated book {book['book_id']} found in results"
        
        print(f"✓ Total books: {len(df)}")
        print(f"✓ Rated books: {len(rated_book_ids)}")
        print(f"✓ Unrated books: {len(unrated_books)}")
        print("✓ TEST PASSED")
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_empty_recommendations():
    """Test behavior with no matching recommendations"""
    print("\n" + "="*60)
    print("TEST: Empty Recommendations Fallback")
    print("="*60)
    
    try:
        # Simulate no user ratings
        user_ratings = {}
        
        # Should return popular books as fallback
        popular_books = df.nlargest(5, 'rating')
        
        assert len(popular_books) == 5, "Should return 5 popular books"
        assert popular_books['rating'].is_monotonic_decreasing, "Should be sorted by rating"
        
        print("✓ No user ratings provided")
        print("✓ Returning popular books as fallback:")
        for _, book in popular_books.iterrows():
            print(f"  - {book['title']} ({book['rating']})")
        
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_year_normalization():
    """Test year normalization"""
    print("\n" + "="*60)
    print("TEST: Year Normalization")
    print("="*60)
    
    try:
        min_year = df['year'].min()
        max_year = df['year'].max()
        
        df['year_normalized'] = (df['year'] - min_year) / (max_year - min_year)
        
        assert df['year_normalized'].min() >= 0, "Normalized year below 0"
        assert df['year_normalized'].max() <= 1, "Normalized year above 1"
        
        print(f"✓ Year range: {min_year} - {max_year}")
        print(f"✓ Normalized range: {df['year_normalized'].min():.2f} - {df['year_normalized'].max():.2f}")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def run_all_tests():
    """Run all model tests"""
    print("\n" + "="*60)
    print("TECH BOOK RECOMMENDER - MODEL TEST SUITE")
    print("="*60)
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Content-Based Model", test_content_based_model),
        ("Rating Filter", test_rating_filter),
        ("Category Matching", test_category_matching),
        ("Level Filtering", test_level_filtering),
        ("Rating Range", test_rating_range),
        ("Recommendation Scoring", test_recommendation_scoring),
        ("Exclude Rated Books", test_recommendation_excludes_rated_books),
        ("Empty Recommendations", test_empty_recommendations),
        ("Year Normalization", test_year_normalization),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} CRASHED: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
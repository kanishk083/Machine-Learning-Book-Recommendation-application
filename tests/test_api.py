# tests/test_api.py
"""
API Testing Suite for Tech Book Recommender
Run with: python test_api.py
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000/api'

def test_get_books():
    """Test GET /api/books endpoint"""
    print("\n" + "="*60)
    print("TEST: GET /api/books")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/books')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Books list should not be empty"
        
        # Check first book structure
        first_book = data[0]
        required_fields = ['book_id', 'title', 'author', 'category', 'level', 'rating', 'year']
        for field in required_fields:
            assert field in first_book, f"Missing field: {field}"
        
        print(f"✓ Received {len(data)} books")
        print(f"✓ First book: {first_book['title']}")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_books_with_category():
    """Test GET /api/books with category filter"""
    print("\n" + "="*60)
    print("TEST: GET /api/books?category=Machine Learning")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/books', params={'category': 'Machine Learning'})
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # Verify all books are Machine Learning
        for book in data:
            assert book['category'] == 'Machine Learning', f"Wrong category: {book['category']}"
        
        print(f"✓ Received {len(data)} Machine Learning books")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_books_with_search():
    """Test GET /api/books with search query"""
    print("\n" + "="*60)
    print("TEST: GET /api/books?search=python")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/books', params={'search': 'python'})
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # Verify search works
        for book in data:
            title_match = 'python' in book['title'].lower()
            author_match = 'python' in book['author'].lower()
            assert title_match or author_match, f"Search term not found in: {book['title']}"
        
        print(f"✓ Received {len(data)} books matching 'python'")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_categories():
    """Test GET /api/categories endpoint"""
    print("\n" + "="*60)
    print("TEST: GET /api/categories")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/categories')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert 'All' in data, "'All' should be in categories"
        
        print(f"✓ Received {len(data)} categories")
        print(f"✓ Categories: {', '.join(data)}")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_book_by_id():
    """Test GET /api/book/:id endpoint"""
    print("\n" + "="*60)
    print("TEST: GET /api/book/1")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/book/1')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "Response should be a dictionary"
        assert data['book_id'] == 1, "Wrong book ID"
        
        print(f"✓ Received book: {data['title']}")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_book_not_found():
    """Test GET /api/book/:id with invalid ID"""
    print("\n" + "="*60)
    print("TEST: GET /api/book/9999 (should fail)")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/book/9999')
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        data = response.json()
        assert 'error' in data, "Error message should be present"
        
        print(f"✓ Correctly returned 404 error")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_post_recommendations():
    """Test POST /api/recommend endpoint"""
    print("\n" + "="*60)
    print("TEST: POST /api/recommend")
    print("="*60)
    
    try:
        payload = {
            'ratings': {'1': 5, '3': 4, '6': 5},
            'method': 'hybrid',
            'n': 5
        }
        
        response = requests.post(
            f'{BASE_URL}/recommend',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) <= 5, f"Expected max 5 recommendations, got {len(data)}"
        
        # Verify recommendations don't include rated books
        rated_ids = [1, 3, 6]
        for rec in data:
            assert rec['book_id'] not in rated_ids, f"Recommendation includes rated book: {rec['book_id']}"
        
        print(f"✓ Received {len(data)} recommendations")
        for i, rec in enumerate(data, 1):
            print(f"  {i}. {rec['title']} (Rating: {rec['rating']})")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_post_recommendations_empty_ratings():
    """Test POST /api/recommend with empty ratings"""
    print("\n" + "="*60)
    print("TEST: POST /api/recommend (empty ratings)")
    print("="*60)
    
    try:
        payload = {
            'ratings': {},
            'method': 'hybrid',
            'n': 5
        }
        
        response = requests.post(
            f'{BASE_URL}/recommend',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        print(f"✓ Received {len(data)} popular books as fallback")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_get_similar_books():
    """Test GET /api/similar/:id endpoint"""
    print("\n" + "="*60)
    print("TEST: GET /api/similar/1")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/similar/1', params={'n': 3})
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) <= 3, f"Expected max 3 similar books, got {len(data)}"
        
        print(f"✓ Received {len(data)} similar books")
        for book in data:
            print(f"  - {book['title']}")
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def test_different_recommendation_methods():
    """Test different recommendation methods"""
    print("\n" + "="*60)
    print("TEST: Different Recommendation Methods")
    print("="*60)
    
    methods = ['content', 'collaborative', 'hybrid']
    ratings = {'1': 5, '3': 4}
    
    try:
        for method in methods:
            payload = {
                'ratings': ratings,
                'method': method,
                'n': 3
            }
            
            response = requests.post(
                f'{BASE_URL}/recommend',
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            assert response.status_code == 200, f"Method {method} failed with {response.status_code}"
            data = response.json()
            print(f"  ✓ {method.capitalize()}: {len(data)} recommendations")
        
        print("✓ TEST PASSED")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        return False


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("TECH BOOK RECOMMENDER - API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    
    tests = [
        ("Get all books", test_get_books),
        ("Filter by category", test_get_books_with_category),
        ("Search books", test_get_books_with_search),
        ("Get categories", test_get_categories),
        ("Get book by ID", test_get_book_by_id),
        ("Get invalid book (404)", test_get_book_not_found),
        ("Get recommendations", test_post_recommendations),
        ("Get recommendations (empty)", test_post_recommendations_empty_ratings),
        ("Get similar books", test_get_similar_books),
        ("Different methods", test_different_recommendation_methods),
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
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API server")
        print("Make sure the Flask server is running on http://localhost:5000")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
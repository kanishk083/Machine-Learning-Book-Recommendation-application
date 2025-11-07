# Backend Installation Fix

## Problem
The original `requirements.txt` had very old package versions (pandas 1.3.3, numpy 1.21.2) that are incompatible with Python 3.13.

## Solution
I've updated `requirements.txt` with compatible versions. 

## Installation Steps

1. **Stop the current Flask server** (if running):
   - Press `Ctrl+C` in the terminal where Flask is running

2. **Install the updated dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **If you still get errors, try installing packages individually**:
   ```powershell
   pip install flask flask-cors pandas numpy scikit-learn
   ```

4. **Start the server again**:
   ```powershell
   python app.py
   ```

## Verify Backend is Working

Test these URLs in your browser:
- http://localhost:5000/api/books
- http://localhost:5000/api/categories

You should see JSON data, not 404 errors.

## Note About 404 Errors

The 404 errors you saw when accessing `http://127.0.0.1:5000/` are **normal** - that's not an API endpoint. The API endpoints are:
- `/api/books` - Get all books
- `/api/categories` - Get categories
- `/api/recommend` - Get recommendations (POST)
- `/api/book/<id>` - Get specific book
- `/api/similar/<id>` - Get similar books


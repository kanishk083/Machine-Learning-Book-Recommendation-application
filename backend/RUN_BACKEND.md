# Backend Setup and Run Instructions

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Step 1: Install Dependencies

Open PowerShell or Command Prompt in the backend directory and run:

```powershell
pip install -r requirements.txt
```

**Note:** If you have multiple Python versions, you might need to use:
- `pip3 install -r requirements.txt` (Linux/Mac)
- `python -m pip install -r requirements.txt` (Windows)

## Step 2: Run the Backend Server

### Option A: Run directly with Python (Recommended)
```powershell
python app.py
```

### Option B: Run with Flask CLI
```powershell
flask run --port 5000
```

### Option C: Run with Python module
```powershell
python -m flask run --port 5000
```

## Expected Output

When the server starts successfully, you should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
 * Debug mode: on
```

## Verify Backend is Running

Open your browser and visit:
- http://localhost:5000/api/books
- http://localhost:5000/api/categories

You should see JSON data returned.

## Troubleshooting

### Issue: Module not found errors
**Solution:** Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Either:
1. Stop the other application using port 5000, OR
2. Change the port in `app.py` (line 248) to a different port (e.g., 5001)

### Issue: Flask not found
**Solution:** Install Flask:
```powershell
pip install flask flask-cors
```

## Next Steps

Once the backend is running, start the frontend:
1. Open a new terminal window
2. Navigate to the `frontend` directory
3. Run: `npm install` (first time only)
4. Run: `npm run dev`

The frontend will be available at http://localhost:5173


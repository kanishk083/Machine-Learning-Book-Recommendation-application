# Frontend Setup - Complete Guide

## ✅ What I've Fixed

1. **Fixed API import path** - Moved `api.jsx` to `src/api.js`
2. **Updated API base URL** - Changed to use Vite proxy (`/api`)
3. **Created PostCSS config** - Added `postcss.config.js` for Tailwind CSS
4. **Fixed filter reload logic** - Books now reload when filters change
5. **Created startup script** - Added `start-frontend.bat` for easy startup

## 🚀 How to Start the Frontend

### Option 1: Using the Batch File (Easiest)
1. Navigate to the `frontend` folder
2. Double-click `start-frontend.bat`
3. Wait for the server to start
4. Open http://localhost:5173 in your browser

### Option 2: Using Command Line
1. Open PowerShell or Command Prompt
2. Navigate to the frontend directory:
   ```powershell
   cd "C:\Users\Dinesh\Downloads\Machine-Learning-Book-Recommendation-application-main\Machine-Learning-Book-Recommendation-application-main\frontend"
   ```
3. Start the server:
   ```powershell
   npm run dev
   ```
4. You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:5173/
   ```
5. Open http://localhost:5173 in your browser

## ✅ Prerequisites Check

Before starting, make sure:
- ✅ **Backend is running** on http://localhost:5000
  - You should see: `Running on http://127.0.0.1:5000`
- ✅ **Dependencies are installed** (`node_modules` folder exists)
  - If not, run: `npm install` in the frontend directory

## 🔍 Troubleshooting

### Issue: "Cannot GET /" or 404 Error
**Solution:** Make sure you're accessing http://localhost:5173 (not 5174 or another port)

### Issue: "Failed to load data" in browser
**Solution:** 
1. Check that backend is running on port 5000
2. Test backend directly: http://localhost:5000/api/books
3. Check browser console (F12) for errors

### Issue: Port 5173 already in use
**Solution:** 
1. Close any other applications using port 5173
2. Or use a different port: `npm run dev -- --port 3000`

### Issue: White screen or nothing loads
**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Make sure all dependencies are installed: `npm install`

### Issue: CORS errors in console
**Solution:** 
- The Vite proxy should handle this automatically
- Make sure `vite.config.js` has the proxy configuration
- Verify backend has `CORS(app)` enabled (it does)

## 📋 Verification Checklist

- [ ] Backend is running on port 5000
- [ ] Frontend dependencies installed (`npm install` completed)
- [ ] Frontend server started (`npm run dev`)
- [ ] Browser opens http://localhost:5173
- [ ] Books are displayed (not error message)
- [ ] Can search and filter books
- [ ] Can rate books
- [ ] Can get recommendations

## 🎯 Expected Behavior

When everything works:
1. You'll see the "Tech Book Recommender" header
2. A list of 25 tech books will be displayed
3. You can search by title/author
4. You can filter by category
5. You can rate books (1-5 stars)
6. Click "Get Recommendations" to see personalized suggestions

## 📞 Still Having Issues?

If the frontend still doesn't work:
1. Check the terminal where `npm run dev` is running for error messages
2. Open browser console (F12) and check for errors
3. Verify backend is accessible: http://localhost:5000/api/books
4. Make sure you're using the correct URL: http://localhost:5173


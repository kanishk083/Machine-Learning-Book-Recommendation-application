# Frontend Setup and Run Instructions

## Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)

## Step 1: Install Dependencies

Open PowerShell or Command Prompt in the frontend directory and run:

```powershell
npm install
```

This will install all required packages including:
- React
- Vite
- Tailwind CSS
- Axios
- Lucide React icons

**Note:** This step only needs to be done once (or when dependencies change).

## Step 2: Start the Development Server

```powershell
npm run dev
```

## Expected Output

When the server starts successfully, you should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Access the Application

Open your browser and visit:
- **http://localhost:5173**

## Important Notes

1. **Backend must be running**: Make sure the backend server is running on port 5000 before using the frontend
   - The frontend will try to connect to `http://localhost:5000/api`
   - If the backend is not running, you'll see errors in the browser console

2. **Hot Module Replacement**: The development server supports hot reloading
   - Changes to your code will automatically refresh in the browser
   - No need to manually refresh the page

3. **Port 5173**: If port 5173 is already in use, Vite will automatically use the next available port

## Other Available Commands

### Build for Production
```powershell
npm run build
```
This creates an optimized production build in the `dist` folder.

### Preview Production Build
```powershell
npm run preview
```
This serves the production build locally for testing.

## Troubleshooting

### Issue: npm command not found
**Solution:** Install Node.js from https://nodejs.org/

### Issue: Port 5173 already in use
**Solution:** Vite will automatically use the next available port, or you can specify a port:
```powershell
npm run dev -- --port 3000
```

### Issue: Module not found errors
**Solution:** Make sure dependencies are installed:
```powershell
npm install
```

### Issue: Tailwind CSS not working
**Solution:** Make sure `postcss.config.js` exists in the frontend directory. If not, create it with:
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Issue: Cannot connect to backend
**Solution:** 
1. Make sure the backend is running on port 5000
2. Check the browser console for CORS errors
3. Verify the API URL in `src/api.js` is set to `/api` (uses Vite proxy)

## Quick Start Summary

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Then open http://localhost:5173 in your browser!


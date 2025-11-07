# Tech Book Recommender

A web application that provides personalized technology book recommendations using various recommendation algorithms.

## Features

- Content-based filtering
- Collaborative filtering
- K-Nearest Neighbors recommendations
- Hybrid recommendations combining multiple approaches
- React-based frontend with a modern UI
- Flask-based RESTful API backend

## Project Structure

```
tech-book-recommender/
├── backend/                   # Flask API server
│   ├── app.py                # Main Flask application
│   ├── models/               # Recommendation models
│   ├── data/                 # Dataset files
│   ├── utils/               # Utility functions
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React frontend
│   ├── src/                 # Source code
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
└── docker-compose.yml       # Docker compose configuration
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   ```

3. Start the development servers:
   ```bash
   # Backend
   cd backend
   flask run

   # Frontend
   cd frontend
   npm run dev
   ```

Or using Docker:
```bash
docker-compose up
```

## API Endpoints

- `/api/recommendations/content-based` - Get content-based recommendations
- `/api/recommendations/collaborative` - Get collaborative filtering recommendations
- `/api/recommendations/knn` - Get K-Nearest Neighbors recommendations
- `/api/recommendations/hybrid` - Get hybrid recommendations

## Technologies Used

- Backend:
  - Flask
  - pandas
  - scikit-learn
  - Surprise
  
- Frontend:
  - React
  - Vite
  - TailwindCSS
  - Axios

## License

MIT
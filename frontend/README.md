# Coin Collection Inventory Tracker - Frontend

React frontend application for managing and tracking coin collections. Built with React, Vite, and React Router, connecting to a Django REST API backend.

## Features

- View coin collection inventory
- Add new coins to the collection
- View collection statistics
- Responsive navigation and routing

## Tech Stack

- **React 19** - UI library
- **Vite** - Build tool and dev server
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API requests
- **ESLint** - Code linting

## Prerequisites

- Node.js (v16 or higher recommended)
- npm or yarn package manager
- Backend API running (see backend README for setup)

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the next available port).

The frontend is configured to connect to the Django backend API at `http://localhost:8000/api`. Make sure your backend server is running before using the frontend.

## Available Scripts

- `npm run dev` - Start development server with hot module replacement
- `npm run build` - Build the app for production (outputs to `dist/`)
- `npm run preview` - Preview the production build locally
- `npm run lint` - Run ESLint to check code quality

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable React components
│   │   └── Navigation.jsx
│   ├── pages/          # Page components (routes)
│   │   ├── Home.jsx
│   │   ├── CoinsList.jsx
│   │   └── AddCoin.jsx
│   ├── services/        # API service layer
│   │   └── api.js       # Axios instance and API functions
│   ├── assets/          # Static assets (images, etc.)
│   ├── App.jsx          # Main app component with routing
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Public static files
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
└── eslint.config.js     # ESLint configuration
```

## API Configuration

The API base URL is configured in `src/services/api.js`. By default, it points to:

```
http://localhost:8000/api
```

To change the API endpoint, modify the `API_BASE_URL` constant in `src/services/api.js`.

## Routes

- `/` - Home page
- `/coins` - View all coins in the collection
- `/coins/add` - Add a new coin to the collection

## Building for Production

To create a production build:

```bash
npm run build
```

The optimized files will be output to the `dist/` directory, ready to be deployed to any static hosting service.

## Development Notes

- The app uses React Router for client-side navigation
- API calls are handled through the `api.js` service layer
- The frontend automatically handles paginated API responses when fetching all coins
- Make sure CORS is properly configured on the backend to allow requests from the frontend origin

## Troubleshooting

**API connection errors:**
- Ensure the Django backend is running on `http://localhost:8000`
- Check that CORS headers are properly configured in the backend
- Verify the API base URL in `src/services/api.js` matches your backend URL

**Port conflicts:**
- If port 5173 is in use, Vite will automatically use the next available port
- Check the terminal output for the actual port number

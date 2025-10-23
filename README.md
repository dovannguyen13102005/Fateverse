# FateVerse 🔮

A modern fortune telling web application with Numerology, Zodiac, Love Matching, Tarot Reading and Daily Fortune features, integrated with Google OAuth for authentication.

## 🌟 Features

- 🔢 **Numerology**: Calculate life path number, expression number, soul urge, and personality numbers
- ♉ **Zodiac**: Get detailed zodiac sign analysis and compatibility
- 💘 **Love Match**: Check love compatibility between two people based on numerology and zodiac
- 🔮 **Tarot**: Digital tarot card reading with past, present, and future insights
- 🌟 **Daily Fortune**: Get your daily fortune, lucky colors, and motivational quotes
- 🔐 **Google OAuth**: Secure authentication with Google Sign-In
- 📜 **History**: Track all your fortune telling history
- ⚙️ **Settings**: Customize your profile and theme preferences

## 🏗️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **TailwindCSS** for styling
- **Framer Motion** for animations
- **Axios** for API calls
- **Google OAuth** for authentication

### Backend
- **FastAPI** (Python) for REST API
- **MongoDB** with Motor (async driver)
- **JWT** for token-based authentication
- **Google OAuth 2.0** for social login
- **Python-Jose** for JWT handling

### DevOps
- **Docker & Docker Compose** for containerization
- **Nginx** for serving frontend static files
- **MongoDB 6.0** for database

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Google OAuth 2.0 credentials (see setup below)

> **📦 For VPS/Production Deployment**: See detailed guide in [VPS Deployment Guide](docs/VPS_Deployment_Guide.md)

### 1. Clone the repository
```bash
git clone <repository-url>
cd boi_toan
```

### 2. Setup Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized JavaScript origins:
   - `http://localhost`
   - `http://localhost:80`
6. Add authorized redirect URIs:
   - `http://localhost`
   - `http://localhost/login`
7. Copy your Client ID

### 3. Configure Environment Variables

Create `.env` file in the root directory:
```env
# JWT Secret
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# MongoDB Password
MONGO_PASSWORD=fateverse123

# Google OAuth (same for both frontend and backend)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

Create `backend/.env`:
```env
MONGODB_URL=mongodb://fateverse:fateverse123@mongodb:27017/fateverse?authSource=admin
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
CORS_ORIGIN=http://localhost:80
```

### 4. Start the application
```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB**: mongodb://localhost:27017

## 🛠️ Development Setup

### Frontend Development

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

4. Start development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:5173

### Backend Development

1. Navigate to backend directory:
```bash
cd backend
```

2. Create Python virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/fateverse
JWT_SECRET=your-super-secret-jwt-key
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
CORS_ORIGIN=http://localhost:5173
```

5. Start development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend API will be available at http://localhost:8000

### MongoDB Setup (for local development)

If running locally without Docker:

```bash
# Install MongoDB 6.0
# Start MongoDB service
mongod --auth

# Create database and user
mongosh
use admin
db.createUser({
  user: "fateverse",
  pwd: "fateverse123",
  roles: [{ role: "readWrite", db: "fateverse" }]
})
```

## 📁 Project Structure

```
boi_toan/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── auth/       # Authentication components
│   │   │   ├── common/     # Common UI components
│   │   │   └── layout/     # Layout components
│   │   ├── contexts/       # React contexts (Auth, etc.)
│   │   ├── pages/          # Page components
│   │   ├── styles/         # Global styles
│   │   ├── utils/          # Utility functions & API client
│   │   ├── App.tsx         # Main app component
│   │   └── main.tsx        # Entry point
│   ├── Dockerfile          # Frontend Docker configuration
│   ├── nginx.conf          # Nginx configuration
│   └── package.json        # Frontend dependencies
│
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── database/       # Database configurations
│   │   ├── models/         # Pydantic models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── Dockerfile          # Backend Docker configuration
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
│
├── docs/                    # Documentation
│   ├── FateVerse_Architecture.md
│   ├── FateVerse_UI_Design.md
│   └── FateVerse_UserStories.md
│
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # This file
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/google` - Google OAuth login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/verify` - Verify JWT token

### Fortune Telling
- `POST /api/numerology/{user_id}` - Calculate numerology
- `POST /api/zodiac/{user_id}` - Get zodiac information
- `POST /api/love/{user_id}` - Calculate love compatibility
- `POST /api/tarot/{user_id}` - Get tarot reading
- `GET /api/fortune/{user_id}` - Get daily fortune

### User Management
- `POST /api/users/register` - Register new user
- `GET /api/users/profile/{user_id}` - Get user profile

## 🧪 Testing

### Frontend
```bash
cd frontend
npm run lint
npm run build  # Test production build
```

### Backend
```bash
cd backend
# Run tests (to be implemented)
pytest
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :80
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:80 | xargs kill
lsof -ti:8000 | xargs kill
```

### Docker Issues
```bash
# Clean up Docker
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

### MongoDB Connection Issues
- Check MongoDB is running
- Verify credentials in .env file
- Check MongoDB logs: `docker-compose logs mongodb`

## � Documentation

- [VPS Deployment Guide](docs/VPS_Deployment_Guide.md) - Complete guide for deploying to VPS with Docker
- [Email/Password Authentication](docs/Email_Password_Authentication.md) - Email authentication feature guide
- [Architecture Overview](docs/FateVerse_Architecture.md) - System architecture documentation
- [UI Design Guide](docs/FateVerse_UI_Design.md) - UI/UX design specifications
- [User Stories](docs/FateVerse_UserStories.md) - Feature requirements and user stories

## �📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Development Team

## 🙏 Acknowledgments

- Google OAuth for authentication
- OpenAI for inspiration
- TailwindCSS for beautiful UI components
- FastAPI for excellent documentation
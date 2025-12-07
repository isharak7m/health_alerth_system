# 🏥 Health Monitoring System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg?style=flat&logo=React&logoColor=white)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg?style=flat&logo=PostgreSQL&logoColor=white)](https://postgresql.org)

A comprehensive, production-ready health monitoring system designed for disease outbreak tracking, vaccination management, and AI-powered health assistance. Built for Smart India Hackathon (SIH) to address critical public health challenges through modern technology.

## 🚀 Key Features

### 🔐 Security & Authentication
- **JWT-based Authentication**: Secure token-based authentication with role-based access control
- **Password Security**: bcrypt hashing with salt for password protection
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Comprehensive data validation using Pydantic

### 📍 Location-based Services
- **Geolocation Integration**: Users get personalized health information based on their location
- **Real-time Notifications**: Instant email alerts for users in affected areas
- **Location Filtering**: Filter outbreaks and vaccinations by state/district

### 🤖 AI Integration
- **Health Assistant**: Ollama-powered chatbot for health queries and medical guidance
- **Natural Language Processing**: LLaMA 3 model for accurate health information
- **Conversation History**: Persistent chat history for better user experience

### 👨‍💼 Admin Management
- **Complete CRUD Operations**: Full management of users, outbreaks, and vaccinations
- **Bulk Data Upload**: CSV import functionality for mass data entry
- **Pagination**: Efficient handling of large datasets
- **Data Analytics**: Comprehensive reporting and statistics

### 📱 User Experience
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Updates**: Live data synchronization across the platform
- **Interactive Dashboard**: Clean, intuitive interface with data visualization
- **Notification System**: Customizable email alerts for health updates

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT Authentication
- Ollama (AI model integration)
- APScheduler (Background tasks)

### Frontend
- React 18
- Tailwind CSS
- React Router
- Axios
- React Query

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Ollama with your fine-tuned model

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
copy .env.example .env
```

Edit `.env` with your configuration:
```
DATABASE_URL=postgresql://username:password@localhost/health_monitoring
SECRET_KEY=your-secret-key-here
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=your-fine-tuned-model:latest
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

5. Create database and run migrations:
```bash
# Create PostgreSQL database named 'health_monitoring'
python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
```

6. Start the backend server:
```bash
python main.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

### Ollama Setup

1. Install Ollama from https://ollama.ai
2. Pull or load your fine-tuned model:
```bash
ollama pull your-fine-tuned-model:latest
```

## Usage

1. **Registration**: Users can register with their location details
2. **Dashboard**: View local health data, outbreaks, and vaccination campaigns
3. **Chat**: Interact with the AI health assistant for personalized advice
4. **Admin Panel**: Admins can manage users and health data
5. **Notifications**: Enable weekly email updates for health information

## API Endpoints

### Authentication
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user info

### Health Data
- `GET /api/health/location-data` - Get location-based health data
- `GET /api/health/outbreaks` - Get outbreak information
- `GET /api/health/vaccinations` - Get vaccination campaigns

### Chat
- `POST /api/chat/message` - Send message to AI assistant
- `GET /api/chat/history` - Get chat history

### Admin (Admin only)
- `GET /api/admin/users` - Get all users
- `DELETE /api/admin/users/{id}` - Delete user
- `POST /api/admin/outbreaks` - Create outbreak
- `PUT /api/admin/outbreaks/{id}` - Update outbreak
- `DELETE /api/admin/outbreaks/{id}` - Delete outbreak
- `POST /api/admin/vaccinations` - Create vaccination
- `PUT /api/admin/vaccinations/{id}` - Update vaccination
- `DELETE /api/admin/vaccinations/{id}` - Delete vaccination

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS protection
- Input validation with Pydantic

## Production Deployment

1. Set strong SECRET_KEY in environment variables
2. Use production database (PostgreSQL)
3. Configure email SMTP settings
4. Set up reverse proxy (nginx)
5. Use HTTPS
6. Configure proper CORS origins

## License

This project is licensed under the MIT License.
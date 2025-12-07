# 🏥 Health Monitoring System - Project Composition

## 📦 What This Project Is Made Of

This is a **3-tier web application** consisting of:
1. **Frontend** (User Interface)
2. **Backend** (Server & Business Logic)
3. **Database** (Data Storage)
4. **AI Service** (Chatbot)

---

## 🎨 FRONTEND (React Application)

### Core Technologies
```
React 18.2.0          → JavaScript UI library
React Router 6.8.1    → Page navigation
Tailwind CSS 3.2.7    → Styling framework
Axios 1.3.4           → HTTP requests to backend
```

### Key Libraries & Their Purpose

**1. React (^18.2.0)**
- Main UI framework
- Component-based architecture
- Virtual DOM for performance
- Hooks for state management

**2. React Router DOM (^6.8.1)**
- Client-side routing
- Navigate between pages without reload
- Protected routes for authentication
```javascript
<Route path="/dashboard" element={<Dashboard />} />
<Route path="/admin" element={<AdminPanel />} />
```

**3. Axios (^1.3.4)**
- HTTP client for API calls
- Interceptors for authentication tokens
- Better error handling than fetch
```javascript
axios.get('/api/health/outbreaks')
axios.post('/api/users/login', credentials)
```

**4. Tailwind CSS (^3.2.7)**
- Utility-first CSS framework
- No custom CSS files needed
- Responsive design built-in
```html
<div className="bg-blue-500 text-white p-4 rounded-lg hover:bg-blue-600">
```

**5. Lucide React (^0.263.1)**
- Icon library (modern, lightweight)
- 1000+ icons
```javascript
import { User, AlertTriangle, Shield } from 'lucide-react';
```

**6. React Hot Toast (^2.4.0)**
- Notification system
- Success/error messages
```javascript
toast.success('Login successful!');
toast.error('Failed to fetch data');
```

**7. React Hook Form (^7.43.5)**
- Form validation
- Better performance than controlled inputs
```javascript
const { register, handleSubmit } = useForm();
```

**8. React Query (^3.39.3)**
- Data fetching & caching
- Automatic refetching
- Loading states management

### Frontend File Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── Login.js           → User login page
│   │   ├── Register.js        → User registration
│   │   ├── Dashboard.js       → Main user dashboard
│   │   ├── AdminPanel.js      → Admin management
│   │   └── Chat.js            → AI chatbot interface
│   ├── contexts/
│   │   └── AuthContext.js     → Global authentication state
│   ├── App.js                 → Main app component & routing
│   └── index.js               → React entry point
├── public/
│   └── index.html             → HTML template
├── package.json               → Dependencies & scripts
└── tailwind.config.js         → Tailwind configuration
```

---

## ⚙️ BACKEND (FastAPI Application)

### Core Technologies
```
FastAPI 0.104.1       → Modern Python web framework
SQLAlchemy 2.0        → Database ORM
PostgreSQL/SQLite     → Database
Pydantic 2.0          → Data validation
```

### Key Libraries & Their Purpose

**1. FastAPI (0.104.1)**
- High-performance web framework
- Automatic API documentation
- Type hints for validation
- Async support
```python
@app.post("/api/users/register")
def register(user: UserCreate):
    return create_user(user)
```

**2. SQLAlchemy (2.0)**
- ORM (Object-Relational Mapping)
- Write Python instead of SQL
- Database agnostic
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

**3. Pydantic (2.0)**
- Data validation using Python types
- Automatic error messages
- JSON serialization
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
```

**4. python-jose (3.3.0)**
- JWT token creation & verification
- Secure authentication
```python
token = jwt.encode({"sub": username}, SECRET_KEY)
```

**5. passlib + bcrypt**
- Password hashing
- Secure password storage
```python
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**6. python-multipart**
- File upload handling
- CSV import functionality
```python
@app.post("/upload-csv")
async def upload(file: UploadFile):
    return process_csv(file)
```

**7. pandas**
- CSV data processing
- Data manipulation
```python
df = pd.read_csv(file)
for row in df.iterrows():
    create_outbreak(row)
```

**8. APScheduler**
- Background task scheduling
- Automated email notifications
```python
scheduler.add_job(send_notifications, 'cron', day_of_week='mon')
```

**9. requests**
- HTTP client for Ollama API
- AI chatbot integration
```python
response = requests.post("http://localhost:11434/api/generate")
```

### Backend File Structure
```
backend/
├── app/
│   ├── routers/
│   │   ├── users.py           → Authentication endpoints
│   │   ├── health_data.py     → Health data APIs
│   │   ├── admin.py           → Admin CRUD operations
│   │   └── chat.py            → AI chatbot endpoints
│   ├── models.py              → Database models (SQLAlchemy)
│   ├── schemas.py             → Data validation (Pydantic)
│   ├── database.py            → Database connection
│   ├── auth.py                → JWT authentication logic
│   ├── chatbot.py             → AI integration
│   └── scheduler.py           → Background tasks
├── main.py                    → FastAPI app entry point
├── requirements.txt           → Python dependencies
└── .env                       → Environment variables
```

---

## 🗄️ DATABASE (PostgreSQL/SQLite)

### Database Tables

**1. Users Table**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR DEFAULT 'user',
    state VARCHAR,
    district VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    notifications BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**2. Outbreaks Table**
```sql
CREATE TABLE outbreaks (
    id SERIAL PRIMARY KEY,
    outbreak_id VARCHAR UNIQUE NOT NULL,
    disease VARCHAR NOT NULL,
    report_date TIMESTAMP,
    country VARCHAR,
    state VARCHAR,
    district VARCHAR,
    cases_reported INTEGER,
    deaths INTEGER,
    severity VARCHAR,
    confirmed BOOLEAN,
    source_url VARCHAR,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**3. Vaccinations Table**
```sql
CREATE TABLE vaccinations (
    id SERIAL PRIMARY KEY,
    campaign_id VARCHAR UNIQUE NOT NULL,
    country VARCHAR,
    state VARCHAR,
    district VARCHAR,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    vaccine_name VARCHAR,
    target_population VARCHAR,
    doses_allocated INTEGER,
    doses_administered INTEGER,
    partner_org VARCHAR,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**4. Chat Messages Table**
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🤖 AI SERVICE (Ollama + LLaMA 3)

### What It Is
- **Ollama**: Local LLM runtime (like Docker for AI models)
- **LLaMA 3**: Meta's large language model
- **Purpose**: Health-related question answering

### How It Works
```
User asks question → Backend sends to Ollama → 
LLaMA 3 processes → Returns health advice → 
Saved to database → Displayed to user
```

### Integration
```python
def chat_with_ollama(message, user_location):
    prompt = f"""You are a health assistant. 
    User location: {user_location}
    Question: {message}
    Provide accurate health information."""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    
    return response.json()["response"]
```

---

## 🔄 How Everything Connects

### Request Flow Example: User Login

```
1. USER ACTION
   ↓
   User enters email/password in Login.js
   
2. FRONTEND
   ↓
   axios.post('/api/users/login', {email, password})
   
3. BACKEND (FastAPI)
   ↓
   Receives request at /api/users/login endpoint
   ↓
   Validates credentials with bcrypt
   ↓
   Generates JWT token
   
4. DATABASE
   ↓
   Queries users table
   ↓
   Returns user data
   
5. RESPONSE
   ↓
   Backend sends JWT token
   ↓
   Frontend stores in localStorage
   ↓
   User redirected to Dashboard
```

### Data Flow Example: Viewing Outbreaks

```
1. USER ACTION
   ↓
   User opens Dashboard
   
2. FRONTEND
   ↓
   useEffect(() => fetchOutbreaks())
   ↓
   axios.get('/api/health/outbreaks', {
       headers: { Authorization: `Bearer ${token}` }
   })
   
3. BACKEND
   ↓
   Verifies JWT token
   ↓
   Gets user location from token
   ↓
   Queries database for local outbreaks
   
4. DATABASE
   ↓
   SELECT * FROM outbreaks 
   WHERE state = user.state 
   AND district = user.district
   
5. RESPONSE
   ↓
   Backend returns JSON data
   ↓
   Frontend displays in UI
```

---

## 📊 Project Statistics

### Lines of Code (Approximate)
```
Frontend:  ~2,500 lines (JavaScript/JSX)
Backend:   ~1,800 lines (Python)
Database:  ~200 lines (SQL schemas)
Config:    ~300 lines (JSON, env files)
Total:     ~4,800 lines
```

### File Count
```
Frontend:  ~15 files
Backend:   ~12 files
Config:    ~8 files
Docs:      ~5 files
Total:     ~40 files
```

### Dependencies
```
Frontend:  14 npm packages
Backend:   18 pip packages
Total:     32 external libraries
```

---

## 🎯 Key Features Breakdown

### User Features (Frontend Heavy)
- ✅ Registration/Login → React forms + Axios
- ✅ Dashboard → React components + Tailwind
- ✅ Health alerts → Real-time data display
- ✅ AI Chat → Chat interface + message history

### Admin Features (Full Stack)
- ✅ User management → CRUD operations
- ✅ Outbreak management → Database operations
- ✅ CSV upload → File processing with pandas
- ✅ Data analytics → SQL queries + visualization

### Backend Services
- ✅ Authentication → JWT tokens
- ✅ Authorization → Role-based access
- ✅ Data validation → Pydantic schemas
- ✅ Email notifications → SMTP integration
- ✅ AI integration → Ollama API calls

---

## 🔐 Security Components

### Authentication Layer
```
JWT Tokens → Secure, stateless authentication
bcrypt → Password hashing (one-way encryption)
CORS → Cross-origin protection
Input Validation → Pydantic prevents injection
```

### Data Protection
```
Environment Variables → Secrets not in code
HTTPS Ready → SSL/TLS support
SQL Injection Prevention → ORM parameterized queries
XSS Protection → React auto-escaping
```

---

## 🚀 Deployment Components

### Development
```
Frontend: npm start (Port 3000)
Backend:  uvicorn main:app --reload (Port 8002)
Database: PostgreSQL (Port 5432)
AI:       Ollama (Port 11434)
```

### Production
```
Frontend: npm run build → Static files
Backend:  Gunicorn/Uvicorn workers
Database: PostgreSQL with connection pooling
Reverse Proxy: Nginx
SSL: Let's Encrypt certificates
```

---

## 📚 Summary

This project is made up of:

1. **React Frontend** - User interface with 14 libraries
2. **FastAPI Backend** - API server with 18 libraries
3. **PostgreSQL Database** - 4 main tables with relationships
4. **Ollama AI** - LLaMA 3 for health assistance
5. **Authentication System** - JWT + bcrypt security
6. **Notification System** - Email alerts with APScheduler
7. **Admin Panel** - Full CRUD operations
8. **File Upload** - CSV processing with pandas

**Total**: ~4,800 lines of code, 32 dependencies, 40 files, 4 services working together to create a production-ready health monitoring platform.

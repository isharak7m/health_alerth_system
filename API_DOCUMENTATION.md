# API Documentation

## Base URL
```
http://localhost:8002/api
```

## Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "John Doe",
  "state": "Delhi",
  "district": "New Delhi",
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

#### Login
```http
POST /users/login
Content-Type: application/json

{
  "username": "username",
  "password": "password123"
}

Response:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /users/me
Authorization: Bearer <token>
```

#### Update User Profile
```http
PUT /users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "Updated Name",
  "notifications": true
}
```

### Health Data

#### Get Location-based Health Data
```http
GET /health/location-data?filter_location=true
Authorization: Bearer <token>
```

#### Get Outbreaks (Paginated)
```http
GET /health/outbreaks?page=1&limit=10&state=Delhi&district=New Delhi
```

#### Get Vaccinations (Paginated)
```http
GET /health/vaccinations?page=1&limit=10&state=Delhi&district=New Delhi
```

#### Get Health Alerts
```http
GET /health/alerts
Authorization: Bearer <token>
```

### Chat System

#### Send Message to AI Assistant
```http
POST /chat/message
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "What is malaria?"
}

Response:
{
  "response": "AI generated response about malaria..."
}
```

#### Get Chat History
```http
GET /chat/history
Authorization: Bearer <token>
```

### Admin Endpoints (Admin Role Required)

#### Get All Users
```http
GET /admin/users
Authorization: Bearer <admin_token>
```

#### Delete User
```http
DELETE /admin/users/{user_id}
Authorization: Bearer <admin_token>
```

#### Create Outbreak
```http
POST /admin/outbreaks
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "outbreak_id": "OUT001",
  "disease": "Dengue",
  "report_date": "2024-01-15T10:00:00",
  "country": "India",
  "state": "Delhi",
  "district": "New Delhi",
  "cases_reported": 45,
  "deaths": 2,
  "severity": "moderate",
  "confirmed": true,
  "source_url": "https://example.com",
  "notes": "Monsoon-related outbreak"
}
```

#### Update Outbreak
```http
PUT /admin/outbreaks/{outbreak_id}
Authorization: Bearer <admin_token>
Content-Type: application/json
```

#### Delete Outbreak
```http
DELETE /admin/outbreaks/{outbreak_id}
Authorization: Bearer <admin_token>
```

#### Upload Outbreaks CSV
```http
POST /admin/outbreaks/upload-csv
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

file: outbreak_data.csv
```

**CSV Format for Outbreaks:**
```csv
outbreak_id,disease,report_date,state,district,cases_reported,deaths,severity,confirmed,country,source_url,notes
OUT001,Malaria,2024-01-15,Delhi,New Delhi,25,1,moderate,true,India,,Monsoon related
```

#### Create Vaccination
```http
POST /admin/vaccinations
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "campaign_id": "VAC001",
  "country": "India",
  "state": "Delhi",
  "district": "New Delhi",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "vaccine_name": "COVID-19 Booster",
  "target_population": "Adults 18+",
  "doses_allocated": 10000,
  "doses_administered": 7500,
  "partner_org": "Delhi Health Department",
  "notes": "Winter campaign"
}
```

#### Update Vaccination
```http
PUT /admin/vaccinations/{vaccination_id}
Authorization: Bearer <admin_token>
Content-Type: application/json
```

#### Delete Vaccination
```http
DELETE /admin/vaccinations/{vaccination_id}
Authorization: Bearer <admin_token>
```

#### Upload Vaccinations CSV
```http
POST /admin/vaccinations/upload-csv
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

file: vaccination_data.csv
```

**CSV Format for Vaccinations:**
```csv
campaign_id,state,district,start_date,end_date,vaccine_name,target_population,doses_allocated,doses_administered,country,partner_org,notes
VAC001,Delhi,New Delhi,2024-01-01,2024-12-31,COVID-19 Booster,Adults 18+,5000,3000,India,Delhi Health Dept,Winter campaign
```

## Response Formats

### Success Response
```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

### Paginated Response
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10
}
```

## Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per authenticated user

## Data Models

### User
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "role": "user",
  "state": "Delhi",
  "district": "New Delhi",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "notifications": true,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Outbreak
```json
{
  "id": 1,
  "outbreak_id": "OUT001",
  "disease": "Dengue",
  "report_date": "2024-01-15T10:00:00Z",
  "country": "India",
  "state": "Delhi",
  "district": "New Delhi",
  "cases_reported": 45,
  "deaths": 2,
  "severity": "moderate",
  "confirmed": true,
  "source_url": "https://example.com",
  "notes": "Monsoon-related outbreak",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Vaccination
```json
{
  "id": 1,
  "campaign_id": "VAC001",
  "country": "India",
  "state": "Delhi",
  "district": "New Delhi",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "vaccine_name": "COVID-19 Booster",
  "target_population": "Adults 18+",
  "doses_allocated": 10000,
  "doses_administered": 7500,
  "partner_org": "Delhi Health Department",
  "notes": "Winter campaign",
  "created_at": "2024-01-15T10:00:00Z"
}
```
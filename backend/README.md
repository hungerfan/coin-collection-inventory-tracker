# Coin Collection Tracker - Django REST API Backend

A modern REST API backend built with Django and Django REST Framework for managing coin collections.

## 🚀 Quick Start

### 1. Set Up Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Use your existing MySQL database credentials
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=coin_tracker
DB_PORT=3306
```

### 4. Verify Database Connection

Django will use your **existing MySQL database** - the same one your CLI app uses! No migration needed since the tables already exist.

However, Django needs to create some of its own tables (for admin, sessions, etc.):

```bash
# This creates Django's built-in tables, won't touch your coin tables
python manage.py migrate
```

### 5. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Start the Server

```bash
python manage.py runserver
```

The API will be available at: **http://localhost:8000**

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API root with endpoint list |
| `/api/coins/` | GET | List all coins |
| `/api/coins/` | POST | Create a new coin |
| `/api/coins/{id}/` | GET | Get specific coin |
| `/api/coins/{id}/` | PUT | Update coin |
| `/api/coins/{id}/` | DELETE | Delete coin |
| `/api/coin-types/` | GET, POST | List/Create coin types |
| `/api/coin-types/{id}/` | GET, PUT, DELETE | Retrieve/Update/Delete coin type |
| `/api/conditions/` | GET, POST | List/Create conditions |
| `/api/conditions/{id}/` | GET, PUT, DELETE | Retrieve/Update/Delete condition |
| `/api/countries/` | GET, POST | List/Create countries |
| `/api/countries/{id}/` | GET, PUT, DELETE | Retrieve/Update/Delete country |
| `/api/stats/` | GET | Get collection statistics |

### Statistics Endpoint

`GET /api/stats/`

Returns:
```json
{
  "total_coins": 19,
  "total_estimated_value": "450.00",
  "total_melt_value": "665.00",
  "coin_types_count": 5,
  "countries_count": 2,
  "conditions_count": 7
}
```

## 🌐 Testing the API

### Option 1: Browser (Django Browsable API)

Django REST Framework provides a beautiful web interface for testing!

1. Visit: `http://localhost:8000/api/coins/`
2. You'll see all your coins in a nice web interface
3. Click buttons to POST, PUT, or DELETE
4. No Postman needed!

### Option 2: cURL

```bash
# List all coins
curl http://localhost:8000/api/coins/

# Get specific coin
curl http://localhost:8000/api/coins/1/

# Get stats
curl http://localhost:8000/api/stats/

# Create a new coin (requires proper JSON)
curl -X POST http://localhost:8000/api/coins/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": 1,
    "year": 2023,
    "mint_mark": "S",
    "condition": 1,
    "quantity": 1,
    "value_estimate": "45.00"
  }'
```

### Option 3: Postman

Import these URLs into Postman and test all endpoints.

### Option 4: Django Admin Panel

Visit: `http://localhost:8000/admin/`

Log in with your superuser credentials to manage data through a beautiful admin interface!

## 🏗️ Architecture

```
HTTP Request
    ↓
URL Router (api/urls.py)
    ↓
ViewSet (api/views.py)
    ↓
Serializer (api/serializers.py)
    ↓
Model (api/models.py)
    ↓
MySQL Database (your existing database!)
```

## 📁 Project Structure

```
backend/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this!)
│
├── config/               # Project configuration
│   ├── __init__.py
│   ├── settings.py       # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI server config
│
└── api/                  # Main API app
    ├── models.py         # Database models
    ├── serializers.py    # JSON serialization
    ├── views.py         # API endpoints
    ├── urls.py          # API URL routing
    └── admin.py         # Admin panel config
```

## 🔧 Common Commands

```bash
# Start development server
python manage.py runserver

# Start on different port
python manage.py runserver 8080

# Create migrations (if you change models)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell (interactive Python with Django)
python manage.py shell

# Check for issues
python manage.py check
```

## 🧪 Testing with Python

You can test the API programmatically:

```python
import requests

# Get all coins
response = requests.get('http://localhost:8000/api/coins/')
print(response.json())

# Get stats
response = requests.get('http://localhost:8000/api/stats/')
print(response.json())
```

## 🎯 Next Steps

Now that your backend is running:

1. ✅ Test all endpoints in your browser
2. ✅ Verify your 19 coins appear in the API
3. ✅ Try the admin panel
4. 📱 Build a React frontend (Phase 2)
5. 🔐 Add authentication (Phase 3)
6. 🚀 Deploy to production (Phase 5)

## 🐛 Troubleshooting

### Can't connect to database
- Verify .env file has correct credentials
- Make sure MySQL server is running
- Test connection: `mysql -h localhost -u your_user -p`

### "ModuleNotFoundError"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Port 8000 already in use
- Another app is using port 8000
- Use different port: `python manage.py runserver 8080`

### Can't see my data
- Check database name in .env matches your CLI app's database
- Verify tables exist: `python manage.py dbshell`

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [HTTP Methods Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

## 💡 Tips

1. **Browsable API**: Django REST Framework's browsable API is your best friend for testing!
2. **Admin Panel**: Use it to quickly view/edit data during development
3. **Django Shell**: Great for testing queries: `python manage.py shell`
4. **Logging**: Check `logs/django.log` for debugging

---

**Your CLI app still works!** This API is completely separate. You can use both at the same time!


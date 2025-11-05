# Environment Variables Setup

## 📋 Overview

The Django backend shares database credentials with your CLI app but needs some Django-specific settings.

## 🔄 Two Approaches

### **Recommended: Shared Database Credentials** ✅

Django will automatically read from your **root `.env` file** for database credentials. You only need a small `backend/.env` for Django-specific settings.

#### Root `.env` (already exists)
```env
# Database credentials (shared by both CLI app and Django)
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=coin_tracker
DB_PORT=3306
```

#### `backend/.env` (create this - Django-only settings)
```env
# Django Secret Key (required for Django)
SECRET_KEY=django-insecure-dev-key-change-in-production

# Debug mode
DEBUG=True

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS for React frontend (when you build it)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**That's it!** Django will:
1. Load DB credentials from root `.env`
2. Load Django-specific settings from `backend/.env`

---

### Alternative: All-in-One Backend .env

If you prefer, you can put everything in `backend/.env`:

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (duplicated from root .env)
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=coin_tracker
DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

But this duplicates your database credentials. 😐

---

## 🎯 Quick Setup (Recommended Way)

### Step 1: Verify Root .env Exists
You should already have this from your CLI app:

```
C:\sites\Python\repos\coin-collection-inventory-tracker\.env
```

If not, create it with your database credentials.

### Step 2: Create backend/.env
Create `backend/.env` with just Django settings:

```env
SECRET_KEY=my-dev-secret-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 3: Test It
```bash
cd backend
python manage.py check
```

If it connects to your database, you're all set! ✅

---

## 🔐 Security Notes

### SECRET_KEY
- **Development**: Any random string is fine
- **Production**: Generate a secure key:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

### DEBUG
- **Development**: `DEBUG=True` (shows detailed errors)
- **Production**: `DEBUG=False` (hides error details from users)

### Database Password
- Never commit `.env` files to git!
- `.gitignore` already excludes them

---

## 🧪 Testing Your Configuration

```bash
# Check if Django can read your settings
python manage.py check

# Test database connection
python manage.py dbshell
# This opens MySQL prompt if connection works
# Type: exit

# View your settings
python manage.py diffsettings
```

---

## ❓ FAQ

### Q: Do I need to copy my database password?
**A:** No! Django reads it from your root `.env` automatically.

### Q: What if I change my database password?
**A:** Just update it in the root `.env`. Both apps will see the change.

### Q: Can I use different databases for CLI and Django?
**A:** Yes! Just put different `DB_*` variables in `backend/.env` and they'll override the root ones.

### Q: What's SECRET_KEY for?
**A:** Django uses it for cryptographic signing (sessions, cookies, CSRF protection). Required for Django to run.

---

## ✅ Minimal Setup Checklist

- [ ] Root `.env` exists with database credentials
- [ ] Created `backend/.env` with SECRET_KEY
- [ ] Can run `python manage.py check` without errors
- [ ] Can connect to database

That's all you need!


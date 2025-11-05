# Getting Started with Django Backend

## 🎯 What You'll Do

You're going to start your Django API server and see your 19 coins through a web interface instead of the CLI!

## ⚡ Step-by-Step Instructions

### Step 1: Open Terminal in Backend Folder

```bash
cd C:\sites\Python\repos\coin-collection-inventory-tracker\backend
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

This creates a new Python environment just for Django. Takes about 30 seconds.

### Step 3: Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` appear before your prompt.

### Step 4: Install Django and Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django (the web framework)
- Django REST Framework (for APIs)
- PyMySQL (MySQL connector)
- Other helpful packages

Takes about 1-2 minutes.

### Step 5: Create Environment File

Create a file named `.env` in the `backend/` folder with your database credentials:

```env
SECRET_KEY=my-secret-key-for-django-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Copy these from your main .env file
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=coin_tracker
DB_PORT=3306
```

**Important**: Use the **same database credentials** as your CLI app! Django will connect to your existing database.

### Step 6: Run Django Migrations

```bash
python manage.py migrate
```

This creates Django's built-in tables (for admin panel, sessions, etc.). It **won't** touch your coin tables!

### Step 7: Create Admin User (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin` (or whatever you want)
- Email: your email or just press Enter
- Password: something you'll remember

### Step 8: Start the Server! 🚀

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**🎉 Congratulations! Your Django API is running!**

### Step 9: Test Your API in Browser

Open your browser and visit these URLs:

#### 1. **API Root**
```
http://localhost:8000/api/
```
You'll see a welcome message and list of endpoints.

#### 2. **View Your Coins**
```
http://localhost:8000/api/coins/
```
**This is magical!** You'll see:
- All 19 of your coins in JSON format
- A beautiful web interface
- Buttons to add, edit, or delete coins
- Forms to create new coins

#### 3. **View Statistics**
```
http://localhost:8000/api/stats/
```
See your total estimated value, melt value, and counts!

#### 4. **View Coin Types**
```
http://localhost:8000/api/coin-types/
```

#### 5. **Django Admin Panel** (if you created superuser)
```
http://localhost:8000/admin/
```
Log in with your admin credentials. This is a beautiful interface to manage all your data!

## 🎨 What You're Seeing

### The Django Browsable API

When you visit `http://localhost:8000/api/coins/`, you're seeing Django REST Framework's **browsable API**. This is a web interface that lets you:

- **Browse data**: See all your coins formatted nicely
- **Test endpoints**: Use forms to POST/PUT/DELETE
- **See JSON**: Raw JSON responses
- **No Postman needed**: Everything testable in the browser!

### Example: What You'll See

```json
[
  {
    "id": 1,
    "type": 1,
    "coin_type_name": "Morgan Dollar",
    "year": 1921,
    "mint_mark": "S",
    "condition": 1,
    "condition_name": "MS-65",
    "quantity": 1,
    "value_estimate": "45.00",
    "acquired_from": "Local coin shop",
    "notes": "Beautiful luster",
    "country_name": "United States",
    "country_code": "US",
    "denomination": "1 Dollar",
    "metal": "Silver"
  },
  ...
]
```

## 🧪 Try These Tests

### Test 1: Get All Coins
Visit: `http://localhost:8000/api/coins/`

You should see all 19 coins!

### Test 2: Get One Coin
Visit: `http://localhost:8000/api/coins/1/`

Replace `1` with any coin ID. You'll see detailed info for that coin.

### Test 3: Get Stats
Visit: `http://localhost:8000/api/stats/`

You should see:
```json
{
  "total_coins": 19,
  "total_estimated_value": "XXX.XX",
  "total_melt_value": "665.00",
  ...
}
```

### Test 4: Add a Coin (Via Web Interface)

1. Go to: `http://localhost:8000/api/coins/`
2. Scroll to bottom
3. Fill in the form (you'll see dropdowns for type and condition)
4. Click "POST"
5. New coin added! 🎉

## 🎓 Understanding What Just Happened

### Your CLI App
```
Python Code → database.py → Raw SQL → MySQL
```

### Your New Django API
```
Browser → HTTP Request → Django View → Django Model → MySQL
```

**Same database, different interface!**

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (Django, DRF, etc.)
- [ ] .env file created with database credentials
- [ ] Migrations ran successfully
- [ ] Server starts without errors
- [ ] Can view `/api/coins/` in browser
- [ ] Can see your 19 coins
- [ ] Can view `/api/stats/`
- [ ] Admin panel accessible (if created superuser)

## 🎯 What's Next?

Now that your API works, you can:

1. **Explore the Admin Panel**: Best way to manage data during development
2. **Test All Endpoints**: Try coin-types, conditions, countries
3. **Learn React**: Build a frontend to consume this API
4. **Add Features**: Authentication, filtering, search, etc.

## 🐛 Common Issues

### Issue: "Can't connect to database"

**Fix**: Check your `.env` file. Make sure DB_NAME, DB_USER, DB_PASSWORD match your CLI app's database.

### Issue: "Port 8000 already in use"

**Fix**:
```bash
# Use a different port
python manage.py runserver 8080
```

Then visit: `http://localhost:8080/api/`

### Issue: "ModuleNotFoundError: No module named 'rest_framework'"

**Fix**: Virtual environment not activated or packages not installed
```bash
# Make sure you see (venv) in your prompt
venv\Scripts\activate

# Then install
pip install -r requirements.txt
```

### Issue: "No module named 'api'"

**Fix**: Make sure you're in the `backend/` directory when running commands.

## 💡 Pro Tips

1. **Keep the server running**: It auto-reloads when you change code!
2. **Use the browsable API**: It's way easier than Postman for testing
3. **Check the logs**: Helpful error messages appear in the terminal
4. **Use Django shell**: Test queries interactively
   ```bash
   python manage.py shell
   >>> from api.models import Coin
   >>> Coin.objects.count()
   19
   ```

## 🎊 You Did It!

You now have a **professional REST API** that:
- Serves your coin data over HTTP
- Provides JSON responses
- Has a beautiful browsable interface
- Connects to your existing database
- Is ready for a React frontend!

**This is exactly what companies use in production!**

---

**Questions?** The Django documentation is excellent: https://docs.djangoproject.com/

**Ready for React?** Let me know and we'll start Phase 2!


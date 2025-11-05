# Django Command Cheat Sheet

Quick reference for common Django commands you'll use.

## 🚀 Starting/Stopping Server

```bash
# Start development server
python manage.py runserver

# Start on different port
python manage.py runserver 8080

# Stop server
Ctrl+C (or Ctrl+Break on Windows)
```

## 🔧 Database Commands

```bash
# Create migration files (after changing models)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Open database shell (MySQL prompt)
python manage.py dbshell

# Reset database (DANGEROUS - deletes all data!)
python manage.py flush
```

## 👤 User Management

```bash
# Create superuser for admin panel
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

## 🐚 Django Shell (Interactive Python)

```bash
# Start Django shell
python manage.py shell
```

Inside the shell:
```python
# Import models
from api.models import Coin, CoinType, Condition, Country

# Get all coins
coins = Coin.objects.all()
print(coins.count())  # 19

# Get specific coin
coin = Coin.objects.get(id=1)
print(coin.type.name)  # "Morgan Dollar"

# Filter coins
silver_coins = Coin.objects.filter(type__metal="Silver")

# Get coin with related data (efficient)
coin = Coin.objects.select_related('type', 'condition').get(id=1)
print(f"{coin.type.name} in {coin.condition.name}")

# Create new coin
coin = Coin.objects.create(
    type_id=1,
    year=2023,
    condition_id=1,
    quantity=1,
    value_estimate=50.00
)

# Update coin
coin.year = 2024
coin.save()

# Delete coin
coin.delete()

# Aggregate queries
from django.db.models import Sum, Count, Avg
total_value = Coin.objects.aggregate(Sum('value_estimate'))
print(total_value)  # {'value_estimate__sum': Decimal('450.00')}

# Exit shell
exit()
```

## 📊 Utility Commands

```bash
# Check for problems
python manage.py check

# Show all available commands
python manage.py help

# Show SQL for a migration
python manage.py sqlmigrate api 0001

# Collect static files (for deployment)
python manage.py collectstatic

# Create empty migration (for custom SQL)
python manage.py makemigrations --empty api
```

## 🧪 Testing Commands

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test api

# Run specific test
python manage.py test api.tests.test_models.CoinTestCase

# Run with verbose output
python manage.py test --verbosity=2
```

## 🔍 Inspection Commands

```bash
# Show database tables
python manage.py inspectdb

# Show model schema
python manage.py showmigrations

# Validate models
python manage.py check --deploy
```

## 📦 Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\activate

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (Mac/Linux)
source venv/bin/activate

# Deactivate
deactivate

# Install packages
pip install -r requirements.txt

# Save current packages
pip freeze > requirements.txt

# Update package
pip install --upgrade package_name
```

## 🌐 URLS to Remember

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/api/` | API root |
| `http://localhost:8000/api/coins/` | List coins |
| `http://localhost:8000/api/stats/` | Statistics |
| `http://localhost:8000/admin/` | Admin panel |

## 💡 Quick Tips

### See all coins in shell
```python
python manage.py shell
>>> from api.models import Coin
>>> for coin in Coin.objects.all()[:5]:
...     print(f"{coin.id}: {coin.type.name} ({coin.year})")
```

### Count records
```python
>>> from api.models import Coin, CoinType, Condition, Country
>>> print(f"Coins: {Coin.objects.count()}")
>>> print(f"Types: {CoinType.objects.count()}")
>>> print(f"Conditions: {Condition.objects.count()}")
>>> print(f"Countries: {Country.objects.count()}")
```

### Find coins by year
```python
>>> coins_2020s = Coin.objects.filter(year__gte=2020)
>>> print(coins_2020s.count())
```

### Get most valuable coins
```python
>>> expensive_coins = Coin.objects.order_by('-value_estimate')[:5]
>>> for coin in expensive_coins:
...     print(f"{coin.type.name}: ${coin.value_estimate}")
```

## 🐛 Troubleshooting Commands

### Can't connect to database
```bash
# Test database connection
python manage.py dbshell
# If this fails, check your .env file
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Server won't start
```bash
# Check for syntax errors
python manage.py check

# Try different port
python manage.py runserver 8080
```

### Clear Python cache
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Mac/Linux
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
```

## 📚 Learning Resources

- **Django Shell**: Perfect for testing queries
- **Admin Panel**: Best for managing data during development
- **Django Debug Toolbar**: Add for detailed debugging
- **Django Extensions**: `pip install django-extensions` for more commands

---

**Pro Tip**: Keep this file open while developing! These commands are what you'll use daily.


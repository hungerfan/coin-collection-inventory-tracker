# Coin Collection Inventory Tracker

A Python application for tracking and managing coin collections with MySQL database backend.

## Features

- Track individual coins with detailed information
- Manage coin types, conditions, and countries
- Dynamic addition of new coin types and conditions
- Value estimation tracking
- Acquisition history and notes

## Database Schema

The application uses a normalized database design with the following tables:

- **coins** - Main table storing individual coin records
- **coin_types** - Lookup table for coin types (Morgan Dollar, Lincoln Cent, etc.)
- **conditions** - Lookup table for coin conditions (MS-65, AU-58, etc.)
- **countries** - Lookup table for countries with ISO codes

## Requirements

- Python 3.7+
- MySQL database
- Required packages:
  - PyMySQL
  - cryptography
  - python-dotenv

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update database connection details in `.env`

5. Run the application:
   ```bash
   python main.py
   ```

## Configuration

Create a `.env` file with your database credentials:

```env
DB_HOST=your_mysql_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
DB_PORT=3306
```

## Usage

The application provides functions for:
- Connecting to the database
- Managing coin inventory (planned)

## Development

This project is in active development. Current status:
- ✅ Database schema design
- ✅ Database connection setup
- ✅ Countries table population
- 🚧 Coin management interface (planned)
- 🚧 Web interface (planned)

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

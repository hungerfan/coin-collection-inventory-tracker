# Database Migrations

This folder contains SQL migration scripts for database schema changes.

## Running Migrations

### Using MySQL Command Line

```bash
# Connect to your database
mysql -u your_username -p your_database_name

# Run the migration
source add_reference_number.sql

# Or pipe it directly
mysql -u your_username -p your_database_name < add_reference_number.sql
```

### Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your database
3. Open `add_reference_number.sql`
4. Execute the script (Ctrl+Shift+Enter or click Execute button)

## Migration: add_reference_number.sql

**Purpose:** Adds `reference_number` field to coins table for physical labeling

**What it does:**
- Adds `reference_number` column to `coins` table
- Populates existing coins with sequential numbers (1, 2, 3...)
- Adds unique constraint to prevent duplicates
- Makes field NOT NULL

**After running:**
- Your existing coins will be numbered 1-19 (or however many you have)
- New coins will automatically get the next sequential number
- Display format in CLI: "001", "002", etc. (padded to 3 digits)

## Rollback (if needed)

```sql
-- Remove the reference_number column
ALTER TABLE coins DROP COLUMN reference_number;
```

**Note:** Only run rollback if you need to undo the migration completely.


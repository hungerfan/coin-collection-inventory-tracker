-- Migration: Add reference_number column to coins table
-- Purpose: Add physical label numbers for coin flips (001-999)
-- Date: 2025-11-05

-- Step 1: Add the column (nullable initially)
ALTER TABLE coins
ADD COLUMN reference_number INT NULL
AFTER id;

-- Step 2: Populate existing coins with sequential numbers
SET @row_number = 0;
UPDATE coins
SET reference_number = (@row_number := @row_number + 1)
ORDER BY id;

-- Step 3: Add unique constraint (prevent duplicate reference numbers)
ALTER TABLE coins
ADD CONSTRAINT unique_reference_number UNIQUE (reference_number);

-- Step 4: Make it NOT NULL now that all rows have values
ALTER TABLE coins
MODIFY reference_number INT NOT NULL;

-- Verification query (optional - run to check results)
-- SELECT id, reference_number, year FROM coins ORDER BY reference_number;


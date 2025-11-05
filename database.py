"""Database operations for the Coin Tracker application.

This module provides all database interaction functionality including
connections, queries, and CRUD operations for coins, coin types,
conditions, and countries.
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any, List
import pymysql

from config import db_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            "Logs/coin_tracker_database.log", maxBytes=1024 * 1024, backupCount=5
        )
    ],
)
logger = logging.getLogger(__name__)


def connect_to_database() -> pymysql.connections.Connection:
    """Connect to the MySQL database with proper error handling.

    Returns:
        Active database connection with DictCursor

    Raises:
        pymysql.Error: If connection fails
    """
    try:
        conn = pymysql.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password,
            database=db_config.name,
            port=db_config.port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        logger.info("Successfully connected to database: %s on %s",
                    db_config.name, db_config.host)
        return conn
    except pymysql.Error as e:
        logger.error("Database connection failed: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during database connection: %s", e)
        raise


def _execute_query(
    sql: str,
    params: tuple = None,
    query_type: str = "SELECT",
    fetch_one: bool = True
) -> Optional[Dict[str, Any]] | List[Dict[str, Any]] | int:
    """Execute database query with consistent error handling.

    Args:
        sql: SQL query string with %s placeholders
        params: Tuple of parameters for query
        query_type: Query type - SELECT, INSERT, UPDATE, or DELETE
        fetch_one: If True, return single row; if False, return all rows

    Returns:
        - SELECT queries: dict (if fetch_one) or list of dicts
        - INSERT queries: last inserted row ID (int)
        - UPDATE/DELETE: number of affected rows (int)

    Raises:
        pymysql.Error: Database operation failed
    """
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())

                if query_type == "SELECT":
                    return cur.fetchone() if fetch_one else cur.fetchall()
                elif query_type == "INSERT":
                    conn.commit()
                    return cur.lastrowid
                else:  # UPDATE or DELETE
                    conn.commit()
                    return cur.rowcount

    except pymysql.Error as e:
        logger.error("Database error executing %s query: %s", query_type, e)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


# ============================================================================
# COIN OPERATIONS
# ============================================================================

def get_data_count() -> int:
    """Get the count of records in the coins table.

    Returns:
        Number of coins in the database
    """
    result = _execute_query(
        "SELECT COUNT(*) as count FROM coins", fetch_one=True)
    count = result["count"]
    logger.info("Retrieved coin count: %s", count)
    return count


def get_coins() -> List[Dict[str, Any]]:
    """Get all coins from the database.

    Returns:
        List of coin dictionaries
    """
    return _execute_query("SELECT * FROM coins", fetch_one=False)


def get_coin_by_id(coin_id: int) -> Optional[Dict[str, Any]]:
    """Get a coin by its ID.

    Args:
        coin_id: Unique identifier of the coin

    Returns:
        Coin data dictionary or None if not found
    """
    return _execute_query(
        "SELECT * FROM coins WHERE id = %s",
        (int(coin_id),),
        fetch_one=True
    )


def get_coins_with_details() -> List[Dict[str, Any]]:
    """Get all coins with detailed information from joined tables.

    Includes coin type names, condition names, country names and codes
    via LEFT JOIN operations.

    Returns:
        List of coin dictionaries with expanded details
    """
    sql = """
        SELECT
            c.id,
            c.year,
            c.mint_mark,
            c.quantity,
            c.value_estimate,
            c.acquired_from,
            c.notes,
            c.created_at,
            c.updated_at,
            ct.id as coin_type_id,
            ct.name as coin_type_name,
            ct.denomination,
            ct.metal,
            cond.name as condition_name,
            cond.description as condition_description,
            country.name as country_name,
            country.country_code
        FROM coins c
        LEFT JOIN coin_types ct ON c.type_id = ct.id
        LEFT JOIN conditions cond ON c.condition_id = cond.id
        LEFT JOIN countries country ON ct.country_id = country.id
        ORDER BY c.id
    """
    return _execute_query(sql, fetch_one=False)


def save_coin_to_database(coin_data: Dict[str, Any]) -> int:
    """Save coin data to the database.

    Args:
        coin_data: Dictionary containing coin attributes

    Returns:
        ID of the newly inserted coin

    Raises:
        pymysql.Error: If insert fails
    """
    logger.debug("Saving coin data: %s", coin_data)
    sql = (
        "INSERT INTO coins (type_id, year, mint_mark, condition_id, quantity, "
        "value_estimate, acquired_from, notes, created_at) VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
    )
    params = (
        coin_data["type_id"],
        coin_data["year"],
        coin_data["mint_mark"],
        coin_data["condition_id"],
        coin_data["quantity"],
        coin_data["value_estimate"],
        coin_data["acquired_from"],
        coin_data["notes"]
    )
    coin_id = _execute_query(sql, params, query_type="INSERT")
    logger.info("Coin data saved to database with ID: %s", coin_id)
    return coin_id


def update_coin_in_database(coin_data: Dict[str, Any]) -> int:
    """Update coin data in the database.

    Args:
        coin_data: Dictionary containing coin attributes including 'id'

    Returns:
        Number of rows affected (should be 1)

    Raises:
        pymysql.Error: If update fails
    """
    sql = (
        "UPDATE coins SET type_id = %s, year = %s, mint_mark = %s, condition_id = %s, "
        "quantity = %s, value_estimate = %s, acquired_from = %s, notes = %s, "
        "updated_at = NOW() WHERE id = %s"
    )
    params = (
        coin_data["type_id"],
        coin_data["year"],
        coin_data["mint_mark"],
        coin_data["condition_id"],
        coin_data["quantity"],
        coin_data["value_estimate"],
        coin_data["acquired_from"],
        coin_data["notes"],
        coin_data["id"]
    )
    rows_affected = _execute_query(sql, params, query_type="UPDATE")
    logger.info("Coin data updated in database: %s", coin_data)
    return rows_affected


def delete_coin_from_database(coin_id: int) -> int:
    """Delete a coin from the database.

    Args:
        coin_id: ID of the coin to delete

    Returns:
        Number of rows deleted (should be 1)
    """
    return _execute_query(
        "DELETE FROM coins WHERE id = %s",
        (int(coin_id),),
        query_type="DELETE"
    )


# ============================================================================
# COIN TYPE OPERATIONS
# ============================================================================

def get_coin_types() -> List[Dict[str, Any]]:
    """Get all coin types with country information.

    Returns:
        List of coin type dictionaries with country details
    """
    sql = """
        SELECT
            ct.id,
            ct.name,
            ct.denomination,
            ct.metal,
            country.name as country_name,
            country.country_code
        FROM coin_types ct
        LEFT JOIN countries country ON ct.country_id = country.id
        ORDER BY country.name, ct.name
    """
    return _execute_query(sql, fetch_one=False)


def get_coin_type_by_id(coin_type_id: int) -> Optional[Dict[str, Any]]:
    """Get a coin type by its ID with country details.

    Args:
        coin_type_id: Unique identifier of the coin type

    Returns:
        Coin type data dictionary with country name, or None if not found
    """
    sql = """
        SELECT
            ct.id,
            ct.name,
            ct.denomination,
            ct.country_id,
            ct.metal,
            c.name as country_name,
            c.country_code
        FROM coin_types ct
        LEFT JOIN countries c ON ct.country_id = c.id
        WHERE ct.id = %s
    """
    return _execute_query(sql, (int(coin_type_id),), fetch_one=True)


def save_coin_type_to_database(coin_type_data: Dict[str, Any]) -> int:
    """Save coin type data to the database.

    Args:
        coin_type_data: Dictionary containing coin type attributes

    Returns:
        ID of the newly inserted coin type
    """
    sql = (
        "INSERT INTO coin_types (name, denomination, country_id, metal) VALUES "
        "(%s, %s, %s, %s)"
    )
    params = (
        coin_type_data["name"],
        coin_type_data["denomination"],
        coin_type_data["country_id"],
        coin_type_data["metal"],
    )
    return _execute_query(sql, params, query_type="INSERT")


def update_coin_type_in_database(coin_type_data: Dict[str, Any]) -> int:
    """Update coin type data in the database.

    Args:
        coin_type_data: Dictionary containing coin type attributes including 'id'

    Returns:
        Number of rows affected (should be 1)
    """
    sql = (
        "UPDATE coin_types SET name = %s, denomination = %s, country_id = %s, "
        "metal = %s WHERE id = %s"
    )
    params = (
        coin_type_data["name"],
        coin_type_data["denomination"],
        coin_type_data["country_id"],
        coin_type_data["metal"],
        coin_type_data["id"]
    )
    return _execute_query(sql, params, query_type="UPDATE")


def delete_coin_type_from_database(coin_type_id: int) -> int:
    """Delete a coin type from the database.

    Args:
        coin_type_id: ID of the coin type to delete

    Returns:
        Number of rows deleted (should be 1)
    """
    return _execute_query(
        "DELETE FROM coin_types WHERE id = %s",
        (int(coin_type_id),),
        query_type="DELETE"
    )


# ============================================================================
# CONDITION OPERATIONS
# ============================================================================

def get_conditions() -> List[Dict[str, Any]]:
    """Get all conditions from the database.

    Returns:
        List of condition dictionaries
    """
    return _execute_query("SELECT * FROM conditions", fetch_one=False)


def get_condition_by_id(condition_id: int) -> Optional[Dict[str, Any]]:
    """Get a condition by its ID.

    Args:
        condition_id: Unique identifier of the condition

    Returns:
        Condition data dictionary or None if not found
    """
    return _execute_query(
        "SELECT * FROM conditions WHERE id = %s",
        (int(condition_id),),
        fetch_one=True
    )


def save_condition_to_database(condition_data: Dict[str, Any]) -> int:
    """Add a new condition to the database.

    Args:
        condition_data: Dictionary containing condition attributes

    Returns:
        ID of the newly inserted condition
    """
    sql = "INSERT INTO conditions (name, description) VALUES (%s, %s)"
    params = (
        condition_data["name"],
        condition_data["description"]
    )
    return _execute_query(sql, params, query_type="INSERT")


def update_condition_in_database(condition_data: Dict[str, Any]) -> int:
    """Update condition data in the database.

    Args:
        condition_data: Dictionary containing condition attributes including 'id'

    Returns:
        Number of rows affected (should be 1)
    """
    sql = "UPDATE conditions SET name = %s, description = %s WHERE id = %s"
    params = (
        condition_data["name"],
        condition_data["description"],
        condition_data["id"]
    )
    return _execute_query(sql, params, query_type="UPDATE")


def delete_condition_from_database(condition_id: int) -> int:
    """Delete a condition from the database.

    Args:
        condition_id: ID of the condition to delete

    Returns:
        Number of rows deleted (should be 1)
    """
    return _execute_query(
        "DELETE FROM conditions WHERE id = %s",
        (int(condition_id),),
        query_type="DELETE"
    )


# ============================================================================
# COUNTRY OPERATIONS
# ============================================================================

def get_countries() -> List[Dict[str, Any]]:
    """Get all countries from the database.

    Returns:
        List of country dictionaries
    """
    return _execute_query("SELECT * FROM countries", fetch_one=False)


def get_country_by_id(country_id: int) -> Optional[Dict[str, Any]]:
    """Get a country by its ID.

    Args:
        country_id: Unique identifier of the country

    Returns:
        Country data dictionary or None if not found
    """
    return _execute_query(
        "SELECT * FROM countries WHERE id = %s",
        (int(country_id),),
        fetch_one=True
    )


def get_country_id_by_code(country_code: str) -> Optional[int]:
    """Get the country ID by country code.

    Args:
        country_code: ISO country code (e.g., 'US', 'CA')

    Returns:
        Country ID or None if not found

    Raises:
        pymysql.Error: If query fails
    """
    result = _execute_query(
        "SELECT id FROM countries WHERE country_code = %s",
        (country_code,),
        fetch_one=True
    )
    return result["id"] if result else None


def save_country_to_database(country_data: Dict[str, Any]) -> Optional[int]:
    """Add a new country to the database.

    Checks for duplicate country codes before inserting.

    Args:
        country_data: Dictionary containing country attributes

    Returns:
        ID of newly inserted country, or None if country code already exists

    Raises:
        pymysql.Error: If database operation fails
    """
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                # Check for existing country code
                cur.execute(
                    "SELECT id FROM countries WHERE country_code = %s",
                    (country_data["country_code"],)
                )
                if cur.fetchone():
                    return None

                # Insert new country
                sql = "INSERT INTO countries (name, country_code) VALUES (%s, %s)"
                cur.execute(
                    sql, (country_data["name"], country_data["country_code"]))
                conn.commit()
                return cur.lastrowid

    except pymysql.Error as e:
        logger.error("Database error while adding country: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding country: %s", e)
        raise


def update_country_in_database(country_data: Dict[str, Any]) -> int:
    """Update country data in the database.

    Args:
        country_data: Dictionary containing country attributes including 'id'

    Returns:
        Number of rows affected (should be 1)
    """
    sql = "UPDATE countries SET name = %s, country_code = %s WHERE id = %s"
    params = (
        country_data["name"],
        country_data["country_code"],
        country_data["id"]
    )
    return _execute_query(sql, params, query_type="UPDATE")


def delete_country_from_database(country_id: int) -> int:
    """Delete a country from the database.

    Args:
        country_id: ID of the country to delete

    Returns:
        Number of rows deleted (should be 1)
    """
    return _execute_query(
        "DELETE FROM countries WHERE id = %s",
        (int(country_id),),
        query_type="DELETE"
    )

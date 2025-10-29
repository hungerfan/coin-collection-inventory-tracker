import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import pymysql

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

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", "3306"))


def connect_to_database():
    """Connect to the MySQL database with proper error handling."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
        )
        logger.info("Successfully connected to database: %s on %s",
                    DB_NAME, DB_HOST)
        return conn
    except pymysql.Error as e:
        logger.error("Database connection failed: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during database connection: %s", e)
        raise


def get_data_count():
    """Get the count of records in the coins table."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(*) as count FROM coins"
                cur.execute(sql)
                result = cur.fetchone()
                count = result["count"]
                logger.info("Retrieved coin count: %s", count)
                return count
    except pymysql.Error as e:
        logger.error("Database error while getting coin count: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coin count: %s", e)
        raise


def get_coins():
    """Get all coins from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM coins"
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coins: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coins: %s", e)
        raise


def get_coin_by_id(coin_id: str):
    """Get a coin by its ID."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM coins WHERE id = %s"
                cur.execute(sql, (int(coin_id)))
                result = cur.fetchone()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coin by ID: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coin by ID: %s", e)
        raise


def get_coins_with_details():
    """Get all coins with detailed information including coin type names, condition names,
       country names and codes."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
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
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coins with details: %s", e)
        raise
    except Exception as e:
        logger.error(
            "Unexpected error while getting coins with details: %s", e)
        raise


def save_coin_to_database(coin_data):
    """Save coin data to the database."""
    print(f"Saving coin data: {coin_data}")
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = (
                    "INSERT INTO coins (type_id, year, mint_mark, condition_id, quantity, "
                    "value_estimate, acquired_from, notes, created_at) VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
                )
                cur.execute(
                    sql,
                    (
                        coin_data["type_id"],
                        coin_data["year"],
                        coin_data["mint_mark"],
                        coin_data["condition_id"],
                        coin_data["quantity"],
                        coin_data["value_estimate"],
                        coin_data["acquired_from"],
                        coin_data["notes"]
                    ),
                )
                conn.commit()
                logger.info("Coin data saved to database: %s", coin_data)
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while saving coin data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving coin data: %s", e)
        raise


def update_coin_in_database(coin_data):
    """Update coin data in the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = (
                    "UPDATE coins SET type_id = %s, year = %s, mint_mark = %s, condition_id = %s, "
                    "quantity = %s, value_estimate = %s, acquired_from = %s, notes = %s, "
                    "updated_at = NOW() WHERE id = %s"
                )
                cur.execute(
                    sql,
                    (
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
                )
                logger.info("Coin data updated in database: %s", coin_data)
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while updating coin data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while updating coin data: %s", e)
        raise


def get_coin_type_by_id(coin_type_id: str):
    """Get a coin type by its ID."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM coin_types WHERE id = %s"
                cur.execute(sql, (int(coin_type_id)))
                result = cur.fetchone()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coin type by ID: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coin type by ID: %s", e)
        raise


def get_coin_types():
    """Get all coin types from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
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
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coin types: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coin types: %s", e)
        raise


def save_coin_type_to_database(coin_type_data):
    """Save coin type data to the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = (
                    "INSERT INTO coin_types (name, denomination, country_id, metal) VALUES "
                    "(%s, %s, %s, %s)"
                )
                cur.execute(
                    sql,
                    (
                        coin_type_data["name"],
                        coin_type_data["denomination"],
                        coin_type_data["country_id"],
                        coin_type_data["metal"],
                    )
                )
                conn.commit()
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while saving coin type data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving coin type data: %s", e)
        raise


def update_coin_type_in_database(coin_type_data):
    """Update coin type data in the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = (
                    "UPDATE coin_types SET name = %s, denomination = %s, country_id = %s, "
                    "metal = %s WHERE id = %s"
                )
                cur.execute(
                    sql,
                    (
                        coin_type_data["name"],
                        coin_type_data["denomination"],
                        coin_type_data["country_id"],
                        coin_type_data["metal"],
                        coin_type_data["id"]
                    )
                )
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while updating coin type data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while updating coin type data: %s", e)
        raise


def get_conditions():
    """Get all conditions from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM conditions"
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting conditions: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting conditions: %s", e)
        raise


def get_condition_by_id(condition_id: str):
    """Get a condition by its ID."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM conditions WHERE id = %s"
                cur.execute(sql, (int(condition_id)))
                result = cur.fetchone()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting condition by ID: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting condition by ID: %s", e)
        raise


def save_condition_to_database(condition_data):
    """
    Add a new condition to the database.

    @param name: The name of the condition.
    @return: inserted id of the condition.
    """
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO conditions (name, description) VALUES (%s, %s)"
                cur.execute(
                    sql,
                    (
                        condition_data["name"],
                        condition_data["description"]
                    )
                )
                conn.commit()
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while adding condition: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding condition: %s", e)
        raise


def update_condition_in_database(condition_data):
    """Update condition data in the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "UPDATE conditions SET name = %s, description = %s WHERE id = %s"
                cur.execute(
                    sql,
                    (
                        condition_data["name"],
                        condition_data["description"],
                        condition_data["id"]
                    )
                )
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while updating condition data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while updating condition data: %s", e)
        raise


def get_countries():
    """Get all countries from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM countries"
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting countries: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting countries: %s", e)
        raise


def get_country_by_id(country_id: str):
    """Get a country by its ID."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM countries WHERE id = %s"
                cur.execute(sql, (int(country_id)))
                result = cur.fetchone()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting country by ID: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting country by ID: %s", e)
        raise


def get_country_id_by_code(country_code):
    """Get the country ID by country code."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT id FROM countries WHERE country_code = %s"
                cur.execute(sql, (country_code,))
                return cur.fetchone()["id"]
    except pymysql.Error as e:
        logger.error("Database error while getting country ID by code: %s", e)
        raise
    except Exception as e:
        logger.error(
            "Unexpected error while getting country ID by code: %s", e)
        raise


def save_country_to_database(country_data):
    """Add a new country to the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM countries WHERE country_code = %s",
                            (country_data["country_code"],))
                if cur.fetchone():
                    # country code already exists
                    return None
                else:
                    sql = "INSERT INTO countries (name, country_code) VALUES (%s, %s)"
                    cur.execute(
                        sql,
                        (
                            country_data["name"],
                            country_data["country_code"]
                        )
                    )
                    conn.commit()
                    return cur.lastrowid

    except pymysql.Error as e:
        logger.error("Database error while adding country: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding country: %s", e)
        raise


def update_country_in_database(country_data):
    """Update country data in the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "UPDATE countries SET name = %s, country_code = %s WHERE id = %s"
                cur.execute(
                    sql,
                    (
                        country_data["name"],
                        country_data["country_code"],
                        country_data["id"]
                    )
                )
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while updating country data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while updating country data: %s", e)
        raise


def delete_coin_from_database(coin_id: str):
    """Delete a coin from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "DELETE FROM coins WHERE id = %s"
                cur.execute(sql, (int(coin_id)))
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while deleting coin: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while deleting coin: %s", e)
        raise


def delete_coin_type_from_database(coin_type_id: str):
    """Delete a coin type from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "DELETE FROM coin_types WHERE id = %s"
                cur.execute(sql, (int(coin_type_id)))
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while deleting coin type: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while deleting coin type: %s", e)
        raise


def delete_condition_from_database(condition_id: str):
    """Delete a condition from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "DELETE FROM conditions WHERE id = %s"
                cur.execute(sql, (int(condition_id)))
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while deleting condition: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while deleting condition: %s", e)
        raise


def delete_country_from_database(country_id: str):
    """Delete a country from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "DELETE FROM countries WHERE id = %s"
                cur.execute(sql, (int(country_id)))
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while deleting country: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while deleting country: %s", e)
        raise

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
        logger.info("Successfully connected to database: %s on %s", DB_NAME, DB_HOST)
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


def get_coins_with_details():
    """Get all coins with detailed information including coin type names, condition names, and country names."""
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
        logger.error("Unexpected error while getting coins with details: %s", e)
        raise


def save_coin_to_database(coin_data):
    """Save coin data to the database."""
    print(f"Saving coin data: {coin_data}")
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = (
                    "INSERT INTO coins (type_id, year, mint_mark, condition_id, quantity, "
                    "value_estimate, acquired_from, notes) VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s, %s)"
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
                    ),
                )
                conn.commit()
                logger.info("Coin data saved to database: %s", coin_data)
                return True
    except pymysql.Error as e:
        logger.error("Database error while saving coin data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving coin data: %s", e)
        raise


def get_coin_types():
    """Get all coin types from the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM coin_types"
                cur.execute(sql)
                result = cur.fetchall()
                return result
    except pymysql.Error as e:
        logger.error("Database error while getting coin types: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while getting coin types: %s", e)
        raise


def add_coin_type(name):
    """
    Add a new coin type to the database.

    @param name: The name of the coin type.
    @return: inserted id of the coin type.
    """
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO coin_types (name) VALUES (%s)"
                cur.execute(sql, (name))
                conn.commit()
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while adding coin type: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding coin type: %s", e)
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
                    ),
                )
                conn.commit()
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while saving coin type data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving coin type data: %s", e)
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


def add_condition(name):
    """
    Add a new condition to the database.

    @param name: The name of the condition.
    @return: inserted id of the condition.
    """
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO conditions (name) VALUES (%s)"
                cur.execute(sql, (name))
                conn.commit()
                return cur.lastrowid
    except pymysql.Error as e:
        logger.error("Database error while adding condition: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding condition: %s", e)
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


def add_country(name, country_code):
    """Add a new country to the database."""
    try:
        with connect_to_database() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO countries (name, country_code) VALUES (%s, %s)"
                cur.execute(sql, (name, country_code))
                conn.commit()
                return True
    except pymysql.Error as e:
        logger.error("Database error while adding country: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while adding country: %s", e)
        raise

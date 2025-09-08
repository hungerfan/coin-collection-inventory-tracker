import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT'))


def connect_to_database():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def insert_data():
    pass


def main():
    with connect_to_database() as db:
        with db.cursor() as cur:
            sql = "SELECT * FROM countries WHERE country_code = 'US'"

            cur.execute(sql)
            db.commit()
    print(cur.fetchall())


if __name__ == "__main__":
    main()

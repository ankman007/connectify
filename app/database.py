import os 
import psycopg2
from loguru import logger
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv()

def get_db_connection():
    try: 
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),  
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("PORT"),
        )
        logger.info("Database connection established successfully.")
        return conn

    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
        
def create_tables(conn):
    create_post_table_query = """
    CREATE TABLE IF NOT EXISTS entry (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        published BOOLEAN DEFAULT TRUE,
        rating INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try: 
        with conn.cursor() as cursor:
            cursor.execute(create_post_table_query)
            cursor.execute(create_users_table_query)
            conn.commit()
            logger.info("Tables created successfully.")
    
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()


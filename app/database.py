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
        
def create_table(conn):
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS post (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        published BOOLEAN DEFAULT TRUE,
        rating INT
    );
    """
    try: 
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'post' created successfully.")
    
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

def insert_post(conn, title, content, published=True, rating=None):
    insert_query = """
    INSERT INTO post (title, content, published, rating)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_query, (title, content, published, rating))
        conn.commit()
        post_id = cursor.fetchone()[0]
        logger.info(f"Inserted post with ID {post_id}.")
        return post_id
    
    except Exception as e:
        logger.error(f"Error inserting post: {e}")
        conn.rollback()
    
    finally:
        cursor.close()

conn = get_db_connection()

mock_title = "Sample Post Title"
mock_content = "This is a sample content for the post."
mock_published = True
mock_rating = 5

insert_post(conn, mock_title, mock_content, mock_published, mock_rating)

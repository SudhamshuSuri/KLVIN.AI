import psycopg2
from config import DATABASE_CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQL Queries to Create Tables
CREATE_COMPANIES_TABLE = """
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
"""

CREATE_DEVICES_TABLE = """
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);
"""

CREATE_DEVICE_READINGS_TABLE = """
CREATE TABLE IF NOT EXISTS device_readings (
    id SERIAL PRIMARY KEY,
    device_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices (id)
);
"""

# Sample Data Insertion Queries
INSERT_COMPANIES = """
INSERT INTO companies (name)
VALUES 
    ('Company A'),
    ('Company B'),
    ('Company C')
ON CONFLICT DO NOTHING;
"""

INSERT_DEVICES = """
INSERT INTO devices (name, company_id)
VALUES 
    ('Device 1', 1),
    ('Device 2', 1),
    ('Device 3', 2),
    ('Device 4', 2),
    ('Device 5', 3)
ON CONFLICT DO NOTHING;
"""

INSERT_DEVICE_READINGS = """
INSERT INTO device_readings (device_id, timestamp)
VALUES 
    (1, NOW() - INTERVAL '1 minute'),
    (2, NOW() - INTERVAL '10 minutes'),
    (3, NOW() - INTERVAL '3 minutes'),
    (4, NOW() - INTERVAL '20 minutes'),
    (5, NOW() - INTERVAL '1 minute')
ON CONFLICT DO NOTHING;
"""

def initialize_database():
    """
    Initialize the PostgreSQL database by creating tables and inserting sample data.
    """
    try:
        # Establish database connection
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Create tables
        logger.info("Creating tables...")
        cursor.execute(CREATE_COMPANIES_TABLE)
        cursor.execute(CREATE_DEVICES_TABLE)
        cursor.execute(CREATE_DEVICE_READINGS_TABLE)

        # Insert sample data
        logger.info("Inserting sample data...")
        cursor.execute(INSERT_COMPANIES)
        cursor.execute(INSERT_DEVICES)
        cursor.execute(INSERT_DEVICE_READINGS)

        # Commit changes
        conn.commit()
        logger.info("Database initialized successfully.")

    except psycopg2.Error as e:
        logger.error("Error initializing the database: %s", e)
        raise
    finally:
        # Close the connection
        if conn:
            cursor.close()
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    initialize_database()


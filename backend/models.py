import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_CONFIG
import logging
import datetime as dt
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
def add_device(name, company_id):
    """
    Add a new device to the database.

    Args:
        name (str): Name of the device.
        company_id (int): ID of the associated company.
    """
    query = """
    INSERT INTO devices (name, company_id)
    VALUES (%s, %s);
    """

    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (name, company_id))
            conn.commit()
    except psycopg2.Error as e:
        logger.error("Error adding device: %s", e)
        raise

'''

def add_device(name, company_id):
    """
    Add a new device to the database and insert an initial reading timestamp.

    Args:
        name (str): Name of the device.
        company_id (int): ID of the associated company.
    """
    device_query = """
    INSERT INTO devices (name, company_id)
    VALUES (%s, %s)
    RETURNING id;
    """
    
    reading_query = """
    INSERT INTO device_readings (device_id)
    VALUES (%s);
    """
    
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            # Execute the first query to insert the device
            cursor.execute(device_query, (name, company_id))
            # Get the generated device ID
            device_id = cursor.fetchone()[0]
            
            # Execute the second query to insert the initial reading
            cursor.execute(reading_query, (device_id,))
            
            # Commit the transaction
            conn.commit()
    except psycopg2.Error as e:
        logger.error("Error adding device: %s", e)
        raise



def get_connection():
    """
    Establish a connection to the PostgreSQL database.
    Returns a new connection object.
    """
    try:
        return psycopg2.connect(**DATABASE_CONFIG)
    except psycopg2.Error as e:
        logger.error("Error connecting to the database: %s", e)
        raise


def fetch_companies():
    """
    Fetch all companies from the database.
    Returns:
        List of dictionaries containing company IDs and names.
    """
    query = "SELECT id, name FROM companies;"

    try:
        with get_connection() as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)
            companies = cursor.fetchall()
            return [{"id": row["id"], "name": row["name"]} for row in companies]
    except psycopg2.Error as e:
        logger.error("Error fetching companies: %s", e)
        raise


from datetime import datetime, timedelta

def fetch_devices(company_id):
    """
    Fetch all devices for a specific company and determine their status.
    A device is online if its last reading is within the last 2 minutes.
    """
    query = """
        SELECT d.id, d.name, MAX(r.timestamp) AS last_reading
        FROM devices d
        LEFT JOIN device_readings r ON d.id = r.device_id
        WHERE d.company_id = %s
        GROUP BY d.id;
    """

    try:
        with get_connection() as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, [company_id])
            devices = cursor.fetchall()

            now = datetime.utcnow()
            two_minutes_ago = now - timedelta(minutes=2)

            # Determine device status based on the timestamp
            return [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "last_reading": row["last_reading"],
                    "status": "online" if row["last_reading"] and row["last_reading"] > two_minutes_ago else "offline"
                    #"status" : row["last_reading"]
                    }
                for row in devices
            ]
    except psycopg2.Error as e:
        logger.error("Error fetching devices for company_id %s: %s", company_id, e)
        raise


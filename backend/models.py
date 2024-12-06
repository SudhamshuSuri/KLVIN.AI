import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    query = "SELECT id, name FROM companies"

    try:
        with get_connection() as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)
            companies = cursor.fetchall()
            return [{"id": row["id"], "name": row["name"]} for row in companies]
    except psycopg2.Error as e:
        logger.error("Error fetching companies: %s", e)
        raise


def fetch_devices(company_id):
    """
    Fetch all devices for a specific company and determine their status.
    A device is online if it has a recent reading (within the last 2 minutes).
    
    Args:
        company_id (int): The ID of the company to fetch devices for.
    Returns:
        List of dictionaries containing device IDs, names, and statuses.
    """
    query = """
        SELECT d.id, d.name, 
               CASE 
                   WHEN MAX(r.timestamp) > NOW() - INTERVAL '2 minutes' THEN 'online'
                   ELSE 'offline'
               END AS status
        FROM devices d
        LEFT JOIN device_readings r ON d.id = r.device_id
        WHERE d.company_id = %s
        GROUP BY d.id
    """

    try:
        with get_connection() as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, (company_id,))
            devices = cursor.fetchall()
            return [
                {"id": row["id"], "name": row["name"], "status": row["status"]}
                for row in devices
            ]
    except psycopg2.Error as e:
        logger.error("Error fetching devices for company_id %s: %s", company_id, e)
        raise


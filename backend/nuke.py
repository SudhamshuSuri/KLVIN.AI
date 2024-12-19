import psycopg2
from psycopg2 import sql

def nuke_and_update():
    # Database connection details
    db_config = {
        'dbname': 'device_status',
        'user': 'postgres',
        'password': 'your_password',
        'host': 'localhost',
        'port': 5432
    }

    # New values to insert
    new_values = [
        (1, 'Company A', 'New Info A'),
        (2, 'Company B', 'New Info B')
    ]

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Begin transaction
        conn.autocommit = False

        # Delete old duplicates
        delete_query = """
        DELETE FROM companies
        WHERE id IN (
            SELECT id
            FROM (
                SELECT id, ROW_NUMBER() OVER (PARTITION BY name ORDER BY id DESC) AS row_num
                FROM companies
            ) subquery
            WHERE row_num > 1
        );
        """
        cur.execute(delete_query)

        # Insert new values
        insert_query = sql.SQL("""
            INSERT INTO companies (id, name, info)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name, info = EXCLUDED.info;
        """)

        cur.executemany(insert_query, new_values)

        # Commit changes
        conn.commit()
        print("Old duplicates removed and new values inserted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    nuke_and_update()


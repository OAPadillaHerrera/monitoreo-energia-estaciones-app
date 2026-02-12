

from config.db import conectar_db


def insert_system_events(records):

    if not records:
        return

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        INSERT INTO system_events (
            timestamp,
            system_id,
            event_type
        )
        VALUES (%s, %s, %s)
    """

    cursor.executemany(query, records)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(records)} system events inserted successfully")

def get_latest_system_event_date():

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        SELECT MAX(DATE(timestamp))
        FROM system_events;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0]:
        return result[0]

    return None

def exists_system_event_in_month(year: int, month: int, event_type: str):

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        SELECT 1
        FROM system_events
        WHERE event_type = %s
          AND EXTRACT(YEAR FROM timestamp) = %s
          AND EXTRACT(MONTH FROM timestamp) = %s
        LIMIT 1;
    """

    cursor.execute(query, (event_type, year, month))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


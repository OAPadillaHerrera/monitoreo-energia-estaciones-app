

from config.db import conectar_db
import datetime

def insert_hourly_consumption(records):

    if not records:
        return

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        INSERT INTO hourly_consumption (
        system_id,
        timestamp, 
        consumption_kwh
        )
        VALUES (%s, %s, %s)
    """   

    cursor.executemany(query, records)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(records)} hourly records inserted succesfully")

def exists_hourly_consumption_for_date(date):

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        SELECT 1
        FROM hourly_consumption
        WHERE DATE(timestamp) = %s
        LIMIT 1;
    """

    cursor.execute(query, (date,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None




from config.db import conectar_db
import io


def insert_hourly_consumption(records):

    if not records:
        return

    connection = conectar_db()
    cursor = connection.cursor()

    buffer = io.StringIO()

    for system_id, timestamp, consumption in records:
        buffer.write(f"{system_id},{timestamp},{consumption}\n")

    buffer.seek(0)

    cursor.execute("""
        COPY hourly_consumption (system_id, timestamp, consumption_kwh)
        FROM STDIN WITH (FORMAT CSV)
    """, stream=buffer)

    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(records)} hourly records inserted via COPY")

def get_latest_consumption_date():

    connection = conectar_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT MAX(DATE(timestamp))
        FROM hourly_consumption;
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0]:
        return result[0]

    return None


from config.db import conectar_db

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


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

def get_latest_consumption_date():

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        SELECT MAX(DATE(timestamp))
        FROM hourly_consumption;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result and result[0]:
        return result[0]

    return None

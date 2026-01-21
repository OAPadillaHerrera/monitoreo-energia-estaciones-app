

from config.db import conectar_db

def insert_daily_consumption(records):

    if not records:
        return
    
    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        INSERT INTO daily_consumption (
            system_id,
            date,
            total_consumption_kwh
        )
        VALUES (%s, %s, %s)
    """

    cursor.executemany(query, records)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(records)} daily records inserted successfully") 


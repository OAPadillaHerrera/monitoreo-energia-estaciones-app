

from config.db import conectar_db


def insert_hourly_voltage_bulk(records):
    if not records:
        return

    connection = conectar_db()
    cursor = connection.cursor()

    query = """
        INSERT INTO hourly_voltage_profile (
            timestamp,
            voltage_120v,
            voltage_240v,
            quality_flag
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.executemany(query, records)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(records)} voltage records inserted successfully")




from config.db import conectar_db

def insert_hourly_voltage(timestamp, voltage_120v, voltage_240v, quality_flag="normal"):
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

    cursor.execute(query, (
        timestamp,
        voltage_120v,
        voltage_240v,
        quality_flag
    ))

    connection.commit()

    cursor.close()
    connection.close()


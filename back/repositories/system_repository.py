

from config.db import conectar_db

def get_systems_map():

    connection = conectar_db()
    cursor = connection.cursor()

    query = "SELECT id, name FROM systems;"
    cursor.execute(query)

    systems = cursor.fetchall()

    cursor.close()
    connection.close()

    return {name: system_id for system_id, name in systems}



    
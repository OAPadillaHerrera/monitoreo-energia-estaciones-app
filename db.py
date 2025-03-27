

import pg8000

def conectar_db ():

    try:

        conexion = pg8000.connect (

            host="localhost",  
            database="monitoreo",
            user="postgres",
            password="Opostgre2024"

        )

        print ("Conexión a la base de datos exitosa.")
        return conexion
    
    except Exception as error:

        print (f"Error al conectar con la base de datos: {error}")
        return None


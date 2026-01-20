

import os
import pg8000
from dotenv import load_dotenv

load_dotenv ()

def conectar_db():
    try:
        conexion = pg8000.connect (
            host=os.getenv("DB_HOST"), 
            database=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASSWORD"), 
            port=int(os.getenv("DB_PORT"), )
        )

        print("Database connection established successfully.")
        return conexion
    
    except Exception as error:

        print(f"Error connecting to the database: {error}")
        return None




from flask import Blueprint, jsonify
import random
import datetime
from db import conectar_db

simulacion_bp = Blueprint ('simulacion', __name__)

def generar_datos_simulados ():

    systems = [
        'Price Display System (LED Modules)',
        'Corporate Lighting System (LED Signage and Logo)',
        'Canopy Lighting System (27 Lamps)',
        'Perimeter Lighting System (5 Luminaires)',
        'Air Conditioning System (Office and Server Room)',
        'Customer Service Kiosk System',
        'Submersible Pump System',
        'Fuel Dispenser System (5 Units)',
        'Office and General Services System'
    ]

    datos = []

    for sistema in sistemas:

        consumo = round (random.uniform (10, 50), 2)
        fecha = datetime.datetime.now ()
        datos.append ((sistema, consumo, fecha))

    print (f"Datos generados: {datos}")
    return datos

def insertar_datos_en_db (datos):

    conexion = conectar_db ()

    if conexion:

        try:

            cursor = conexion.cursor ()
            query = "INSERT INTO consumo_energetico (sistema, consumo, fecha) VALUES (%s, %s, %s)"
            cursor.executemany (query, datos)
            conexion.commit ()
            print ("Datos insertados correctamente.")
            return True
        
        except Exception as error:

            print (f"Error al insertar datos: {error}")
            return False
        
        finally:

            cursor.close ()
            conexion.close ()

    else:

        print ("Error al conectar. No se insertaron datos.")
        return False

@simulacion_bp.route ('/')

def index ():

    return "ENERGY MONITORING SYSTEM WORKING CORRECTLY ..."

@simulacion_bp.route ('/generar-datos', methods = ['POST'])

def generar_datos ():

    datos_simulados = generar_datos_simulados () 
    exito = insertar_datos_en_db (datos_simulados)  

    if exito:

        return jsonify ({"mensaje": "Datos insertados correctamente"}), 200
    
    else:

        return jsonify ({"mensaje": "Error al insertar datos"}), 500


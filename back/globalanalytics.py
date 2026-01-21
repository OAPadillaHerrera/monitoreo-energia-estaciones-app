

from flask import Blueprint, jsonify
import requests
from db import conectar_db  
import pandas as pd

from flask import Blueprint, jsonify
import requests

totales_bp = Blueprint ('totales', __name__)  

def construir_url (endpoint):      
    
    return f"http://host.docker.internal:5001/api/consumo/{endpoint}"

@totales_bp.route ('/total_promedio', methods = ['GET'])

def total_promedio ():

    url = construir_url ('promedio')
    response = requests.get (url)
    print(f"URL construida: {url}")

    
    print (f"Response Status: {response.status_code}")
    print (f"Response Text: {response.text}") 

    try:

        response_json = response.json ()

    except requests.exceptions.JSONDecodeError as e:

        print (f"Error decodificando JSON: {str(e)}")
        return jsonify ({"error": "Error al decodificar la respuesta JSON", "response_text": response.text}), 500
    
    if response.status_code == 200:

        datos_promedio = response_json
        promedio_por_sistema = datos_promedio.get ("consumo_promedio_por_sistema", {})
        
        total_promedio_global = sum (promedio_por_sistema.values ())

        return jsonify ({

            "total_promedio_global": float (total_promedio_global),
            "promedio_por_sistema": promedio_por_sistema

        }), 200
    
    else:

        return jsonify ({"error": "No se pudo obtener los datos de promedio"}), response.status_code

@totales_bp.route ('/total_max_min', methods = ['GET'])

def total_max_min ():
  
    url = construir_url ('max_min')
    response = requests.get (url)

    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}") 

    try:
        response_json = response.json ()

    except requests.exceptions.JSONDecodeError as e:

        print (f"Error decodificando JSON: {str(e)}")
        return jsonify ({"error": "Error al decodificar la respuesta JSON", "response_text": response.text}), 500
    
    if response.status_code == 200:

        datos_max_min = response_json
        max_min_por_sistema = datos_max_min.get ("max_min_por_sistema", {})
        
        total_max_global = sum ([sistema_data ['max'] for sistema_data in max_min_por_sistema.values ()])
        total_min_global = sum ([sistema_data ['min'] for sistema_data in max_min_por_sistema.values ()])

        return jsonify ({

            "total_max_min_global": {

                "total_maximo": float (total_max_global),
                "total_minimo": float (total_min_global)
            },

            "max_min_por_sistema": max_min_por_sistema

        }), 200
    
    else:

        return jsonify ({"error": "No se pudo obtener los datos de max/min"}), response.status_code

@totales_bp.route ('/total_consumo', methods = ['GET'])

def total_consumo ():

    url = construir_url ('total')
    response = requests.get (url)
    
    print (f"Response Status: {response.status_code}")
    print (f"Response Text: {response.text}")  

    try:

        response_json = response.json ()

    except requests.exceptions.JSONDecodeError as e:

        print (f"Error decodificando JSON: {str (e)}")
        return jsonify ({"error": "Error al decodificar la respuesta JSON", "response_text": response.text}), 500
    
    if response.status_code == 200:

        datos_total = response_json
        total_por_sistema = datos_total.get ("consumo_total_por_sistema", {})
        
        total_global = sum (total_por_sistema.values ())

        return jsonify ({

            "total_global": float (total_global),
            "total_por_sistema": total_por_sistema

        }), 200
    
    else:

        return jsonify ({"error": "No se pudo obtener los datos de consumo total"}), response.status_code

@totales_bp.route ('/total_promedio_movil', methods=['GET'])

def total_promedio_movil ():
   
    url = construir_url ('promedio_movil')
    response = requests.get (url)
    
    print (f"Response Status: {response.status_code}")
    print (f"Response Text: {response.text}")  

    try:

        response_json = response.json ()

    except requests.exceptions.JSONDecodeError as e:

        print (f"Error decodificando JSON: {str(e)}")
        return jsonify ({"error": "Error al decodificar la respuesta JSON", "response_text": response.text}), 500
    
    if response.status_code == 200:

        datos_promedio_movil = response_json
        promedio_movil_por_sistema = datos_promedio_movil.get ("promedio_movil_por_sistema", {})

        promedios_movil_globales = []

        if promedio_movil_por_sistema:
          
            fecha_comun = list(promedio_movil_por_sistema.values())[0]  

            if not fecha_comun:

                return jsonify ({"error": "No hay datos válidos de promedios móviles"}), 400

            for i in range (len (fecha_comun)):

                suma_promedios_fecha = 0.0

                for sistema, promedios in promedio_movil_por_sistema.items():

                    if i < len (promedios):  

                        suma_promedios_fecha += promedios[i] 

                promedios_movil_globales.append (suma_promedios_fecha)

        else:

            return jsonify ({"error": "No se encontraron promedios móviles por sistema"}), 400
        
        response_data = {

            "promedio_movil_por_sistema": promedio_movil_por_sistema,

        }

        response_data ["promedio_movil_global"] = promedios_movil_globales
        
        return jsonify(response_data), 200
    
    else:
        return jsonify({"error": "No se pudo obtener los datos de promedio móvil"}), response.status_code

@totales_bp.route ('/suma_totales_por_fecha', methods = ['GET'])

def suma_totales_por_fecha ():

    """
    Calcula la suma total de consumos agrupados por fecha y hora desde la base de datos.
    """

    conexion = conectar_db ()

    if conexion:
        try:
          
            query = """

                SELECT 
                    DATE_TRUNC('second', fecha) AS fecha_hora,
                    SUM(consumo) AS consumo_total
                FROM consumo_energetico
                GROUP BY fecha_hora
                ORDER BY fecha_hora ASC;

            """

            df = pd.read_sql (query, conexion)

            fechas = df ['fecha_hora'].astype (str).tolist() 
            consumos = df ['consumo_total'].tolist ()  

            return jsonify ({

                "fechas": fechas,
                "consumos": consumos

            }), 200
        
        except Exception as error:

            print (f"Error al obtener datos: {error}")

            return jsonify ({"mensaje": "Error al procesar datos"}), 500
        
        finally:

            conexion.close ()

    else:

        return jsonify ({"mensaje": "Error al conectar con la base de datos"}), 500




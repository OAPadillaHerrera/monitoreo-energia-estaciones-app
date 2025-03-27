

from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from db import conectar_db

analytics_bp = Blueprint ('analytics', __name__)

def obtener_datos_filtrados (conexion):
    query = "SELECT sistema, consumo, fecha FROM consumo_energetico"
    df = pd.read_sql (query, conexion)
    return df

@analytics_bp.route ('/promedio', methods = ['GET'])

def consumo_promedio ():

    start = request.args.get ('start')
    end = request.args.get ('end')
    conexion = conectar_db ()

    if conexion:

        try:

            df = obtener_datos_filtrados (conexion, start, end)
            df ['consumo'] = pd.to_numeric (df ['consumo'], errors = 'coerce').fillna (0) 

            promedio_por_sistema = df.groupby ('sistema')['consumo'].apply (np.mean)

            return jsonify ({

                "consumo_promedio_por_sistema": promedio_por_sistema.to_dict ()

            }), 200
        
        finally:

            conexion.close ()

@analytics_bp.route ('/max_min', methods = ['GET'])

def consumo_max_min ():

    start = request.args.get ('start')
    end = request.args.get ('end')
    conexion = conectar_db ()

    if conexion:

        try:

            df = obtener_datos_filtrados (conexion, start, end)
            df ['consumo'] = pd.to_numeric (df ['consumo'], errors = 'coerce').fillna (0)  

            max_min_por_sistema = df.groupby ('sistema') ['consumo'].agg (max = np.max, min = np.min)

            return jsonify ({

                "max_min_por_sistema": max_min_por_sistema.to_dict (orient='index')

            }), 200
        
        finally:

            conexion.close ()

@analytics_bp.route ('/total', methods = ['GET'])

def consumo_total ():

    start = request.args.get ('start')
    end = request.args.get ('end')
    conexion = conectar_db ()

    if conexion:

        try:

            df = obtener_datos_filtrados (conexion, start, end)            
            df ['consumo'] = pd.to_numeric (df ['consumo'], errors = 'coerce').fillna (0) 

            total_por_sistema = df.groupby ('sistema')['consumo'].apply (np.sum)

            return jsonify ({

                "consumo_total_por_sistema": total_por_sistema.to_dict ()

            }), 200
        
        finally:

            conexion.close ()

@analytics_bp.route ('/picos', methods = ['GET'])

def deteccion_picos ():

    start = request.args.get ('start')
    end = request.args.get ('end')
    conexion = conectar_db ()

    if conexion:

        try:

            df = obtener_datos_filtrados (conexion, start, end)
            df ['consumo'] = pd.to_numeric (df ['consumo'], errors = 'coerce').fillna (0)  

            picos_por_sistema = {}

            for sistema, datos in df.groupby ('sistema'):

                umbral = np.percentile (datos ['consumo'], 95)

                picos_por_sistema [sistema] = datos [datos ['consumo'] > umbral].to_dict (orient='records')

            return jsonify ({

                "picos_por_sistema": picos_por_sistema

            }), 200
        
        finally:

            conexion.close ()

@analytics_bp.route ('/promedio_movil', methods = ['GET'])

def promedio_movil ():

    start = request.args.get ('start')
    end = request.args.get ('end')
    conexion = conectar_db ()

    if conexion:

        try:
            
            df = obtener_datos_filtrados(conexion, start, end)         
            df ['fecha'] = pd.to_datetime (df ['fecha'])
            df.set_index ('fecha', inplace = True)
            df = df.sort_index ()  
            
            promedio_movil_por_sistema = {}
           
            for sistema, grupo in df.groupby ('sistema'):
                promedio_movil = grupo ['consumo'].rolling ('24H').mean ().dropna ()
                promedio_movil_por_sistema[sistema] = promedio_movil.tolist()

            return jsonify ({

                "promedio_movil_por_sistema": promedio_movil_por_sistema

            }), 200
        
        finally:

            conexion.close ()

@analytics_bp.route ('/sistema', methods = ['GET'])

def consumo_por_sistema ():

    conexion = conectar_db ()

    if conexion:

        try:
          
            query = """

                SELECT sistema, consumo, fecha
                FROM consumo_energetico
                ORDER BY fecha ASC;

            """

            df = pd.read_sql (query, conexion)          
            datos_por_sistema = {}

            for sistema, grupo in df.groupby ('sistema'):

                datos_por_sistema [sistema] = {

                    "fechas": grupo ['fecha'].astype (str).tolist (), 
                    "consumos": grupo ['consumo'].tolist ()
                }

            return jsonify (datos_por_sistema), 200
        
        except Exception as error:

            print (f"Error al obtener datos: {error}")
            return jsonify ( {"mensaje": "Error al procesar datos"}), 500
        
        finally:

            conexion.close ()













        





     





















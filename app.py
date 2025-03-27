

from flask import Flask
from simulacion import simulacion_bp
from analytics import analytics_bp
from globalanalytics import totales_bp
from flask_cors import CORS

app = Flask (__name__)
CORS (app) 

app.register_blueprint (simulacion_bp, url_prefix = '/simulacion')
app.register_blueprint (analytics_bp, url_prefix = '/api/consumo')
app.register_blueprint (totales_bp, url_prefix = '/api/consumo')

@app.route ('/')

def index ():
    
    return "ENERGY MONITORING SYSTEM WORKING CORRECTLY ..."

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5001, debug=True)
   
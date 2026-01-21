

from flask import Flask
from simulation import simulation_bp
from analytics import analytics_bp
from globalanalytics import totales_bp
from flask_cors import CORS

app = Flask (__name__)
CORS (app) 

app.register_blueprint (simulation_bp, url_prefix = '/simulation')
app.register_blueprint (analytics_bp, url_prefix = '/api/consumo')
app.register_blueprint (totales_bp, url_prefix = '/api/totales')

@app.route ('/')

def index ():
    
    return "ENERGY MONITORING SYSTEM WORKING CORRECTLY ..."

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5001, debug=True)
   
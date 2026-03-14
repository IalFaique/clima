import requests
import csv
import os
from datetime import datetime, timedelta, timezone

# --- CONFIGURACIÓN ---
API_KEY = "ad5b14cb501e5b275644b0306de2bf97" 
LAT = "-5.4058"
LON = "-79.6133"
ARCHIVO_LOG = "historial_clima.csv"

def revisar_clima():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&lang=es&units=metric"
    respuesta = requests.get(url)
    datos = respuesta.json()
    
    if respuesta.status_code == 200:
        descripcion = datos['weather'][0]['description'].capitalize()
        temp = datos['main']['temp']
        humedad = datos['main']['humidity']
        
        # Ajustamos a la zona horaria de Perú (UTC -5)
        hora_peru = datetime.now(timezone.utc) - timedelta(hours=5)
        fecha_actual = hora_peru.strftime('%Y-%m-%d')
        hora_actual = hora_peru.strftime('%H:%M:%S')
        
        archivo_existe = os.path.isfile(ARCHIVO_LOG)
        with open(ARCHIVO_LOG, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            if not archivo_existe:
                escritor.writerow(["Fecha", "Hora", "Condición", "Temperatura (°C)", "Humedad (%)"])
            
            escritor.writerow([fecha_actual, hora_actual, descripcion, temp, humedad])

revisar_clima()

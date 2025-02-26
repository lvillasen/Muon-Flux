#!/usr/bin/env python3
# Last updated 26/Feb/25
import http.client
import urllib.parse
import ssl
import  smbus2
import bme280
from datetime import datetime
from periphery import MMIO
import time
import json
import os
import csv
def enviar_datos( ):
    global Rates
    result = os.popen("bash /root/Muon-Flux/Temperature.sh").read().strip()
    temperature = float(result)
    port = 0
    #address = 0x77
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    dataPTH = bme280.sample(bus, address, calibration_params)
    P=round(dataPTH.pressure,2)
    T=round(dataPTH.temperature,2)
    H=round(dataPTH.humidity,2)
    regset = MMIO(0x41210000, 0xc)
    NUM_SINGLES = regset.read32(8) % (256*256)
    NUM_DOUBLES = int(regset.read32(8) / (256*256))
    regset.close()
    if (NUM_SINGLES < NumSinglesLast):
        deltaS = NUM_SINGLES-NumSinglesLast + 2**16
    else:
        deltaS = NUM_SINGLES-NumSinglesLast

    if (NUM_DOUBLES < NumDoublesLast):
        deltaD = NUM_DOUBLES-NumDoublesLast + 2**16
    else:
        deltaD = NUM_DOUBLES-NumDoublesLast

    Rates["NumSinglesLast"]=NUM_SINGLES
    Rates["NumDoublesLast"]=NUM_DOUBLES
    save_Rates(Rates)
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    ssl_context = ssl._create_unverified_context()
    data = {
        'date_time': formatted_time,
        'r1': deltaS,
        'r2': deltaD,
        'P': P,
        'T': T,
        'H': H,
        'temperature': temperature
    }
    fieldnames = ['date_time', 'deltaR1','deltaR2','R1', 'R2', 'P', 'T', 'H', 'temperature']

    data_raw = {
        'date_time': formatted_time,
        'deltaR1': deltaS,
        'deltaR2': deltaD,
        'R1': NUM_SINGLES,
        'R2': NUM_DOUBLES,
        'P': P,
        'T': T,
        'H': H,
        'temperature': temperature
    }

    file_name = "/root/Muon-Flux/Data.csv"

    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(data_raw)
    params = urllib.parse.urlencode(data)
    headers = { "Content-type": "application/x-www-form-urlencoded" }

    try:
        conn = http.client.HTTPSConnection("XXX.XXX.8.192", context=ssl_context)
        conn.request("POST", "/Muon-Flux/save_mySQL.php", params, headers)
        response = conn.getresponse()
        if response.status == 200:
            print(formatted_time,deltaS,deltaD,P,T,H)
            print(response.read().decode())  # Respuesta del servidor
        else:
            print("Error al enviar los datos a mySQL: ", response.status)
        conn.close()

    except Exception as e:
        print("Ocurrio un error:", e)

def load_Rates():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)  # Leer y convertir a un diccionario de Python
    return {"NumSinglesLast": -1, "NumDoublesLast": -1}  # Valores iniciales si el archivo no existe

def save_Rates(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file)  # Convertir a JSON y guardar


FILE_PATH = "/root/Muon-Flux/Rates.json"
Rates = load_Rates()
if Rates["NumSinglesLast"] == -1:
    regset = MMIO(0x41210000, 0xc)
    NumSingles = regset.read32(8) % (256*256)
    NumDoubles = int(regset.read32(8) / (256*256))
    regset.close()
    Rates["NumSinglesLast"]=NumSingles
    Rates["NumDoublesLast"]=NumDoubles
    save_Rates(Rates)
else:
    NumSinglesLast = Rates["NumSinglesLast"]
    NumDoublesLast = Rates["NumDoublesLast"]
    enviar_datos()

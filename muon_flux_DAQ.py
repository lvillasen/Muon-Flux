import http.client
import urllib.parse
import ssl
import  smbus2
import bme280
from datetime import datetime
from periphery import MMIO
import time

port = 0
#address = 0x77
address = 0x76
bus = smbus2.SMBus(port)
regset = MMIO(0x41210000, 0xc)
NumSinglesLast = regset.read32(8) % (256*256)
NumDoublesLast = int(regset.read32(8) / (256*256))
regset.close()
N=0
print("Iniciando la toma remota de datos ...")
print(datetime.now())
print("NumSinglesLast = ",NumSinglesLast)
print("NumDoublesLast = ",NumDoublesLast)


def enviar_datos( ):
    global NumSinglesLast
    global NumDoublesLast
    global N
    N += 1
    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    dataPTH = bme280.sample(bus, address, calibration_params)

    # the compensated_reading class has the following attributes
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
        
    
       
    NumSinglesLast = NUM_SINGLES
    NumDoublesLast = NUM_DOUBLES
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    

    # Crear contexto SSL sin verificación de certificados
    ssl_context = ssl._create_unverified_context()

    # Datos a enviar
    data = {
        'date_time': formatted_time,
        'r1': deltaS,
        'r2': deltaD,
        'p': P,
        't': T,
        'h': H
    }

    # Preparar los datos para la solicitud
    params = urllib.parse.urlencode(data)
    headers = { "Content-type": "application/x-www-form-urlencoded" }

    try:
        # Crear la conexión HTTPS
        conn = http.client.HTTPSConnection("ciiec.buap.mx", context=ssl_context)

        # Enviar la solicitud POST
        conn.request("POST", "/Muon-Flux/save_data.php", params, headers)

        # Obtener la respuesta
        response = conn.getresponse()

        # Leer y mostrar la respuesta
        if response.status == 200:
            print(N,formatted_time,deltaS,deltaD,P,T,H)
            print(response.read().decode())  # Respuesta del servidor
        else:
            print("Error al enviar los datos a mySQL: ", response.status)

        # Cerrar la conexión
        conn.close()

    except Exception as e:
        print("Ocurrió un error:", e)

while(1):
    time.sleep(5*60)
    enviar_datos()

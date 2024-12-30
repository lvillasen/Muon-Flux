import os
result = os.popen("bash /root/Muon-Flux/Temperature.sh").read().strip()
temperature = float(result)
print("La temperatura obtenida es: {}".format(temperature))
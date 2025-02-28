# pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org RPI.BME280
# i2cdetect -y -r 0
import smbus2
import bme280

port = 0
#address = 0x77
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)

# there is a handy string representation too
print(data)

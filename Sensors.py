
import os
import requests
import board
import time

import adafruit_bme680
from pms5003 import PMS5003
from dotenv import load_dotenv

load_dotenv()

class SensorData:
    def __init__(self):
        self.api_endpoint = os.getenv("API_ENDPOINT")
        self.pms5003 = PMS5003(
            device="/dev/ttyAMA0",
            baudrate=9600,
            pin_enable=22,
            pin_reset=27
        )
        i2c = board.I2c()
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, os.getenv("I2C_ADDR"))
        self.bme680.sea_level_pressure = 1002.25


    def readPms(self):
        pmsData = self.pms5003.read()

        pm1_0 = pmsData.pm_ug_per_m3(1.0)
        pm2_5 = pmsData.pm_ug_per_m3(2.5)
        pm10 = pmsData.pm_ug_per_m3(10)
        
        data = {
            "PM1_0": pm1_0,
            "PM2_5": pm2_5,
            "PM10": pm10
        }

        return data

    def sendPms(self, data):
        endpoint = self.api_endpoint + "/pms5003"

        response = requests.post(url=endpoint, data=data)
        return response.status_code
        
	def readBme(self, num_readings=5, delay=2):
        temp, humidity, pressure, altitude = 0.0, 0.0, 0.0, 0.0

        for _ in range(num_readings):
            temp = "%0.1f" % self.bme680.temperature
            humidity = "%0.1f" % self.bme680.relative_humidity
            pressure = "%0.3f" % self.bme680.pressure
            altitude = "%0.2f" % self.bme680.altitude
            time.sleep(delay)

        data = {
            'Temperature': temp,
            'Pressure': pressure,
            'Humidity': humidity,
            'Altitude': altitude
        }

        return data 

    def sendBme(self, data):
		endpoint = self.api_endpoint + "/bme680"

		response = requests.post(url=endpoint, data=data)
		return response.status_code


sensor_data = SensorData()

pms_data = sensor_data.readPms()
sensor_data.sendPms(pms_data)

bme_data = sensor_data.readBme()
sensor_data.sendBme(bme_data)

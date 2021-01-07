# -----------------------------------
#     MQTT PUBLISHER DEMO 
# -----------------------------------
from servicios.weblogging import Applogging
from static.constantes import TEMP_PIN, VENTILADOR_PIN
import paho.mqtt.publish as publish
import json
import smbus
import servicios.dht_sensor
import subprocess
import dht_config
import os
import RPi.GPIO as GPIO
import time
import dht_sesn

GPIO.setmode(GPIO.BCM)
GPIO_sensor = TEMP_PIN


topic = "deustoLab/temperatura"
HOSTNAME = "test.mosquitto.org"
bus = smbus.SMBus(1)
MMA7660FC_DEFAULT_ADDRESS           = 0x4C


##CLASE TEMPERATURA


class Temperatura():
    def __init__(self):
        self.medir_temperatura()
        self.encender_ventilador()
        self.__pin_ventilador = VENTILADOR_PIN
        self.__rpi_log = Applogging("RPI")


    def medir_temperatura(self):
        sensor = dht_config.DHT(GPIO_sensor)
        temperatura = sensor.read()
        return temperatura

    def encender_ventilador(self):
        try:
            GPIO.output(self.__pin_ventilador, GPIO.HIGH)
            time.sleep(4)
            GPIO.output(self.__pin_ventilador, GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se ha podido iniciar")    

    
    def crear_json(self, tmp): 
        print("JSON creado")

        mensaje = {
            "Temperatura": tmp
        }     
        mensaje_json = json.dumps(mensaje)
        if (publish.single("deustoLab/temperatura", mensaje_json, hostname=HOSTNAME)):
            print("Done")
        else:
            print("Datos no publicados")    

    




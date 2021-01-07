
SIMULACION = False

import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()
    SIMULACION = True

import json
import subprocess
import os
import time
import threading
import atexit
from servicios.mqtt import Mqtt
from servicios.weblogging import Applogging
from comun.singleton import Singleton
from static.constantes import (
    TOPIC_ACELEROMETRO, 
    HOSTNAME_SIMULACION_LOCAL,
    HOSTNAME_RPI_1)

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class ClienteRPI1:

    __metaclass__= Singleton

    def __init__(self, nombre_log):
        self.__cliente_log = Applogging(nombre_log)
        self.__hilo_datalock = threading.Lock()
        self.__hilo_cliente_rpi = threading.Thread()
        self.__comenzar_servicio_background()
            
    def __comenzar_servicio_background(self):
        global SIMULACION
        if (SIMULACION == False):
            self.client = mqtt.Client()
            self.__cliente_log.info_log(f"Configuracion client rpi1 {TOPIC_ACELEROMETRO}:{HOSTNAME_SIMULACION_LOCAL}")
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.connect(HOSTNAME_SIMULACION_LOCAL, 1883, 60)
        self.__hilo_cliente_rpi = threading.Timer(0, self.__obtener_datos_cliente_mqtt, ())
        self.__cliente_log.info_log("Servicio cliente mqtt 1 en el background...")
        self.__hilo_cliente_rpi.start()

    def __obtener_datos_cliente_mqtt(self):
        self.__hilo_cliente_rpi = threading.Timer(0.1, self.__obtener_datos_cliente_mqtt, ())
        if (SIMULACION == False):   
            self.client.loop_forever()
        with self.__hilo_datalock:
            self.__hilo_cliente_rpi.start()
    
    def _on_connect(self, client, serdata, flags, rc):
            global TOPIC_ACELEROMETRO
            self.__cliente_log.info_log("Conectado como cliente mqtt, con codigo: " + str(rc))
            client.subscribe(TOPIC_ACELEROMETRO)

    def _on_message(self, client, userdata, msg):
            msg.payload = msg.payload.decode("utf-8")
            mensaje_recibido = msg.payload
            self.__cliente_log.info_log(msg.topic + " "+ mensaje_recibido)
            mensaje_recibido_json = json.loads(msg.payload )
    
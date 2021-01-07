DEBUG = False

import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()
    DEBUG = True

import json
import subprocess
import os
from datetime import datetime
import threading
import atexit
from servicios.weblogging import Applogging
from comun.singleton import Singleton
from modelos.medicionAccelerometro import MAcelerometro
from static.constantes import (
    TOPIC_ACELEROMETRO, 
    HOSTNAME_SIMULACION_LOCAL,
    HOSTNAME_RPI_1)

class ClienteRPI1:

    __metaclass__= Singleton

    def __init__(self, nombre_log, servicio_db):
        self.__cliente_log = Applogging(nombre_log)
        self.__servicio_db = servicio_db
        self.__sesion = servicio_db.sesion
        self.__hilo_datalock = threading.Lock()
        self.__hilo_cliente_rpi = threading.Thread()
        self.__comenzar_servicio_background()
            
    def __comenzar_servicio_background(self):
        global DEBUG
        if (DEBUG == False):
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
        if (DEBUG == False):   
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
        mensaje_recibido_json = json.loads(msg.payload)
        varx = mensaje_recibido_json["varx"]
        vary = mensaje_recibido_json["vary"]
        varz = mensaje_recibido_json["varz"]
        self.__insert_medicion_accel(
            var_x = varx,
            var_y = vary,
            var_z = varz)

    def __insert_medicion_accel(self, var_x, var_y, var_z):
        self.__sesion = self.__servicio_db.crear_nueva_conexion_si_ha_caducado()
        fecha_actual = datetime.now()
        self.__cliente_log.info_log(fecha_actual)
        nueva_medicion = MAcelerometro(
            fecha = fecha_actual,
            eje_x = var_x,
            eje_y = var_y,
            eje_z = var_z,)
        self.__sesion.add(nueva_medicion)
        self.__sesion.commit()
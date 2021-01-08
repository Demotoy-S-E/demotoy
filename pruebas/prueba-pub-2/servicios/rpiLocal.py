import comun.excepciones as excepciones

try:
    import RPi.GPIO as GPIO
except:
    excepciones.error_gpio_import_log()

import subprocess
import os
import time
import threading
import atexit
from comun.singleton import Singleton
from servicios.weblogging import Applogging
from servicios.Temper import Temperatura
from static.constantes import (
    SECUANCIA_SEGUNDOS_RPI, 
    TEMP_PIN, 
    VENTILADOR_PIN)
from random import randrange

class RpiLocal(metaclass=Singleton):
    
    def __init__(self):
        self.__rpi_log = Applogging("RPI")
        self.__hilo_datalock = threading.Lock()
        self.__hilo_rpi = threading.Thread()
        self.__comenzar_servicio_background()
        self.__pin_temperatura = TEMP_PIN
        self.__servicio_temperatura = None
        self.valor_temperatura = None
        
    def __obtener_datos_rpi(self):
        try:
            self.__hilo_rpi = threading.Timer(SECUANCIA_SEGUNDOS_RPI, self.__obtener_datos_rpi, ())
            self.__servicio_temperatura = Temperatura()
            self.__temperatura = self.__servicio_temperatura.medir_temperatura()
            self.__servicio_temperatura.crear_json(self.__temperatura)
            print("La temperatura actual es: {0:.1f}".format(self.__temperatura))

            temp_adecuada = 21

            if self.__temperatura < temp_adecuada:
                print("Temperatura inferior a la adecuada")
                print("Activando sistema de calefacción")

            if self.__temperatura > temp_adecuada:
                print("Temperatura superior a la adecuada")
                print("Activando el sistema de climatización")       
                # self.__servicio_temperatura.encender_ventilador()
            GPIO.cleanup()

        except:
            self.__rpi_log.error_log("No se ha podido obtener datos de la rpi")
            self.__servicio_temperatura = Temperatura()
            self.__temperatura = self.devolver_datos_fake()
        with self.__hilo_datalock:
            self.__hilo_rpi.start()

    def __comenzar_servicio_background(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__pin_temperatura, GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se han podido configurar las salidas GPIO")
        self.__hilo_rpi = threading.Timer(0, self.__obtener_datos_rpi, ())
        self.__rpi_log.info_log("Servicio RPI comenzando en background")
        self.__hilo_rpi.start()

    def devolver_datos_fake(self):
        temp = randrange(25)
        return {'Temperatura' : temp}
    

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
from static.constantes import SECUANCIA_SEGUNDOS_RPI, CALOR_PIN

class RpiLocal(metaclass=Singleton):
    
    def __init__(self):
        self.__rpi_log = Applogging("RPI")
        self.__hilo_datalock = threading.Lock()
        self.__hilo_rpi = threading.Thread()
        self.__pin_acelerometro = CALOR_PIN
        self.__comenzar_servicio_background()

    def __obtener_datos_rpi(self):
        try:
            self.__hilo_rpi = threading.Timer(SECUANCIA_SEGUNDOS_RPI, self.__obtener_datos_rpi, ())

            """ Acelerometro """

        except:
            self.__rpi_log.error_log("No se ha podido obtener datos de la rpi")
        with self.__hilo_datalock:
            self.__hilo_rpi.start()

    def __comenzar_servicio_background(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__pin_acelerometro, GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se han podido configurar las salidas GPIO")
        self.__hilo_rpi = threading.Timer(0, self.__obtener_datos_rpi, ())
        self.__rpi_log.info_log("Servicio RPI comenzando en background")
        self.__hilo_rpi.start()

    
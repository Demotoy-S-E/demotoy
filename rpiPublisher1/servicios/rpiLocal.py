
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
        self.__pin_calor = CALOR_PIN
        self.__comenzar_servicio_background()

    def encender_calor(self):
        try:
            GPIO.output(self.__pin_calor, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.__pin_calor, GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se ha podido calentar")

    def __obtener_datos_rpi(self):
        try:
            self.__hilo_rpi = threading.Timer(SECUANCIA_SEGUNDOS_RPI, self.__obtener_datos_rpi, ())
            self.__medir_temperatura_interna()
            if (self.temperatura_cpu > 40 and self.parpadear == True):
                self.__parpadear_led()
            else:
                self.__dejar_parpadear() 
        except:
            self.__rpi_log.error_log("No se ha podido obtener datos de la rpi")
        with self.__hilo_datalock:
            self.__hilo_rpi.start()

    def __comenzar_servicio_background(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__pin_buzzer,GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se han podido configurar las salidas GPIO")
        self.__hilo_rpi = threading.Timer(0, self.__obtener_datos_rpi, ())
        self.__rpi_log.info_log("Servicio RPI comenzando en background")
        self.__hilo_rpi.start()

    
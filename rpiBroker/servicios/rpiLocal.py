
import comun.excepciones as excepciones
try:
    import RPi.GPIO as GPIO
    import smbus2
except:
    excepciones.error_gpio_import_log()

import subprocess
import os
import time
import threading
import atexit
from comun.singleton import Singleton
from servicios.weblogging import Applogging
from static.constantes import SECUANCIA_SEGUNDOS_RPI, BUZZER_PIN

class RpiLocal(metaclass=Singleton):
    
    def __init__(self):
        self.__rpi_log = Applogging("RPI")
        self.__hilo_datalock = threading.Lock()
        self.__hilo_rpi = threading.Thread()
        self.__pin_buzzer = BUZZER_PIN
        self.temperatura_cpu = None
        self.parpadear = True
        self.__comenzar_servicio_background()

    def pitar_buzzer(self):
        try:
            GPIO.output(self.__pin_buzzer, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.__pin_buzzer, GPIO.OUT)
        except:
            self.__rpi_log.error_log("No se ha podido pitar")

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

    def __medir_temperatura_interna(self):
        cpu = subprocess.check_output('sudo cat /sys/class/thermal/thermal_zone0/temp', shell=True)
        self.temperatura_cpu = int(cpu)/1000       # Se divide en en 1000 por que muestra decimales, ej; 48320
        self.__rpi_log.info_log(f"Temperatura CPU: {self.temperatura_cpu}")

    def __parpadear_led(self):
        os.system('modprobe ledtrig_heartbeat')
        resultado = os.system('echo heartbeat >/sys/class/leds/led0/trigger')
        return resultado

    def __dejar_parpadear(self): 
        os.system('echo 0 >/sys/class/leds/led0/brightness')
        self.__rpi_log.info_log("Dejando de parpadear")
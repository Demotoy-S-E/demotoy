import subprocess
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

def medir_temperatura():
 cpu = subprocess.check_output('sudo cat /sys/class/thermal/thermal_zone0/temp', shell=True)
 cpu_c = int(cpu)/1000
 print(cpu_c)
 time.sleep(1)
 return cpu_c


#Un bucle que analice la temperatura
while True:
    #Estado inicial del LED : apagado
    temp = medir_temperatura()
    GPIO.output(18,GPIO.LOW)
    if (temp>28):
        #Encendemos el LED
        GPIO.output(18,GPIO.HIGH)
        print("Temperatura superior al umbral establecido")

    else:
        GPIO.output(18,GPIO.LOW)
        #print("Temperatura normal")
GPIO.cleanup()
import subprocess
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

def medir_temperatura():
 cpu = subprocess.check_output('sudo cat /sys/class/thermal/thermal_zone0/temp', shell=True)
 #convertimos a entero, y divimos entre 1000 para tener grados centígrados
 cpu_c = int(cpu)/1000
 return cpu_c


#Obtenemos la temperatura inicial de la CPU mediante un comando de la shell
cpu_c = medir_temperatura()
print(cpu_c)


#Un bucle que analice la temperatura
#Inicialmente, apagamos el led interno de la RPi
os.system('echo 0 >/sys/class/leds/led0/brightness')
temperatura_umbral = 47


while 1:
    while cpu_c < temperatura_umbral:
            cpu_c = medir_temperatura()
            time.sleep(1)
            print("Temperatura inferior al umbral establecido")
            print(cpu_c)

    print("Arrancar el parpadeo")
    os.system('modprobe ledtrig_heartbeat')
    os.system('echo heartbeat >/sys/class/leds/led0/trigger')
    cpu_c = medir_temperatura()
    print(cpu_c)
    
    while cpu_c > temperatura_umbral:
        cpu_c = medir_temperatura()
        time.sleep(1)
        print("MAYOR que el valor umbral")
        print(cpu_c)

    os.system('echo 0 >/sys/class/leds/led0/brightness')
    time.sleep(2)
    print("Parar el parpadeo")
    cpu_c = medir_temperatura()

GPIO.cleanup()
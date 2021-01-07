class Acelerometro():
    def __init__(self):
        self.mode_config()
        self.sample_rate_config()
    
    #Función para configurar el sensor antes de proceder a las medidas
    def mode_config(self):
        """Select the mode control register of the accelerometer from the given provided values"""
        MODE_CONTROL = (MMA7660FC_MODE_ACTIVE | MMA7660FC_AWE_DS | MMA7660FC_ASE_DS | MMA7660FC_SCPS_1 | MMA7660FC_IAH_LOW)
        bus.write_byte_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_MODE, MODE_CONTROL)
        
    #Función para configurar el registro de interrupciones
    def interrupt_config(self):
        bus.write_byte_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_INTSU, 0xE7)
    
    #Función para configurar el número de muestras por segundo
    def sample_rate_config(self):
        SAMPLE_RATE = (MMA7660FC_AMSR_2)
        bus.write_byte_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_SR, SAMPLE_RATE)
    

    #Función para leer los valores de x,y,z del sensor
    #Parámetros de la función bus.read_i2c_block_data
        #  direcicón I2C del dispositivo (MMA7660FC_DEFAULT_ADDRESS)
        #  donde se comienza a leer (MMA7660FC_XOUT)
        #  cuantos bytes se quiren leer (3)
    def read_accl(self):
        data = bus.read_i2c_block_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_XOUT, 3)
        
        # Se conveirten los datos a 6 bits, porque la trama leída completa son 8 bits, y los dos primeros
        # bits más significativos son de configuración. Los bits de la aceleracion son los bits 6-0
        xAccl = data[0] & 0x3F
        if xAccl > 31 :
            xAccl -= 64
        
        yAccl = data[1] & 0x3F
        if yAccl > 31 :
            yAccl -= 64
        
        zAccl = data[2] & 0x3F
        if zAccl > 31 :
            zAccl -= 64
        
        return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}



  #Función para leer los bits correspondientes a la orentación del sensor
    #Parámetros de la función bus.read_i2c_block_data
        #  direcicón I2C del dispositivo (MMA7660FC_DEFAULT_ADDRESS)
        #  donde se comienza a leer (MMA7660FC_TILT) -- que es 0x03
        #  cuantos bytes se quiren leer (1)
    def read_orientation(self):
        """Leer datos desde la posicion 0x03, 1 byte """
        data = bus.read_i2c_block_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_TILT, 1)
        
        PoLa = data[0] & 0x1C
        
        if PoLa == 0x00:
            print("Orientacion desconocida")
            orientation = 0 #Desconocido
        elif PoLa == 0x04:
            print("Orientacion izquierda")
            orientation = 1  #Izquierda: Dispositivo esta en modo paisaje hacia la izquierda
        elif PoLa == 0x08:
            print("Orientacion derecha")
            orientation = 2  #Derecha: Dispositivo esta en modo paisaje hacia la derecha
        elif PoLa == 0x14:
            print("Orientacion abajo")
            orientation = 3 # Abajo: Dispositivo está en posición vertical invertida
        elif PoLa == 0x18:
            print("Orientacion arriba")
            orientation = 4 # Arriba: Dispositivo está en posición vertical normal
        else:
            orientation = 0x00
        return orientation    


 # ---------------------- TO DO ----------------
# Actividad Parte 2 - E
    def read_shake(self):
        data = bus.read_i2c_block_data(MMA7660FC_DEFAULT_ADDRESS,MMA7660FC_TILT,1)

        shake = data[0] & 0x80

        if shake == 0x00:
            print("No shake")
        else:
            print("Shake")

 # ---------------------- TO DO ----------------
# Actividad Parte 2 - G
    def contar_pasos(self, eje_x, eje_y, eje_z):
        mag = math.sqrt((eje_x**2) + (eje_y**2) + (eje_z**2))  
        pasos = 0
        if (mag > 30):
            return True
        else:
            return False

 # ------------INICIALIZACIÓN Y CONFIGURACIÓN DEL SENSOR ----------------
mma7660fc = Acelerometro()
mma7660fc.mode_config()
time.sleep(0.1)
mma7660fc.sample_rate_config()
time.sleep(0.1)
mma7660fc.interrupt_config()
time.sleep(0.1)
 # -------------------------------

def crear_envar_json():
    print("Creado json")
    accl = mma7660fc.read_accl()
    eje_x = accl['x']
    eje_y = accl['y']
    eje_z = accl['z']
    mensaje= {
      "varx": eje_x,
      "vary": eje_y,
      "varz": eje_z
    }
    mensaje_json= json.dumps(mensaje)
    if (publish.single("deustoLab/aceleracion", mensaje_json, hostname=HOSTNAME)):
        print("Done")
    else:
        print("Datos no publicados")



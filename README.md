# demotoy
## Vision general
![Alt text](docs/propuesta-proyecto-SE.jpg?raw=true "propuesta-proyecto-SE")
## Requisitos (28/12/20)
```
click==7.1.2 
fernet==1.0.1  // instalar
Flask==1.1.2 // instalar
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
mysql-connector==2.2.9 // instalar
mysqlclient==2.0.2 // instalar
pyaes==1.6.1 // instalar
PyMySQL==0.10.1 // instalar
six==1.15.0
SQLAlchemy==1.3.22 // instalar
SQLAlchemy-Utils==0.36.8 // instalar
Werkzeug==1.0.1
sshtunnel==0.3.1 // instalar
```
## Servidor remoto Ubuntu-Server
El servicio en cloud para base de datos escogido es una micro maquina virtual de AWS (Amazon Web Services), que es gratuito. A esta maquina virtual se le implementado un contenedor Docker con un servidor Mysql en su interior. En la carpeta aws-docker esta toda la configuracion utilizada. Mediante un docker-compose se pone en "Up" un contenedor linux que inyecta una configuracion previa, en este caso se crea una base de datos y usuario con acceso a ella.

Para acceder al servidor remoto hace falta la clave privada que AWS te la proporciona por primera vez. Para conectarte por ssh:

```
ssh -i "[clave privada]" [usuario administrador o sudo]@[ip servidor]
```
Ejemplo:
```
ssh -i "mi-clave.pem" ubuntu_user@14-15.amazon.com
```
Dockerfile-Mysql:
```
FROM mysql

WORKDIR /etc/mysql/conf.d

# Delete configuration file from base image
RUN rm -rf /etc/mysql/conf.d/docker.cnf

# Copy custom mysql config file into config folder
COPY ./wwwroot/mysql-config.cnf ./
COPY ./wwwroot/cer/mysqlcertificate.cer /etc/ssl/certs/

# RUN echo "listen_addresses='*'"

# RUN update-ca-certificates

# We indicate to execute the program in the executable of the project
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 3306 33060
CMD ["mysqld"]
```

Docker-compose:
```
version: '2'
services:
    mysql:
      image: mysql-image-service
      container_name: mysql-service
      ports:
         - "127.0.0.1:3306:3306/tcp"
      environment:
        MYSQL_ROOT_PASSWORD: rootpassword
        MYSQL_DATABASE: domotoyawsdatabase
        MYSQL_USER: domotoystgsvr
        MYSQL_PASSWORD: ySyd,r6Y1h:jNw6
      volumes:
        - db_data:/var/lib/mysql-db

volumes:
  db_data:
```

Configuracion Myswl:
```
[mysqld]
skip-host-cache
skip-name-resolve

bind-address=0.0.0.0
```
## Servicios

### Inyeccion de dependencias (startup.py)
Es el punto de inicio de la aplicacion. Se definen los objetos que se van a instanciar, todos los servicios:

```
def __inyeccion_dependencias(self):
        self.__log_startup.info_log("Iniciando instacias de la aplicacion")
        self.__add_servicio_db()
        self.__add_servicio_autenticacion()
        self.__add_servicio_cliente_rpi1()
        self.__add_servicio_cliente_rpi2()
        self.__add_controller_principal()
```
#### Clase Singleton
```
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
```

La clase Singleton se utiliza para ser heredada (padre) de aquellos servicios donde sólo queramos una solo instacia del objeto. Para que otras clases lo hereden:
```
class Autenticacion(metaclass=Singleton):
    ...
```
Una vez que se hace la instacia ```x = Autenticacion()```, aun que después haya otra instacia ```y = Autenticacion()```; ```x == y``` ya que ```y``` recogerá la instacia ya creada ```x```.

```
x = Autenticacion()
y = Autenticacion()
if (x == y):
    print("True")
    # True
```

### Servicio Mysql con AWS-Docker

Se ha optado por utilizar una ORM (sqlalchemy) que se encarge que utilizar por debajo el lenguaje sql. De esa manera conseguimos los siguientes beneficios:
 - No tenemos que crear statements sqls y organizarlos.
 - No tenemos que preocuparnos de la sincronizacion de los modelos y las tablas, de eso se encarga la ORM.
 - La libreria se encarga de migrar aquellos cambios de la logica de datos de manera automatica, él crea las tablas.
 - Añade seguridad a las conexiones por que no manipulamos directamente lenguaje sql.

El servicio mysqlDB.py utiliza un paquete externo llamda ```sshtunnel``` que incorpora objetos dedicados a conexiones ssh. Primero de todo se obtiene las credenciales de autenticacion y la clave privada para hacer el tunel.

```
server = SSHTunnelForwarder(
            (self.__ip_host , 22),
            ssh_username='ubuntu',
            ssh_pkey='domotoy-key.pem',
            remote_bind_address=(self.__ip_local_con_ssh, int(self.__puerto_host)),
            )  
            self.__mysql_log.info_log(f"Utilizando la direccion remota {self.__ip_host}:22 con IP host servidor {self.__ip_local_con_ssh}:{self.__puerto_host}")
            return server
```
Una vez que se ha hecho el tunel, la direccion meadiante una cadena de conexion que apunta a 127.0.0.1:[Puerto utilizado para ese proceso] se puede acceder al contenedor Docker del servidor ubuntu.

Para la conexion con la base de datos:
```
    def __crear_conexion(self):
        self.engine.connect()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.sesion = Session()
```
Para las interacciones con la base de datos se hace medienta codigo. Para comprobar si existe usuario:
```
self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()
```
Insert de usuario:
```
self.__sesion.add(nuevo_usuario)
```

### Servicio Autenticacion
Mediante el servicio se crean usuarios:
```
    def crear_usuario(self, nombre_form, email_form, contrasenia_form) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()):
                self.__autenticacion_log.warning_log(f"El usuario con nombre {nombre_form} ya existe")
                return False
            else:
                nuevo_usuario = Usuario(nombre_form, email_form, contrasenia_form)
                self.__sesion.add(nuevo_usuario)
                self.__sesion.commit()
                return True
        except:
            self.__autenticacion_log.error_log("Ha habido un problema para crear usuario")
            return False
```
Se comprueban sus credenciales para la autenticacion:
```
    def comprobar_autenticacion(self, nombre_form, contrasenia_form) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()):
                usuario = self.__sesion.query(Usuario).filter_by(nombre = nombre_form).first()
                self.__sesion.commit()
                if (usuario.get_contrasenia() != contrasenia_form):
                    self.__autenticacion_log.warning_log(
                        f"El usuario con nombre {nombre_form} existe pero las credenciales no son correctas")
                    return self.usuario_autenticado
                elif (usuario.get_contrasenia() == contrasenia_form):
                    self.usuario_autenticado = True
                    self.__autenticacion_log.info_log("Usuario autenticado")
                    self.ultima_autenticacion = time.time()
                    return self.usuario_autenticado
            else:
                self.__autenticacion_log.warning_log(f"El usuario con nombre {nombre_form} no existe")
                return self.usuario_autenticado
        except:
            self.__autenticacion_log.error_log("Ha habido un problema con la autenticacion")
```
### Servicios Backgound (hilos)
Para los servicios que se encargan de operar con entradas y salidas de la RPi la mejor solucion es utilizar hilos de procesamiento en background. El objetivo es desprenderse de bucles que se apoderan del ciclo de la aplicación, de esa manera al hacer hilos asincronos la aplicacion puede hacer varios cosas a la vez. Se dejan que esos procesos se ejecuten en backgound y que administren esas entradas y salidas locales.

Con el metodo comenzar_servicio_backgorund() se define un metodo donde se crea un objeto que asigna un proceso especifico:
```
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
```
¿Que hara este hilo rutinariamente?
```
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
```
Cada X tiempo que le asignemos hará ese metodo en especifico, en este caso obtener datos de la RPi.
## Modelos
Para crear las tablas basados en los modelos SQLAlchemy es necesario que hereden el objeto Base:
```
class Usuario(Base):
    ...
```
Para definir los parametros (columnas) de la tabla:
```
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    nombre = Column(String(15), index = True, nullable = False)
    email = Column(EmailType)
    __clave = Column(LargeBinary(2048), nullable = False)
    __token = Column(LargeBinary(2048), nullable = False)
```

SQLAlchemy tiene objetos tipo Password para los campos de contrasenias. Pero debido a su complejidad y exceso de codigo se decidio utilizar otra solucion. Mediante las columans ``` __clave ``` y ``` __token``` se encripta la contraseña. El proceso es el siguiente;
```
self.__clave = Fernet.generate_key()
        self.__clave.decode()
        self.__token = self.__encrypt(contrasenia.encode(), self.__clave)

    def get_contrasenia(self):
        contrasenia_desencriptada = self.__decrypt(self.__token, self.__clave)
        contrasenia_desencriptada = contrasenia_desencriptada.decode("utf-8")
        return contrasenia_desencriptada

    def __encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def __decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)
```

1. Se recoge la contrseña como string.
2. Se genera una clave (bytes).
3. Se encripta un objeto tipo token mediante esa clave y la contraseña. 
4. Ambas columnas son de tipo binarios (BLOB en mysql).
5. Para obtener la contraseña a la hora de comparar credenciales, mediante la funcion get_contrasenia() se desencripta el token para obtener el string.

## Controladores

Definicion (rounting):
```
self.__app.add_url_rule('/', endpoint = 'index', view_func = Indexcontroller.as_view(
            'index', autenticacion = self.__servicio_autenticacion, index_controller_log = index_controller_log), methods = ["GET", "POST"])
```
Constructor:
```
class Indexcontroller(MethodView):

    def __init__(self, autenticacion, index_controller_log):
        self.__controlador_log = index_controller_log
        self.__autenticacion = autenticacion
```
Es necesario que herede la clase ``` MethodView ``` de Flask para hacerlos "classfull". Una vez instanciado el objeto se utilizan los metodos HTTP para las peticiones:
```
    def get(self):
        self.__autenticacion.usuario_autenticado = False
        return render_template(TEMPLATE_INDEX_CONSTANTE)
```

```
    def post(self):
        informacion_request = request.form
        usuario_form = informacion_request.get("nombre")
        contrasenia_form = informacion_request.get("contrasenia")
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__controlador_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_INDEX_CONSTANTE, feedback=feedback)
        else:
            autenticacion_aceptada = self.__autenticacion.comprobar_autenticacion(usuario_form, contrasenia_form)
            if (autenticacion_aceptada):
                return redirect(DIRECCION_PRINCIPAL_CONSTANTE)
            else:
                feedback = f"Credenciales no correctas"
                return render_template(TEMPLATE_INDEX_CONSTANTE, feedback=feedback)
```
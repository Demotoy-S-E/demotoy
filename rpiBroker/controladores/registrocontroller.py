from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView   
from static.constantes import TEMPLATE_INDEX_CONSTANTE, TEMPLATE_REGISTRO_CONSTANTE
from modelos.vista.crearModeloUsuario import CrearModeloUsuario

class Registrocontroller(MethodView):

    def __init__(self, autenticacion, registro_controller_log):
        self.__autenticacion = autenticacion
        self.__registro_log = registro_controller_log

    def get(self):
        return render_template(TEMPLATE_REGISTRO_CONSTANTE)

    def post(self):
        informacion_request = request.form
        nuevo_usuario = self.__obtener_parametros_request(informacion_request)
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__registro_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_REGISTRO_CONSTANTE, feedback=feedback)
        else:
            self.__crear_nuevo_usuario_si_no_existe(nuevo_usuario)
    
    def __obtener_parametros_request(self, informacion_request):
        nuevo_usuario = CrearModeloUsuario()
        nuevo_usuario.nombre = informacion_request.get("nombre")
        nuevo_usuario.email = informacion_request.get("email")
        nuevo_usuario.contrasenia = informacion_request.get("contrasenia")
        nuevo_usuario.nombre_completo = informacion_request.get("nombre_completo")
        nuevo_usuario.numero_telefono = informacion_request.get("numero_telefono")
        nuevo_usuario.direccion = informacion_request.get("direccion")
        return nuevo_usuario

    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos

    def __crear_nuevo_usuario_si_no_existe(self, nuevo_usuario):
        usuario_creado = self.__autenticacion.crear_usuario(nuevo_usuario)
        if (usuario_creado):
            return render_template(TEMPLATE_INDEX_CONSTANTE)
        else:
            feedback = f"El usuario {nuevo_usuario.nombre} no es correcto o ya existe"
            return render_template(TEMPLATE_REGISTRO_CONSTANTE, feedback=feedback)
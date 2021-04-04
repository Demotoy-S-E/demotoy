from flask import render_template, request, redirect
from flask.views import MethodView   
from static.constantes import (
    TEMPLATE_INDEX_CONSTANTE, 
    TEMPLATE_REGISTRO_CONSTANTE,
    DIRECCION_INDEX_CONSTANTE)
from modelos.usuario import Usuario

class Registrocontroller(MethodView):

    def __init__(self, repositorio_usuario, registro_controller_log):
        self.___repositorio_usuario = repositorio_usuario
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
            return self.__devolver_index_si_crea_usuario(nuevo_usuario)
    
    def __obtener_parametros_request(self, informacion_request) -> Usuario:
        nuevo_usuario = Usuario(
            nombre = informacion_request.get("nombre"),
            email = informacion_request.get("email"),
            contrasenia = informacion_request.get("contrasenia"),
            nombre_completo = informacion_request.get("nombre_completo"),
            numero_telefono = informacion_request.get("numero_telefono"),
            direccion = informacion_request.get("direccion")
        )
        return nuevo_usuario

    def __revisar_campos_vacios(self, informacion_request) -> list:
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos

    def __devolver_index_si_crea_usuario(self, nuevo_usuario):
        resultado = self.___repositorio_usuario.crear_usuario(nuevo_usuario)
        if (resultado.is_success):
            return redirect(DIRECCION_INDEX_CONSTANTE)
        elif (resultado.is_error):
            feedback = f"El usuario {nuevo_usuario.nombre} no es correcto o ya existe"
            return render_template(TEMPLATE_REGISTRO_CONSTANTE, feedback=feedback)
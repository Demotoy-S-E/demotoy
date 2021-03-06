from flask import render_template, request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from modelos.vista.updateModeloUsuario import UpdateModeloUsuario
from static.constantes import (
    TEMPLATE_PRINCIPAL_CONSTANTE, 
    DIRECCION_INDEX_CONSTANTE, 
    DIRECCION_PRINCIPAL_CONSTANTE)

class Principalcontroller(MethodView):

    def __init__(self, autenticacion , rpi_local, principal_controller_log, api):
        self.__servicio_autenticacion = autenticacion
        self.__principal_log = principal_controller_log
        self.__rpi_local = rpi_local
        self.__api = api

    def get(self):
        if (self.__servicio_autenticacion.usuario_autenticado == True):
            self.__rpi_local.pitar_buzzer()
            contrasenia_usuario = self.__servicio_autenticacion.usuario.get_contrasenia()
            templateData = {
                'cpu' : self.__rpi_local.temperatura_cpu,
                'usuario' : self.__servicio_autenticacion.usuario,
                'contrasenia' : contrasenia_usuario,
            }
            return render_template(TEMPLATE_PRINCIPAL_CONSTANTE, **templateData)
        else:
            return redirect(DIRECCION_INDEX_CONSTANTE)

    def post(self):
        # Proxima iteracion del servicio se apaga
        informacion_request = request.form
        modelo_actualizar_usuario = self.__obtener_parametros_modelo(informacion_request)
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__registro_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_PRINCIPAL_CONSTANTE, feedback=feedback)
        else:
            self.__api.modificar_usuario(
                id = self.__servicio_autenticacion.usuario.id, 
                modelo_actualizar_usuario = modelo_actualizar_usuario)
            return redirect(DIRECCION_PRINCIPAL_CONSTANTE)

    def __obtener_parametros_modelo(self, informacion_request) -> UpdateModeloUsuario:
        modelo_actualizar = UpdateModeloUsuario(
            nombre = informacion_request.get("nombre"),
            email = informacion_request.get("email"),
            nombre_completo = informacion_request.get("nombre_completo"),
            numero_telefono = informacion_request.get("numero_telefono"),
            direccion = informacion_request.get("direccion")
        )
        return modelo_actualizar
            
    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos
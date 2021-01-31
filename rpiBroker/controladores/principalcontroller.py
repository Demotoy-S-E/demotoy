from flask import render_template, request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
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
        nombre_form = informacion_request.get("nombre")
        email_form = informacion_request.get("email")
        nombre_completo_form = informacion_request.get("nombre_completo")
        numero_form = informacion_request.get("numero_telefono")
        direccion_form = informacion_request.get("direccion")
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__registro_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_PRINCIPAL_CONSTANTE, feedback=feedback)
        else:
            self.__api.modificar_usuario(
                id = self.__servicio_autenticacion.usuario.id, # esto no debe hacerlo
                nombre = nombre_form,
                email = email_form,
                nombre_completo = nombre_completo_form,
                numero_telefono = numero_form,
                direccion = direccion_form)
            return redirect(DIRECCION_PRINCIPAL_CONSTANTE)
            
    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos
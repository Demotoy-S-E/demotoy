from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView  
from static.constantes import (
    TEMPLATE_MONITORIZACION_CONSTANTE, 
    DIRECCION_PRINCIPAL_CONSTANTE,
    DIRECCION_INDEX_CONSTANTE)

class Monitorizacioncontroller(MethodView):

    def __init__(self, autenticacion, monitorizacion_controller_log, api):
        self.__controlador_log = monitorizacion_controller_log
        self.__autenticacion = autenticacion
        self.__api = api

    def get(self):
        if (self.__servicio_autenticacion.usuario_autenticado == True):
            contrasenia_usuario = self.__servicio_autenticacion.usuario.get_contrasenia()
            mediciones_temperatura = self.__api.obtener_ultimas_mediciones_temperatura_externa()
            mediciones_accel = self.__api.obtener_ultimas_mediciones_accel()
            templateData = {
                'mediciones_temperatura' : mediciones_temperatura,
                'mediciones_accel' : mediciones_accel,
            }
            return render_template(TEMPLATE_MONITORIZACION_CONSTANTE, **templateData)
        else:
            return redirect(DIRECCION_INDEX_CONSTANTE)
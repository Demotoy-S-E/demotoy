from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from static.constantes import TEMPLATE_PRINCIPAL_CONSTANTE, DIRECCION_INDEX_CONSTANTE

class Principalcontroller(MethodView):

    def __init__(self, autenticacion , rpi, principal_controller_log):
        self.__servicio_autenticacion = autenticacion
        self.__principal_log = principal_controller_log
        self.__rpi = rpi

    def get(self):
        if (self.__servicio_autenticacion.usuario_autenticado == True):
            self.__rpi.pitar_buzzer()
            templateData = {
                'cpu' : self.__rpi.temperatura_cpu,
                'temperatura_externa' : self.__rpi.temperatura_externa_sensor,
            }
            return render_template(TEMPLATE_PRINCIPAL_CONSTANTE, **templateData)
        else:
            return redirect(DIRECCION_INDEX_CONSTANTE)

    def post(self):
        self.__rpi.parpadear = False # Proxima iteracion del servicio se apaga
        return render_template(TEMPLATE_PRINCIPAL_CONSTANTE)

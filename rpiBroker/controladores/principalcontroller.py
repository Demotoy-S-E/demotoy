from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from static.constantes import TEMPLATE_PRINCIPAL_CONSTANTE, DIRECCION_INDEX_CONSTANTE

class Principalcontroller(MethodView):

    def __init__(self, autenticacion , rpi_local, rpi1, rpi2, principal_controller_log):
        self.__servicio_autenticacion = autenticacion
        self.__principal_log = principal_controller_log
        self.__rpi_local = rpi_local
        self.__rpi1 = rpi1
        self.__rpi2 = rpi2

    def get(self):
        if (self.__servicio_autenticacion.usuario_autenticado == True):
            self.__rpi_local.pitar_buzzer()
            templateData = {
                'cpu' : self.__rpi_local.temperatura_cpu,
                'temperatura_externa' : None,
            }
            return render_template(TEMPLATE_PRINCIPAL_CONSTANTE, **templateData)
        else:
            return redirect(DIRECCION_INDEX_CONSTANTE)

    def post(self):
        self.__rpi_local.parpadear = False # Proxima iteracion del servicio se apaga
        return render_template(TEMPLATE_PRINCIPAL_CONSTANTE)

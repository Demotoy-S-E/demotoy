from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from static.constantes import TEMPLATE_INDEX_CONSTANTE, TEMPLATE_PRINCIPAL_CONSTANTE, DIRECCION_PRINCIPAL_CONSTANTE

class Indexcontroller(MethodView):

    def __init__(self, autenticacion, index_controller_log):
        self.__controlador_log = index_controller_log
        self.__autenticacion = autenticacion

    def get(self):
        self.__autenticacion.usuario_autenticado = False
        return render_template(TEMPLATE_INDEX_CONSTANTE)

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

    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos
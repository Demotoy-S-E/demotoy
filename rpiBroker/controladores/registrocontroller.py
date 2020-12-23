from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from static.constantes import TEMPLATE_INDEX_CONSTANTE, TEMPLATE_REGISTRO_CONSTANTE

class Registrocontroller(MethodView):

    def __init__(self, autenticacion, registro_controller_log):
        self.__autenticacion = autenticacion
        self.__registro_log = registro_controller_log

    def get(self):
        return render_template(TEMPLATE_REGISTRO_CONSTANTE)

    def post(self):
        informacion_request = request.form
        nombre_form = informacion_request.get("nombre")
        email_form = informacion_request.get("email")
        contrasenia_form = informacion_request.get("contrasenia")
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__registro_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_REGISTRO_CONSTANTE, feedback=feedback)
        else:
            usuario_creado = self.__autenticacion.crear_usuario(nombre_form, email_form, contrasenia_form)
            if (usuario_creado):
                return render_template(TEMPLATE_INDEX_CONSTANTE)
            else:
                feedback = self.__registro_log.error_feeddback("El usuario no es correcto o ya existe")
                return render_template(TEMPLATE_REGISTRO_CONSTANTE)

    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos
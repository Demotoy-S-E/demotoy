from flask import render_template, request, redirect
from flask.views import MethodView   
from modelos.usuario import Usuario
from modelos.vista.comprobarModeloUsuario import ComprobarModeloUsuario
from static.constantes import TEMPLATE_INDEX_CONSTANTE, TEMPLATE_PRINCIPAL_CONSTANTE, DIRECCION_PRINCIPAL_CONSTANTE

class Indexcontroller(MethodView):

    def __init__(self, autenticacion, index_controller_log):
        self.__controlador_log = index_controller_log
        self.__autenticacion = autenticacion

    def get(self):
        self.__autenticacion.usuario_autenticado = False
        return render_template(TEMPLATE_INDEX_CONSTANTE)

    # REST siempre tiene que DEVOLVER un objeto
    def post(self):
        informacion_request = request.form
        campos_vacios = self.__revisar_campos_vacios(informacion_request)
        if (campos_vacios):
            self.__controlador_log.warning_log("Se han encontrado campos vacios")
            feedback = f"Campos vacios en {', '.join(campos_vacios)}"
            return render_template(TEMPLATE_INDEX_CONSTANTE, feedback=feedback)
        else:
            modelo_auth = self.__obtener_parametros_request(informacion_request)
            return self.__autenticar(modelo_auth)


    def __obtener_parametros_request(self, informacion_request) -> ComprobarModeloUsuario:
        auth_usuario = ComprobarModeloUsuario(
            nombre = informacion_request.get("nombre"),
            contrasenia = informacion_request.get("contrasenia"))
        return auth_usuario

    def __revisar_campos_vacios(self, informacion_request):
        campos_requeridos = []
        for k, v in informacion_request.items():
            if v == "":
                campos_requeridos.append(k)
        return campos_requeridos

    def __autenticar(self, modelo_auth):
        autenticacion_aceptada = self.__autenticacion.comprobar_autenticacion(modelo_auth)
        if (autenticacion_aceptada):
            return redirect(DIRECCION_PRINCIPAL_CONSTANTE)
        else:
            feedback = f"Credenciales no correctas"
            return render_template(TEMPLATE_INDEX_CONSTANTE, feedback=feedback)
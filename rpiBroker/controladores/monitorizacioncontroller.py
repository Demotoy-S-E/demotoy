from flask import render_template, request
from flask import request, redirect
from flask.views import MethodView  

class Monitorizacioncontroller(MethodView):

    def __init__(self, autenticacion, monitorizacion_controller_log, rpi1, rpi2):
        self.__controlador_log = monitorizacion_controller_log
        self.__autenticacion = autenticacion
        self.__rpi1 = rpi1
        self.__rpi2 = rpi2
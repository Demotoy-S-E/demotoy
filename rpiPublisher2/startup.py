from flask import _app_ctx_stack, jsonify
from servicios.weblogging import Applogging
from servicios.Temper import Temperatura

class Startup:

    def __init__(self, app):
        self.__app = app
        self.__log_startup = Applogging("Startup")
        self.__temperatura = Temperatura()


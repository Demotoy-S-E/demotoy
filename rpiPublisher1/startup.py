from flask import _app_ctx_stack, jsonify
from servicios.weblogging import Applogging
from servicios.acelerometro import Acelerometro


class Startup:

    def __init__(self, app):
        self.__app = app
        self.__log_startup = Applogging("Startup")
        self.__acelerometro = Acelerometro()

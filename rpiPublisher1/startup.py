from flask import _app_ctx_stack, jsonify
from flask_cors import CORS
from servicios.weblogging import Applogging


class Startup:

    def __init__(self, app):
        self.__app = app
        CORS(self.__app)
        self.__log_startup = Applogging("Startup")
    
from servicios.weblogging import Applogging

excepcion_import_log = Applogging("Import")

def error_gpio_import_log():
    return excepcion_import_log.error_log("Error al importar modulo GPIO")
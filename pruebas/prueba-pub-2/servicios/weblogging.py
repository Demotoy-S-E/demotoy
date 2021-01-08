from datetime import datetime

class Applogging:
    
    def __init__(self, log_type):
        self.log_type = log_type

    def info_log(self, log):
        current_date = datetime.today()
        return print(f" \033[1;32;48m [{current_date}] INFO {self.log_type}: {log}")

    def warning_log(self, log):
        current_date = datetime.today()
        return print(f" \033[1;33;48m [{current_date}] WARNING {self.log_type}: {log}")

    def error_log(self, log):
        current_date = datetime.today()
        return print(f" \033[1;31;48m [{current_date}] ERROR {self.log_type}: {log}")





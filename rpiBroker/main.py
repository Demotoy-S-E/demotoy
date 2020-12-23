from flask import Flask
from startup import Startup

app = Flask(__name__, static_url_path="/static/", static_folder="static")
x = Startup(app)
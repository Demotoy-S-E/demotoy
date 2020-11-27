from flask import Flask
from startup import Startup

app = Flask(__name__)
x = Startup(app)
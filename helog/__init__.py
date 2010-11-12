from flask import Flask
from helog.config import *

app = Flask(__name__)
app.config.from_object(__name__)

import helog.views

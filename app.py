import traceback
import os
from flask import Flask, request

from rdslm_sff_comparison.schema import schema
from rdslm_sff_comparison.utilities.utilities import get_template_text

app = Flask(__name__)

@app.route("/")
def index():
    #choice_html = get_template_text("index.html")
    #return choice_html
    return 'cgoiiii'


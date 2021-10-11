import traceback
import os
from flask import Flask, request

os.environ["DATABRICKS_ADDRESS"] = "https://adb-8937165168112498.18.azuredatabricks.net"
os.environ["DATABRICKS_API_TOKEN"] = "dapi6ab57495f863823424571a67e7f9f8e3"
os.environ["DATABRICKS_CLUSTER_ID"] = "0506-084842-girt358"
os.environ["DATABRICKS_ORG_ID"] = "8937165168112498"
os.environ["DATABRICKS_PORT"] = "15001"

os.environ["FLASK_ENV"] = "production"
os.environ["FLASK_APP"] = "app.py"

from rdslm_sff_comparison.schema import schema
from rdslm_sff_comparison.utilities.utilities import get_template_text

app = Flask(__name__)

@app.route("/")
def index():
    choice_html = get_template_text("index.html")
    return choice_html


@app.route("/schema_comparison/params")
def schema_comparison():
    parameters = request.args
    comparison_dimensions = {}

    dimensions = parameters.get("dimensions").split(",")
    if dimensions == [""]:
        dimensions = ["market", "product", "fact", "period", "data"]
    for dim in dimensions:
        cols = parameters[dim + "_cols"]
        if not cols == "":
            cols = cols.replace(" , ", ",").replace(", ", ",").replace(" ,", ",")
            comparison_dimensions[dim] = cols.split(",")
        else:
            comparison_dimensions[dim] = []

    try:
        sch = schema(
            parameters["expected_path"],
            parameters["actual_path"],
            parameters["output_path"],
            comparison_dimensions,
        )
        sch.display()
        return sch.html

    except Exception as err:
        text = ""
        traceback_string = traceback.format_exc().splitlines()
        for line in traceback_string[:-1]:
            a = 0
            while line[a] == " ":
                a += 1
            text += f"<div style='margin-left:{a}vw;'>{line[a:]}</div>"

        error_html = get_template_text("error.html")
        error_html = error_html.replace(
            "<div>ERROR</div>",
            f"<div class='center type'><span>Type: </span>{type(err).__name__}</div><span>Description</span><div class='description'>{traceback_string[-1]}</div><span>Traceback:</span><div class='traceback'>{text}</div>",
        )
        return error_html

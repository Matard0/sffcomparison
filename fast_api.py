import traceback

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from rdslm_sff_comparison.schema import schema
from rdslm_sff_comparison.utilities.utilities import get_template_text

app = FastAPI()


@app.get("/")
def get(request: Request):
    choice_html = get_template_text("index.html")
    return HTMLResponse(content=choice_html)


@app.get("/schema_comparison/{item}")
async def output_comparison(request: Request):
    parameters = request._query_params
    comparison_dimensions = {}

    dimensions = parameters["dimensions"].split(",")
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
        return HTMLResponse(content=sch.html)

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
        return HTMLResponse(content=error_html)

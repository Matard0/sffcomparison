# virtualenv env
# source antenv/bin/activate

export host="https://adb-8937165168112498.18.azuredatabricks.net" 
export token="dapi6ab57495f863823424571a67e7f9f8e3" 
export clusterid="0506-084842-girt358" 
export orgid="8937165168112498" 
export port="15001"

python -m pip install databricks-cli

pip install -U databricks-connect==7.3.*
echo "$host
$token
$clusterid
$orgid
$port" | databricks-connect configure

# python -m pip install -r requirements.txt

# kill -9 $(lsof -t -i:3000 -sTCP:LISTEN)
#export FLASK_APP=flask_api.py export FLASK_ENV=development flask run
unset FLASK_APP
unset FLASK_ENV
# flask run -h localhost -p 3000

#kill -9 $(lsof -t -i:8000 -sTCP:LISTEN)
#uvicorn fast_api:app

# rm -rf antenv
# rm -rf __pycache__
# source deactivate
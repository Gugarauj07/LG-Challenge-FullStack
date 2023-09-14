#!/bin/bash

python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt

cd processing/

python downloading.py

python dataProcessing.py

cd ../server/

python app.py
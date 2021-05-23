#!/bin/bash

python3 -m venv env
source ./env/bin/activate

pip install -r requirements.txt

cd friends_api
./manage.py makemigrations
./manage.py migrate


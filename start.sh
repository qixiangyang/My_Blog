#!/usr/bin/env bash

source venv/bin/activate
export FLASK_APP=my_blog.py
source ~/.bash_profile
#flask db upgrade
#flask run --port=5555 --host=192.168.8.239
flask run --port=8008 --host=0.0.0.0
#gunicorn my_blog:app -c gunicorn_config.py
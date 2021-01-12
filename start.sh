#!/usr/bin/env bash

source venv/bin/activate
export FLASK_APP=blog_start.py
source ~/.bash_profile
#flask run --port=5555 --host=192.168.8.239
flask run --port=8008 --host=0.0.0.0
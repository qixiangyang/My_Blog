#!/bin/bash

flask db upgrade
gunicorn my_blog:app -c gunicorn_config.py
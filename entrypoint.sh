#!/bin/bash

gunicorn my_blog:app -c gunicorn_config.py

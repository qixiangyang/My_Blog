#!/bin/bash

gunicorn acenter:app -c gunicorn_config.py

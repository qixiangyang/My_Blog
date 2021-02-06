#!/bin/bash

falsk db upgrade
gunicorn my_blog:app -c gunicorn_config.py

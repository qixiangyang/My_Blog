"""
Description:
Author:qxy
Date: 2019/9/18 3:04 下午
File: __init__.py 
"""

from flask import Blueprint

blog = Blueprint('blog', __name__)

from . import views


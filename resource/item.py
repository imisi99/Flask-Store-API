import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import item


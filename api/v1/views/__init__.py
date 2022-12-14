from flask import Blueprint

app_view = Blueprint("app_view", __name__, url_prefix="/api/v1")
from api.v1.views.users import *
from api.v1.views.rooms import *
from api.v1.views.messages import *
from api.v1.views.reviews import *

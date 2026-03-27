"""Routes package."""

from flask import Blueprint

from app.routes.add import route_add
from app.routes.subtract import route_subtract
from app.routes.multiply import route_multiply
from app.routes.divide import route_divide

api = Blueprint("api", __name__)

api.post("/add")(route_add)
api.post("/subtract")(route_subtract)
api.post("/multiply")(route_multiply)
api.post("/divide")(route_divide)

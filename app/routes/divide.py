"""Divide route."""

from app.operations import divide
from app.routes.helpers import calc_route


def route_divide():
    return calc_route("divide", divide)

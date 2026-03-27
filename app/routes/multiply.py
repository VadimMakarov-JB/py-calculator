"""Multiply route."""

from app.operations import multiply
from app.routes.helpers import calc_route


def route_multiply():
    return calc_route("multiply", multiply)

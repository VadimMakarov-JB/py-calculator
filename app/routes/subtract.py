"""Subtract route."""

from app.operations import subtract
from app.routes.helpers import calc_route


def route_subtract():
    return calc_route("subtract", subtract)

"""Add route."""

from app.operations import add
from app.routes.helpers import calc_route


def route_add():
    return calc_route("add", add)

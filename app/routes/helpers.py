"""Shared route helpers."""

from flask import jsonify, request

from app.db import log_operation


def parse_operands():
    data = request.get_json()
    if data is None or "a" not in data or "b" not in data:
        return None, None, (jsonify(error="Request body must contain 'a' and 'b'"), 400)
    try:
        a = float(data["a"])
        b = float(data["b"])
    except (TypeError, ValueError):
        return None, None, (jsonify(error="'a' and 'b' must be numbers"), 400)
    return a, b, None


def calc_route(operation_name, operation_func):
    a, b, err = parse_operands()
    if err:
        return err
    try:
        result = operation_func(a, b)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    log_operation(a, b, operation_name, result)
    return jsonify(operation=operation_name, a=a, b=b, result=result)

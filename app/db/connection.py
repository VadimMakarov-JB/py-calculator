"""Database connection management."""

import mysql.connector

_db_config = {}


def configure(config: dict):
    global _db_config
    _db_config = config


def get_connection():
    return mysql.connector.connect(**_db_config)

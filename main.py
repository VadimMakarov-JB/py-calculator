#!/usr/bin/env python3
"""Entry point for the Calculator REST API."""

import argparse

from app import create_app
from app.db import configure, init_db


def main():
    parser = argparse.ArgumentParser(description="Calculator REST API")
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", required=True)
    parser.add_argument("--db-password", default="")
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    configure({
        "host": args.db_host,
        "port": args.db_port,
        "user": args.db_user,
        "password": args.db_password,
        "database": args.db_name,
    })

    init_db()
    app = create_app()
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

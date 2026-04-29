# py-calculator

A small Flask-based REST API that performs the four basic arithmetic operations
(addition, subtraction, multiplication, division) and persists every request to
a MySQL database for auditing.

## Features

- Four JSON endpoints: `/add`, `/subtract`, `/multiply`, `/divide`.
- Validates request bodies and returns descriptive `400` errors for missing or
  non-numeric operands and for division by zero.
- Logs every successful operation (operands, operation name, result, timestamp)
  to a MySQL table `operations_log`, which is auto-created on startup.
- Database connection details and the HTTP bind address/port are supplied via
  command-line arguments — no environment variables or config files required.

## Project layout

```
py-calculator/
├── main.py              # Entry point: parses CLI args, configures DB, starts Flask
├── requirements.txt     # Python dependencies (flask, mysql-connector-python)
└── app/
    ├── __init__.py      # Flask app factory (create_app)
    ├── operations.py    # Pure arithmetic functions (add/subtract/multiply/divide)
    ├── routes/          # One module per endpoint, plus shared helpers
    │   ├── __init__.py  # Registers the API blueprint
    │   ├── add.py
    │   ├── subtract.py
    │   ├── multiply.py
    │   ├── divide.py
    │   └── helpers.py   # Operand parsing and shared response/logging flow
    └── db/              # MySQL connection + logging
        ├── __init__.py
        ├── connection.py
        └── logging.py   # Schema bootstrap and INSERT for each operation
```

The split keeps the layers independent: `operations.py` knows nothing about
HTTP, the route modules don't talk to the database directly (they go through
`helpers.calc_route`), and the `db` package encapsulates all MySQL access.

## Requirements

- Python 3.9 or newer.
- A reachable MySQL server (5.7+ / 8.x) with a database the configured user can
  write to.

## Installation

```bash
pip install -r requirements.txt
```

## Running the server

`main.py` requires the database user and database name; everything else has
sensible defaults.

```bash
python main.py \
    --db-host localhost \
    --db-port 3306 \
    --db-user calc_user \
    --db-password secret \
    --db-name calculator \
    --host 0.0.0.0 \
    --port 5000
```

| Argument        | Default     | Description                          |
| --------------- | ----------- | ------------------------------------ |
| `--db-host`     | `localhost` | MySQL host                           |
| `--db-port`     | `3306`      | MySQL port                           |
| `--db-user`     | *required*  | MySQL user                           |
| `--db-password` | `""`        | MySQL password                       |
| `--db-name`     | *required*  | MySQL database name                  |
| `--host`        | `0.0.0.0`   | Address Flask binds to               |
| `--port`        | `5000`      | Port Flask listens on                |

On startup, the app connects to MySQL and runs `CREATE TABLE IF NOT EXISTS
operations_log (...)`, so the target database must already exist but the table
does not.

## API

All endpoints accept `POST` with a JSON body of the form:

```json
{ "a": <number>, "b": <number> }
```

`a` and `b` may be sent as numbers or numeric strings; both are coerced to
`float`.

A successful response is `200 OK` with:

```json
{
  "operation": "add",
  "a": 2.0,
  "b": 3.0,
  "result": 5.0
}
```

### Endpoints

| Method | Path        | Operation                  |
| ------ | ----------- | -------------------------- |
| POST   | `/add`      | `a + b`                    |
| POST   | `/subtract` | `a - b`                    |
| POST   | `/multiply` | `a * b`                    |
| POST   | `/divide`   | `a / b` (rejects `b == 0`) |

### Error responses

- `400` — `{"error": "Request body must contain 'a' and 'b'"}` when the JSON
  body is missing or fields are absent.
- `400` — `{"error": "'a' and 'b' must be numbers"}` when an operand cannot be
  coerced to a float.
- `400` — `{"error": "Cannot divide by zero"}` for `/divide` with `b == 0`.

### Example

```bash
curl -X POST http://localhost:5000/add \
     -H 'Content-Type: application/json' \
     -d '{"a": 2, "b": 3}'
# {"a":2.0,"b":3.0,"operation":"add","result":5.0}
```

## Operation log

Every successful call appends a row to `operations_log`:

| Column       | Type           | Notes                          |
| ------------ | -------------- | ------------------------------ |
| `id`         | `INT`          | Auto-increment primary key     |
| `operand_a`  | `DOUBLE`       | First operand                  |
| `operand_b`  | `DOUBLE`       | Second operand                 |
| `operation`  | `VARCHAR(10)`  | `add` / `subtract` / etc.      |
| `result`     | `DOUBLE`       | Computed result                |
| `created_at` | `TIMESTAMP`    | Defaults to `CURRENT_TIMESTAMP`|

Failed requests (validation errors, divide-by-zero) are **not** logged.

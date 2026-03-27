"""Operation logging to MySQL."""

from app.db.connection import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            operand_a DOUBLE NOT NULL,
            operand_b DOUBLE NOT NULL,
            operation VARCHAR(10) NOT NULL,
            result DOUBLE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def log_operation(a, b, operation, result):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO operations_log (operand_a, operand_b, operation, result) VALUES (%s, %s, %s, %s)",
        (a, b, operation, result),
    )
    conn.commit()
    cursor.close()
    conn.close()

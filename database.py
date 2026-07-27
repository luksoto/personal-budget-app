from pathlib import Path
import sqlite3


DATABASE_DIRECTORY = Path("data")
DATABASE_PATH = DATABASE_DIRECTORY / "budget.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a connection to the local SQLite database."""
    DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create the initial database tables if they do not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                description_raw TEXT NOT NULL,
                merchant_name TEXT,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL
                    CHECK (transaction_type IN ('income', 'expense')),
                category TEXT,
                source TEXT NOT NULL DEFAULT 'manual',
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


if __name__ == "__main__":
    initialize_database()
    print(f"Database created successfully at: {DATABASE_PATH}")


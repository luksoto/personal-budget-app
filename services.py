from database import get_connection



def insert_transaction(
    transaction_date,
    description_raw,
    merchant_name,
    amount,
    transaction_type,
    category,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO transactions
            (
                transaction_date,
                description_raw,
                merchant_name,
                amount,
                transaction_type,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                transaction_date,
                description_raw,
                merchant_name,
                amount,
                transaction_type,
                category,
            ),
        )

        connection.commit()

def get_all_transactions():
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                transaction_id,
                transaction_date,
                merchant_name,
                description_raw,
                category,
                transaction_type,
                amount
            FROM transactions
            ORDER BY transaction_date DESC
            """
        )

        return cursor.fetchall()        

def update_transaction(
    transaction_id,
    transaction_date,
    description_raw,
    merchant_name,
    amount,
    transaction_type,
    category,
):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE transactions
            SET
                transaction_date = ?,
                description_raw = ?,
                merchant_name = ?,
                amount = ?,
                transaction_type = ?,
                category = ?
            WHERE transaction_id = ?
            """,
            (
                transaction_date,
                description_raw,
                merchant_name,
                amount,
                transaction_type,
                category,
                transaction_id,
            ),
        )

        connection.commit()    

def delete_transaction(transaction_id):
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction_id,),
        )

        connection.commit()        
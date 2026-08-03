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

def get_dashboard_summary():

    with get_connection() as connection:

        cursor = connection.execute("""
            SELECT
                SUM(CASE WHEN transaction_type='income'
                    THEN amount ELSE 0 END) AS income,

                SUM(CASE WHEN transaction_type='expense'
                    THEN amount ELSE 0 END) AS expenses,

                COUNT(*) AS total_transactions

            FROM transactions
        """)

        return cursor.fetchone()         

def get_expenses_by_category():
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                category,
                SUM(amount) AS total
            FROM transactions
            WHERE transaction_type = 'expense'
            GROUP BY category
            ORDER BY total DESC
            """
        )

        return cursor.fetchall()      

def get_monthly_expenses():

    with get_connection() as connection:

        cursor = connection.execute(
            """
            SELECT
                substr(transaction_date,1,7) AS month,
                SUM(amount) AS total
            FROM transactions
            WHERE transaction_type='expense'
            GROUP BY month
            ORDER BY month
            """
        )

        return cursor.fetchall()    
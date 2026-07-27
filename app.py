import streamlit as st
import pandas as pd
from database import initialize_database, DATABASE_PATH

from services import (
    insert_transaction,
    get_all_transactions,
    update_transaction,
    delete_transaction,
)



st.set_page_config(
    page_title="Personal Budget App",
    page_icon="💰",
    layout="wide",
)

initialize_database()

st.title("Personal Budget App")
st.write("Track, categorize, and analyze your personal finances.")

st.success("The application is running correctly.")

st.subheader("Project status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Transactions", 0)

with col2:
    st.metric("Monthly spending", "$0.00")

with col3:
    st.metric("Savings", "$0.00")


st.divider()

st.header("Add Transaction")

with st.form("transaction_form"):

    transaction_date = st.date_input("Date")

    merchant = st.text_input("Merchant")

    description = st.text_input("Description")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=0.01,
        format="%.2f",
    )

    transaction_type = st.selectbox(
        "Type",
        ["expense", "income"],
    )

    category = st.selectbox(
        "Category",
        [
            "Groceries",
            "Gas",
            "Restaurant",
            "Entertainment",
            "Utilities",
            "Shopping",
            "Salary",
            "Other",
        ],
    )

    submitted = st.form_submit_button("Save Transaction")

    if submitted:

        insert_transaction(
            str(transaction_date),
            description,
            merchant,
            amount,
            transaction_type,
            category,
        )

        st.success("Transaction saved successfully!")    

st.info(f"Local database: {DATABASE_PATH}")

st.divider()

st.header("Transactions")

transactions = get_all_transactions()

if transactions:

    df = pd.DataFrame(
        transactions,
        columns=[
            "ID",
            "Date",
            "Merchant",
            "Description",
            "Category",
            "Type",
            "Amount",
        ]
    )
    df_display = df.drop(columns=["ID"])
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Edit Transaction")

    transaction_options = {
        f"{row['Date']} | {row['Merchant']} | ${row['Amount']:.2f}": row["ID"]
        for _, row in df.iterrows()
    }

    selected_label = st.selectbox(
        "Select a transaction",
        transaction_options.keys(),
    )

    selected_id = transaction_options[selected_label]

    selected_transaction = df[df["ID"] == selected_id].iloc[0]

    with st.form("edit_transaction_form"):

        edit_date = st.date_input(
            "Edit Date",
            value=pd.to_datetime(selected_transaction["Date"]).date(),
        )

        edit_merchant = st.text_input(
            "Edit Merchant",
            value=selected_transaction["Merchant"],
        )

        edit_description = st.text_input(
            "Edit Description",
            value=selected_transaction["Description"] or "",
        )

        edit_amount = st.number_input(
            "Edit Amount",
            min_value=0.0,
            value=float(selected_transaction["Amount"]),
            step=0.01,
            format="%.2f",
        )

        type_options = ["expense", "income"]

        edit_type = st.selectbox(
            "Edit Type",
            type_options,
            index=type_options.index(selected_transaction["Type"]),
        )

        category_options = [
            "Groceries",
            "Gas",
            "Restaurant",
            "Entertainment",
            "Utilities",
            "Shopping",
            "Salary",
            "Other",
        ]

        edit_category = st.selectbox(
            "Edit Category",
            category_options,
            index=category_options.index(selected_transaction["Category"]),
        )

        update_submitted = st.form_submit_button("Update Transaction")

        if update_submitted:
            update_transaction(
                selected_id,
                str(edit_date),
                edit_description,
                edit_merchant,
                edit_amount,
                edit_type,
                edit_category,
            )

            st.success("Transaction updated successfully!")
            st.rerun()
    st.divider()

    st.subheader("Delete Transaction")

    delete_label = st.selectbox(
        "Select a transaction to delete",
        transaction_options.keys(),
        key="delete_transaction_select",
    )

    delete_id = transaction_options[delete_label]

    confirm_delete = st.checkbox(
        "I understand this transaction will be permanently deleted."
    )

    if st.button(
        "Delete Transaction",
        type="primary",
        disabled=not confirm_delete,
    ):
        delete_transaction(delete_id)

        st.success("Transaction deleted successfully!")
        st.rerun()
        
else:
    st.info("No transactions yet.")
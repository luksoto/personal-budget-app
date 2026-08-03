import streamlit as st
import pandas as pd
from database import initialize_database, DATABASE_PATH
import plotly.express as px

from services import (
    insert_transaction,
    get_all_transactions,
    update_transaction,
    delete_transaction,
    get_dashboard_summary,
    get_expenses_by_category,
    get_monthly_expenses,
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

summary = get_dashboard_summary()

income = summary["income"] or 0
expenses = summary["expenses"] or 0
transactions = summary["total_transactions"] or 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Income",
        f"${income:,.2f}"
    )

with col2:
    st.metric(
        "Expenses",
        f"${expenses:,.2f}"
    )

with col3:
    st.metric(
        "Transactions",
        transactions
    )

st.metric(
    "Savings",
    f"${income - expenses:,.2f}"
)


st.divider()
st.subheader("Expenses by Category")

category_expenses = get_expenses_by_category()

if category_expenses:
    category_df = pd.DataFrame(
        category_expenses,
        columns=["Category", "Total"],
    )

    fig = px.pie(
        category_df,
        names="Category",
        values="Total",
        hole=0.4,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
else:
    st.info("Add expense transactions to display the chart.")




st.divider()

st.subheader("Monthly Spending Trend")

monthly = get_monthly_expenses()

if monthly:

    monthly_df = pd.DataFrame(
        monthly,
        columns=["Month", "Expenses"],
    )

    fig = px.line(
        monthly_df,
        x="Month",
        y="Expenses",
        markers=True,
        title="Monthly Expenses",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:
    st.info("No monthly data available.")    


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

    st.subheader("Search Transactions")

    search_text = st.text_input("Search by merchant or description")

    filtered_df = df.copy()

    if search_text:
        filtered_df = filtered_df[
            filtered_df["Merchant"].str.contains(search_text, case=False, na=False)
            |
            filtered_df["Description"].str.contains(search_text, case=False, na=False)
        ]


    df_display = filtered_df.drop(columns=["ID"])
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
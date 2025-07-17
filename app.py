
import streamlit as st
import sqlite3
from datetime import datetime

# --- DB Functions ---
def create_db():
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_sale(product, amount):
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()
    c.execute("INSERT INTO sales (product, amount, date) VALUES (?, ?, ?)",
              (product, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_total_sales():
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM sales")
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0.0

# --- Main App ---
st.set_page_config(page_title="Daily Sales Tracker")

st.title("📊 Daily Sales Tracker")

create_db()

with st.form("sales_form"):
    st.subheader("Enter New Sale")
    product = st.text_input("Product Name")
    amount = st.number_input("Amount (₦)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Sale")
    if submitted and product and amount:
        add_sale(product, amount)
        st.success(f"Sale for '{product}' of ₦{amount:.2f} added!")

st.divider()
st.subheader("📈 Total Sales")
st.metric("Total ₦", f"{get_total_sales():,.2f}")

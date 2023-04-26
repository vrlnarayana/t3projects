#Import packages
import streamlit as st
import sqlite3
import pandas as pd

def fn_leads_load():
    data = pd.read_csv("data/Leads_001.csv")
    return data

def fn_user_load():
    data = pd.read_csv("data/Users_001.csv")
    return data

def fn_acc_load():
    data = pd.read_csv("data/Accounts_001.csv")
    return data

def fn_deal_load():
    data = pd.read_csv("data/Deals_001.csv")
    return data

def data_populate():
    # Retrieve API keys
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    leads_data = fn_leads_load()
    leads_data.columns = leads_data.columns.str.replace(' ', '_')
    user_data = fn_user_load()
    user_data.columns = user_data.columns.str.replace(' ', '_')
    acc_data = fn_acc_load()
    acc_data.columns = acc_data.columns.str.replace(' ', '_')
    deal_data = fn_deal_load()
    deal_data.columns = deal_data.columns.str.replace(' ', '_')
    st.write(leads_data)
    st.write(user_data)

    populate = st.button("Populate")
    if populate:
        # Connect to SQL database
        con = sqlite3.connect('db/turiyatree.db')
        cursor = con.cursor()
        # populate data from dataframe to DuckDB
        leads_data.to_sql('leads', con, if_exists='replace', index=False)
        user_data.to_sql('users', con, if_exists='replace', index=False)
        acc_data.to_sql('accounts', con, if_exists='replace', index=False)
        deal_data.to_sql('deals', con, if_exists='replace', index=False)
        # Get list of tables and their columns
        table_list = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = table_list.fetchall()
        for table in tables:
            column_list = cursor.execute("SELECT name FROM pragma_table_info('table');")
            st.write(table,column_list)
        con.close()
        return "Success"

if __name__ == '__main__':
    data_populate()


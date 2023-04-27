#Import packages
import streamlit as st
import os
from dotenv import load_dotenv
import openai
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
import sqlite3
import sales.menu as menu
import sales.populate_data as dpop

load_dotenv()

def sqlite_conn():
    con = sqlite3.connect('turiyatree.db')
    return con

def fn_generate_query(cursor):
    # Get list of tables in database
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # Loop through tables and columns
    query = ""
    for table in tables:
        table_name = table[0]
        columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
        for column in columns:
            column_name = column[1]
            query += f"SELECT {column_name} FROM {table_name};\n"
    return query


def main():
    menu_out = menu.menu()
    if menu_out == "Query":
        #st.title("Langchain-GPT3 based DB search")
        # Retrieve API keys
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Connect to SQL database
        with st.expander('Sample Queries',expanded=False):
            st.markdown("*Please list the deals which were Closed Won and Closed Lost in the last one year*")
            st.markdown("*Please list the leads which were converted into deals in the last five years*")
            st.markdown("*Name the account and revenue which is the largest account in terms of annual revenue*")
            st.markdown("*Name the account and revenue which is the smallest in terms of annual revenue*")
            st.markdown("*From which existing business did we win and close a deal successfully in the last one year?*")
            st.markdown("*List the total sales per country. Which country's customers spent the most?*")
        text = st.text_area("Query here..", max_chars=1500)

        show = st.button("show result")
        if text and show:
            db = SQLDatabase.from_uri("sqlite:///db/turiyatree.db")
            llm = OpenAI(temperature=0)
            toolkit = SQLDatabaseToolkit(db=db)
            agent_executor = create_sql_agent(
                llm=OpenAI(temperature=0),
                toolkit=toolkit,
                verbose=True
            )
            out = agent_executor.run(text)
            st.write(out)
    elif menu_out == "Populate":
        dpop.data_populate()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


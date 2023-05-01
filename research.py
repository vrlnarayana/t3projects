import streamlit as st
import sales.salesquery as sq
import crawl.chatbot as cb
import auth.login as login
import langchain_demo

def app():
    st.sidebar.image('images/black-logo-text.png')
    yourname, yourpass, allowentry = login.login()
    if allowentry == 'authenticated':
        st.sidebar.divider()
        menu = st.sidebar.selectbox("Main Menu:",["Sales Query","Bot Page"],key="menu")
        if menu == "Sales Query":
            st.title("Sales Query")
            sq.main()
        elif menu == "Bot Page":
            st.title("Chat Bot")
            cb.main()

        st.sidebar.divider()
    else:
        st.sidebar.write("\n",allowentry)

import streamlit as st
import sales.salesquery as sq
import crawl.chatbot as cb

def app():
    st.sidebar.divider()
    menu = st.sidebar.radio("Main Menu:",["Sales Query","Bot Page"],key="menu")
    if menu == "Sales Query":
        st.title("Sales Query")
        sq.main()
    elif menu == "Bot Page":
        st.title("Chat Bot")
        cb.main()

    st.sidebar.divider()


import streamlit as st
import sales.salesquery as sq
import crawl.chatbot as cb
import auth.login as login
import langchain_demo
import utility.pdf2html as pdf2html

def app():
    st.sidebar.image('images/black-logo-text.png')
    yourname, yourpass, allowentry = login.login()
    if allowentry == 'authenticated':
        st.sidebar.divider()
        menu = st.sidebar.selectbox("Main Menu:",["Sales Query","Bot Page", "Utility"],key="menu")
        if menu == "Sales Query":
            st.title("Sales Query")
            sq.main()
        elif menu == "Bot Page":
            st.title("Chat Bot")
            cb.main()
        elif menu == "Utility":
                    st.title("Utility")
                    pdf2html.scanpdf()

        st.sidebar.divider()
    else:
        st.sidebar.write("\n",allowentry)

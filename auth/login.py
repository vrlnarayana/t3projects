import streamlit as st

import auth.authenticate as au

# pass login field values
def login():
    st.sidebar.header('Login to access the App')
    yourname = st.sidebar.text_input('name',max_chars=20, key=11)
    yourpass = st.sidebar.text_input('passcode',max_chars=8,type="password",key=22)
    #.__hash__() hashed password field to be added
    authallow=au.authenticate(yourname, yourpass)  # authenticate with name,passcode not empty and passcode matching
    return yourname, yourpass,authallow

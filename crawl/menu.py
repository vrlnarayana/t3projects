import streamlit as st
def menu():
    st.write('\n')
    st.sidebar.divider()
    menu_choice = st.sidebar.radio("Bot Page - Sub Menu:", ('Chat', 'Crawl'), index=0, key=123)
    return menu_choice


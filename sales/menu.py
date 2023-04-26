import streamlit as st
def menu():
    st.write('\n')
    st.sidebar.divider()
    menu_choice = st.sidebar.radio("Sales Query - Sub Menu:", ('Query', 'Populate'), index=0, key=321)
    return menu_choice


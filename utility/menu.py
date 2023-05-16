import streamlit as st
def menu():
    st.write('\n')
    st.sidebar.divider()
    menu_choice = st.sidebar.radio("utility - Sub Menu:", ('PDF2HTML','OPEN-HTML'), index=0, key=3212)
    return menu_choice


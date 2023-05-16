import streamlit as st
import pandas as pd
import json

if 'i' not in st.session_state:
    st.session_state['i'] = 0

if 'responded' not in st.session_state:
    st.session_state['responded'] = []

# Load the survey questions from a JSON file
with open('data.json', 'r') as f:
    survey_data = json.load(f)

# Create a DataFrame from the survey questions
df = pd.DataFrame(survey_data['survey']['questions'])

# Create an empty array to store the user's survey responses
responses = []

# Define a function to display a survey question and get the user's response
def ask_question(index):
    question = df.loc[index, 'question']
    options = df.loc[index, 'options']
    response = st.radio(question, list(options.values()), key=str(index), on_change=lambda val: responses.append(val))
    return index,response

# Display the survey questions one by one and get the user's responses
st.write("# Customer Satisfaction Survey")

#with st.button(label="click",key='survey_form'):
if st.button("click"):
    if st.session_state.i < len(df):
        indx,response = ask_question(st.session_state.i)
        st.session_state.responded.append(response)
        st.session_state.i=indx+1
    else:
        st.write("Thank you for taking the survey!")

    #st.write(st.session_state.responded,is_user=True)
    # Add a submit button to the form
    #submit_button = st.form_submit_button(label='Submit')


"""Python file to serve as the frontend"""
import os
from dotenv import load_dotenv
import openai
import streamlit as st
from streamlit_chat import message

from langchain.chains import ConversationChain
from langchain.llms import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_chain():
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain

chain = load_chain()

def main():

    # From here down is all the StreamLit UI.
    st.set_page_config(page_title="Conversation Chain Demo", page_icon=":robot:")
    st.header("Conversation Chain Demo")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []


    def get_text():
        input_text = st.text_input("You: ", key="input")
        return input_text


    user_input = get_text()
    #input_button = st.button("submit")

    if user_input:
        output = chain.run(input=user_input)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state["generated"]:

        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

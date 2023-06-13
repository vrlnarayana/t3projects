import os
import requests
import streamlit as st
from dotenv import load_dotenv
import openai
from sales.llm_agent import LLMAgent

load_dotenv()


# Define the base URL for the API
BASE_URL = "http://localhost:8000"
api_schema_path = 'api_schema.json'
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
agent = LLMAgent(api_schema_path)
# Define the available API endpoints_map
endpoints_map = {
    "Read Leads": "/leads",
    # "Create Lead": "/leads",
    "Read Lead": "/leads/{lead_id}",
    # "Update Lead": "/leads/{lead_id}",
    # "Delete Lead": "/leads/{lead_id}",
    "Search Leads": "/search_leads",
    "Chat": "chat",
}

# Define the available search types
search_types = {
    "Name": "name",
    "Company": "company",
    "Email": "email",
}


def show_messages(text, messages):
    messages_str = [f"{_['role']}: {_['content']}" for _ in messages[1:]]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)


def frontend_app():
    # Set the page title
    #st.set_page_config(page_title="FastAPI Chatbot")

    # Define the sidebar options
    st.sidebar.title("API Endpoints")
    endpoint = st.sidebar.radio("Select an endpoint", list(endpoints_map.keys()))

    # Define the API parameters based on the selected endpoint
    if endpoint == "Read Leads":
        skip = st.sidebar.number_input("Skip", value=0)
        limit = st.sidebar.number_input("Limit", value=100)
        params = {
            "skip": skip,
            "limit": limit,
        }
    # elif endpoint == "Create Lead":
    #     name = st.text_input("Name")
    #     company = st.text_input("Company")
    #     email = st.text_input("Email")
    #     data = {
    #         "name": name,
    #         "company": company,
    #         "email": email,
    #     }
    #     params = {}
    elif (
        endpoint == "Read Lead"
        or endpoint == "Update Lead"
        # or endpoint == "Delete Lead"
    ):
        lead_id = st.text_input("Lead ID")
        data = {}
        params = {}
        # if endpoint == "Update Lead":
        #     response = requests.get(
        #         BASE_URL + endpoints_map[endpoint].format(lead_id=lead_id)
        #     )
        #     if response.ok:
        #         result = response.json()
        #         name = st.text_input(
        #             "Name",
        #             value=result["name"],
        #         )
        #         company = st.text_input(
        #             "Company",
        #             value=result["company"],
        #         )
        #         email = st.text_input(
        #             "Email",
        #             value=result["email"],
        #         )
        #         data = {
        #             "name": name,
        #             "company": company,
        #             "email": email,
        #         }
        #     else:
        #         st.error(response.text)
    elif endpoint == "Search Leads":
        search_type = st.sidebar.selectbox("Search Type", list(search_types.keys()))
        search_query = st.sidebar.text_input("Search Query")
        params = {
            "search_type": search_types[search_type],
            "search_query": search_query,
        }
    elif endpoint == "Chat":
        openai.api_key = OPENAI_API_KEY
        BASE_PROMPT = [
            {
                "role": "system",
                "content": "Hey there...",
            }
        ]

        if "messages" not in st.session_state:
            st.session_state["messages"] = BASE_PROMPT

        st.header("Test Bot")

        text = st.empty()
        show_messages(
            text,
            st.session_state["messages"],
        )

        prompt = st.text_input(
            "Prompt",
            value="",
        )

        if st.button("Send"):
            with st.spinner("Generating response..."):
                st.session_state["messages"] += [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
                # response = openai.ChatCompletion.create(
                #     model="gpt-3.5-turbo",
                #     messages=st.session_state["messages"],
                # )
                response = agent.get_query_plan(st.session_state["messages"])
                message_response = response #["choices"][0]["message"]["content"]
                st.session_state["messages"] += [
                    {
                        "role": "system",
                        "content": message_response,
                    }
                ]
                show_messages(
                    text,
                    st.session_state["messages"],
                )

        if st.button("Clear"):
            st.session_state["messages"] = BASE_PROMPT
            show_messages(
                text,
                st.session_state["messages"],
            )
    # Send the HTTP request to the API and display the response
    st.subheader(endpoint)
    if endpoint == "Read Leads":
        response = requests.get(
            BASE_URL + endpoints_map[endpoint],
            params=params,
        )
        if response.ok:
            result = response.json()
            st.json(result)
        else:
            st.error(response.text)

    # elif endpoint == "Create Lead":
    #     response = requests.post(
    #         BASE_URL + endpoints_map[endpoint],
    #         json=data,
    #     )
    #     if response.ok:
    #         result = response.json()
    #         st.json(result)
    #     else:
    #         st.error(response.text)

    elif endpoint == "Read Lead":
        response = requests.get(
            BASE_URL + endpoints_map[endpoint].format(lead_id=lead_id)
        )
        if response.ok:
            result = response.json()
            st.json(result)
        else:
            st.error(response.text)

    elif endpoint == "Update Lead":
        response = requests.put(
            BASE_URL + endpoints_map[endpoint].format(lead_id=lead_id), json=data
        )
        if response.ok:
            result = response.json()
            st.json(result)
        else:
            st.error(response.text)

    # elif endpoint == "Delete Lead":
    #     response = requests.delete(
    #         BASE_URL + endpoints_map[endpoint].format(lead_id=lead_id)
    #     )
    #     if response.ok:
    #         result = response.json()
    #         st.json(result)
    #     else:
    #         st.error(response.text)

    elif endpoint == "Search Leads":
        response = requests.get(
            BASE_URL + endpoints_map[endpoint],
            params=params,
        )
        if response.ok:
            result = response.json()
            st.json(result)
        else:
            st.error(response.text)


# Run the Streamlit frontend_app
if __name__ == "__main__":
    frontend_app()

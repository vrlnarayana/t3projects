import duckdb
import os
from dotenv import load_dotenv
import openai
import numpy as np
import streamlit as st
import crawl.menu as menu
import crawl.crawl as crawl
import ast
import pandas as pd
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
    load_dotenv()
    menu_out = menu.menu()
    if menu_out == 'Chat':
        if "generated" not in st.session_state:
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []

        # connect to DuckDB database
        conn = duckdb.connect(database='duckdb/turiyatree.db')
        # Execute a SQL query to get the table names
        result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Fetch the results as a list of tuples
        tables = result.fetchall()
        #st.write(tables)
        # list of tables
        tables_list = []
        for table in tables:
            tables_list.append(table[0])
        selected_table = st.selectbox("Select your dataset:",tables_list)

        # get search string input from user
        search_str = st.text_area("Enter your search query: ")
        if search_str:
            # retrieve all embeddings from the table
            query = "SELECT DISTINCT * FROM "+selected_table
            #st.write(query)
            df = conn.execute(query).fetchdf()
            #st.write(df)
            model_engine = "text-davinci-003"
            prompt = "Nearest embeddings to: "+search_str
            # Encode the search query into an embedding
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=prompt
            )
 
            # Extract the vector embeddings from the API response and print them
            search_embedding = np.array(response.data[0].embedding)
            # Compute cosine similarity between the search embedding and all embeddings in the table
            embeddings = np.array(df['embedding']).tolist()
            similarity_scores = []
            for i in range(len(df)):
                embeddings_list = ast.literal_eval(embeddings[i])
                embeddings_arr = np.array(embeddings_list, dtype=np.float32)
                similarity_score = embeddings_arr.dot(search_embedding) / (np.linalg.norm(embeddings_arr) * np.linalg.norm(search_embedding))
                similarity_scores.append(similarity_score)

            # Find the most similar content
            sorted_indices = np.argsort(similarity_scores)[::-1]  # Sorts indices in descending order

            top_10_indices = sorted_indices[:20]  # Take the top 10 indices
            top_5_indices = sorted_indices[:10]  # Take the top 5 indices

            most_similar_contents = []
            for index in top_10_indices:
                most_similar_contents.append(df['content'][index])
                most_similar_string = " ".join(most_similar_contents)
            tokenize_content = most_similar_string.strip().split(" ")
            #st.write("LEn",len(tokenize_content))
            if len(tokenize_content) > 1000:
                most_similar_contents = []
                for index in top_5_indices:
                    most_similar_contents.append(df['content'][index])

            most_similar_df = pd.DataFrame(most_similar_contents).drop_duplicates()
            most_similar_contents = np.array(most_similar_df).tolist()
            # generate response using ChatGPT and the most similar content
            promptpreempt = "You are a representative of the company and you will answer based on the information you have. If I am confident in my answer, I will provide it to you. If you don't have enough information to provide a confident answer, you will let people know that you don't have enough information."
            prompt1 = promptpreempt+f"{most_similar_contents}\n\nQuestion: {search_str}\nAnswer:"
            #st.write(prompt1)
            response = chain.run(input=prompt1)
            st.session_state.past.append(search_str)
            st.session_state.generated.append(response)
            st.write("\n")
            # print the generated response
            if st.session_state["generated"]:
                for i in range(len(st.session_state["generated"]) - 1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

            st.write("\n")
            #st.write("most_similar_content", most_similar_contents)
    elif menu_out == 'Crawl':
        crawl.crawl(openai.api_key)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

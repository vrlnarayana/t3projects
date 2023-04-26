#import packages
import streamlit as st
import requests
from bs4 import BeautifulSoup 
#also requires lxml - ensure you do pip install beautifulsoup4 & pip install lxml 
import openai
import duckdb
import time


def crawl(api_key):
    # send a GET request to the webpage
    #url = 'https://www.e-consystems.com/embedded-cameras-frequently-asked-questions.asp'
    # Connect to the database or create a new one
    con = duckdb.connect(database='duckdb/turiyatree.db')
    # Set your OpenAI API key
    openai.api_key=api_key
    # Create a table to store the embeddings
    #con.execute('DROP TABLE embeddings')
    url = st.text_input("Provide sitemap url:(example: https://www.turiyatree.com/page-sitemap.xml)")
    sitemap = url
    st.write(sitemap)
    #sitemap = 'https://www.e-consystems.com/sitemap.xml'
    if url:
        # remove the protocol prefix
        company_name = url.split("://")[-1]
        # split the remaining string using dot separator
        company_name = company_name.split(".")[0]+company_name.split(".")[1]
        st.write(company_name)
        response = requests.get(sitemap,verify=False)
        xml_doc = response.text
       # Parse the XML document
        soup = BeautifulSoup(xml_doc, 'lxml')
       # Extract the URLs
        urls = [url.text for url in soup.find_all('loc')]
        # Print the URLs
        st.write(urls)
        if urls:
            create_table = f'CREATE TABLE IF NOT EXISTS ' + company_name + '_embeddings (content TEXT, embedding VARCHAR)'
            st.write("\n Table created ",company_name,"_embeddings")
            con.execute(create_table)
            # for percent_complete in range(100):
            for url in urls:
                response = requests.get(url, verify=False)
                soup = BeautifulSoup(response.text, "html.parser")
                # Loop through the extracted content and create vector embeddings for each piece
                for div in soup.find_all("div"):
                    content = ""
                    for elem in div.contents:
                        if hasattr(elem, "text"):
                            content += elem.text.strip()
                        elif hasattr(elem, "src"):
                            content += elem["src"].strip()
                        elif hasattr(elem, "href"):
                            content += elem["href"].strip()
                        else:
                            content += str(elem).strip()
                    if content:
                        st.write("\n Content scraping completed....")
                        # Generate vector embeddings for the content using the text-embedding-ada-002 model
                        response = openai.Embedding.create(
                            engine="text-embedding-ada-002",
                            input=content,
                            max_tokens=1024,
                            n=1,
                            stop=None,
                            temperature=0,
                        )
                        # Extract the vector embeddings from the API response and print them
                        embeddings = response.data[0].embedding
                        con.execute('INSERT INTO ' + company_name + '_embeddings VALUES (?, ?)', (content, embeddings))
                        st.write("\n Embeddings update completed.....")
                        # Sleep for 1 second to avoid rate limiting
                        time.sleep(1)
    # Close the connection to the database
            #my_bar_content.progress(percent_complete + 1, text=progress_text_content)
            st.write("\n Successfully written embeddings into db")
    con.close()


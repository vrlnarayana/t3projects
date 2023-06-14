from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate(
    input_variables=["schema", "query"],
    template="""OpenAPISchema: {schema} \n 
            ----
            Query : {query} \n
            ----
            Given the above OpenAPISchema and the Query, come up with a query plan for invoking the endpoints. Provide the answer strictly in the below schema dict format.  
            order_number: <shows the order of planned execution>, 
            request_type:  <should be either of [GET,PUT,POST,DELETE]>,
            endpoint_url:  <the endpoint to invoke such as /leads>, 
            payload: <the payload that needs to be used in dict format>
 
    """,
)


class LLMAgent:
    def __init__(self, api_schema_path):
        self.api_schema_path = api_schema_path
        self.llms = OpenAI(
            temperature=0.9,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.schema = self.get_schema()
        self.prompt = prompt

    def get_schema(self):
        with open(self.api_schema_path) as f:
            self.schema = json.loads(f.read())

    def get_query_plan(self, query):
        chain = LLMChain(llm=self.llms, prompt=self.prompt)
        response = chain.run({"schema": self.schema, "query": query})
        return response
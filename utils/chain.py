from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import os

load_dotenv()
LLM_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    api_key=LLM_KEY,
)

class DocumentRetriever:
    def __init__(self, retriever):
        self.llm = llm
        self.retriever = retriever
        self.document_variable_name = "context"

        # Define how each document should be formatted
        self.document_prompt = PromptTemplate(
            input_variables=["page_content"], 
            template="{page_content}"
        )

        # Create a prompt template for summarization or answering queries
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context. 
        Think step by step before providing a detailed answer. 
        if there is no context given then Respond with  "I don't know". 
        otherwise, provide a detailed answer based on the context.
        <context>
        {context}
        </context>
        Question: {input}""")

        # Initialize LLMChain
        self.chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.chain)

        

    def retrieve_and_answer(self, query):
        try:
            # Retrieve relevant documents
            retrieved_docs = self.retrieval_chain.invoke({"input": query})
            return retrieved_docs
        except Exception as e:
            return f"Failure: {str(e)}"
        
    
        


    
    

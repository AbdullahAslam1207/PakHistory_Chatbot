from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from flask import jsonify
import os

from dotenv import load_dotenv
load_dotenv()

LLM_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=LLM_KEY
)

class EmbeddingsCreator:
    def __init__(self):
        
        self.documents = []
        self.embedding_model=embeddings 

    def process_documents(self, documents, x):
        try:
            # Split the documents into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            document_chunks = text_splitter.split_documents(documents)
            self.documents = document_chunks
            
            # Create FAISS vector store
            db = FAISS.from_documents(self.documents, self.embedding_model)
            # serialized_faiss_index = db.serialize_to_bytes()
            
            # folder_name = "VectorStore"
            # os.makedirs(folder_name, exist_ok=True)

            # # Define the file path inside the folder
            # file_name = f"faiss_index{x}.pkl"
            # file_path = os.path.join(folder_name, file_name)
            # # Save the serialized FAISS index
            # with open(file_path, "wb") as f:
            #     f.write(serialized_faiss_index)

            
                
            # return f"Embeddings created and stored successfully!:  {file_name}"
            print ("I am here")
            return db.as_retriever() # Return the FAISS index object for further use
        
        except Exception as e:
            return f"Failure: {str(e)}"
            
    # def load_faiss_index(self,faiss_index):
    #     try:
    #         # Load the FAISS index from the pickle file

    #         folder_name = "VectorStore"
    #         file_name = faiss_index  # Ensure 'x' has a valid value
    #         file_path = os.path.join(folder_name, file_name)

    #         # Load the FAISS index
    #         with open(file_path, "rb") as f:
    #             serialized_faiss_index = f.read()
            
                
    #         db = FAISS.deserialize_from_bytes(embeddings=self.embedding_model, serialized=serialized_faiss_index,allow_dangerous_deserialization=True)
    #         return db
        
    #     except Exception as e:
    #         return f"Failure: {str(e)}"

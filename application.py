from flask import Flask, request, jsonify, abort,render_template

from dotenv import load_dotenv
from functools import wraps
from flask_cors import CORS 
from utils.documentprocessor import DocumentProcessor
from utils.embeddings import EmbeddingsCreator
from utils.access import set_retriever
from utils.agent import Agent
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import os 

application=Flask(__name__)
CORS(application)

load_dotenv()

# Load the environment variables from the .env file
API_KEY=os.getenv("OPENAI_API_KEY")

#Define the global retriver variable
retriever=None


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import os

load_dotenv()
LLM_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    api_key=LLM_KEY,
)

@application.route('/')
def home():
    return render_template('index.html')  # Renders the HTML file

#Adding Document links
@application.route("/document", methods=["POST"])
def document_route():
    data=request.get_json()
    document_url=data.get("document_url",[])

#     document_url = [
#     r"C:\Users\ABDULLAH ASLAM\Desktop\Internship\Pak_History_Chatbot\file1.txt",
#     # r"C:\Users\ABDULLAH ASLAM\Desktop\Internship\Pak_History_Chatbot\file2.docx",
#     # r"C:\Users\ABDULLAH ASLAM\Desktop\Internship\Pak_History_Chatbot\file3.pdf"
# ]


    print(document_url)

    if not document_url:
        return jsonify({"error": "No document URL provided"}), 400
    
    #to check if the documents are onyl pdf , txt or docx
    for doc in document_url:
        if doc.endswith(('.pdf', '.txt', '.docx')):
            
            pass
        else:
            return jsonify({"error": f"Unsupported file format: {doc}"}), 400
    
    #Merge all the documents provided in a single Document of type Document.(Page_Content)
    documents = []
    process_documents=DocumentProcessor()
    process_documents.add_files(document_url)
    process_documents.process_pdfs()
    process_documents.process_text_files()
    process_documents.process_word_files()
    #save the documents for emebeddings further 
    document=process_documents.get_documents()

    #Create Embeddings for the the Document
    embeddings=EmbeddingsCreator()
    db=embeddings.process_documents(document, 1)
    
    # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    # rag_chain = create_retrieval_chain(db, combine_docs_chain)

    # response= rag_chain.invoke({"input": "What Happned on May 1857 in Pakistan?"})
    # return jsonify({"message": response['answer'] }), 200
        
    try:
        global retriever
        retriever=db
        set_retriever(retriever)
        #Initilize the agent so it will be used only one time 
        global agent
        agent=Agent()
        return jsonify({"message": "Documents processed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    # return jsonify({"message": "Documents processed successfully!"}), 200
    # return db
    

    #Create the query route 
@application.route("/query", methods=["POST"])

def query_route():
    data=request.get_json()
    query=data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    if retriever is None:
        return jsonify({"error": "No retriever available. Please process documents first."}), 400
    try:
        # agent=Agent()
        response = agent.get_resposne(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"response": response}), 200

if __name__ == "__main__":
    application.run(debug=True)
        





from langchain_core.tools import tool
from utils.chain import DocumentRetriever
from utils.access import get_retriever

@tool
def retrieval_qa_chain(input: str) -> str:
    """
    The name of this tool is retrieval_qa_chain
    Use this tool when the user asks information about the history of Pakistan.
    Input to this tool should be the user query without any modifications.
    """
    retriver=get_retriever()
    retrieval_qa_chain = DocumentRetriever(retriever=retriver)

    response = retrieval_qa_chain.retrieve_and_answer(input)
    return response['answer']
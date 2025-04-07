from langchain_core.tools import tool
from dotenv import load_dotenv
from openai import OpenAI
import os 
import requests
from prompts.prompt import INTERENT_PROMPT


load_dotenv()
# Load the environment variables from the .env file
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
CX=os.getenv("CX")
google_api_key = GOOGLE_API_KEY  # Replace with your actual API key (Google)
google_cx = CX  # Replace with your actual Custom Search Engine ID (Google)


@tool
def google_search(search_query: str) -> str:
    """
    The name of this tool is google_search.
    Use this tool when you want to search the internet or the user asks about news.
    Never use this tool if the user query contains Pakistan Army or Special Forces.
    Input to this tool should be the user query without any modification.
    """
    
    # Perform the search and obtain search results
    search_results = perform_search(search_query, google_api_key, google_cx)

    # Query the LLM with the search results and get the response
    response_text = query_llm_with_search_results(search_query, search_results)

    return response_text  # Return the LLM's response
    

def perform_search(query, api_key, cx):
    """
    Perform a search using the Google Custom Search API.
    
    Args:
    - query (str): The search query.
    - api_key (str): The Google API key.
    - cx (str): The Custom Search Engine ID.

    Returns:
    - dict: The search results in JSON format.
    """
    params = {
        "key": api_key,  # API key for authentication
        "cx": cx,        # Custom Search Engine ID
        "q": query       # Search query
    }
    # Make a GET request to the Google Custom Search API
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params, verify=False)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    search_results = response.json()  # Parse the JSON response
    return search_results


def query_llm_with_search_results(query, search_results):
    """
    Query the LLM with the search results and return the response.
    
    Args:
    - query (str): The original search query.
    - search_results (dict): The search results obtained from Google Custom Search.

    Returns:
    - str: The LLM's response.
    """
    # Extract relevant information from search results
    search_results_text = ""
    if 'items' in search_results:
        search_results_text = "\n".join(
            f"Snippet: {item['snippet']}\nLink: {item['link']}"
            for item in search_results['items']
        )
        # search_results_text = "\n".join(item['snippet'] for item in search_results['items'])

    # return search_results_text
    # Combine the query and search results into a single input for the LLM
    combined_input = f"Query: {query}\nSearch Results:\n{search_results_text}"
    # print(search_results_text)  # Print search results for debugging
    
    # Create a client instance for OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Query the LLM with the combined input
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=[
            {"role": "system", "content": INTERENT_PROMPT},
            {"role": "user", "content": combined_input}
        ]
    )
    
    return response.choices[0].message.content.strip()  # Return the LLM's response




# # Print the LLM's response
# print(response_text)


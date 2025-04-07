from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver 
from dotenv import load_dotenv
from tools.context import retrieval_qa_chain
from tools.internet import google_search
from tools.mail import send_email
from prompts.prompt import AGENT_PROMPT
import os

load_dotenv()

LLM_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini",
                   api_key=LLM_KEY)

class Agent:
    def __init__(self):
        self.model = model
        self.tools = [retrieval_qa_chain, google_search, send_email]
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", AGENT_PROMPT), # This will be replaced with the agent prompt
                ("placeholder", "{messages}") # This will be replaced with the messages in the conversation
                
              ]           
        )
        self.memory = MemorySaver()
        self.langgraph_agent_executor = create_react_agent(model, self.tools, prompt=self.prompt, checkpointer=self.memory)
        self.config = {"configurable": {"thread_id": "test-thread"}}
    
    def get_agent_executor(self):
        return self.langgraph_agent_executor
    
    def get_resposne(self, query):
        return self.langgraph_agent_executor.invoke({"messages": [("user", query)]},config=self.config)["messages"][-1].content





# messages = langgraph_agent_executor.invoke({"messages": [("user", query)]},config=config)
# print(messages["messages"][-1].content)
# print('--------------------------------')
# query='Do you know my name?'
# messages = langgraph_agent_executor.invoke({"messages": [("user", query)]},config=config)   
# print(messages["messages"][-1].content)
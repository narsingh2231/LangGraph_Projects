from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal,Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]
    
    
    
def chat_node(state:ChatState):
    
    messages = state['messages']
    
    response = llm.invoke(messages)
    
    return {'messages':[response]}

conn= sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
# add node
graph.add_node('chat_node', chat_node)
#add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot= graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

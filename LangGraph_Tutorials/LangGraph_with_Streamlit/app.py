from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal,Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.tools import tool

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

@tool
def calculator(first_num:float, second_num:float, operation:str)->dict:
    """Perform a basic arithmetic operation on two numbers.
    supported operations add, sub, mul, div.

    Args:
        first_num (float): _description_
        second_num (float): _description_
        operation (str): _description_

    Returns:
        dict: _description_
    """
    
    try:

        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result":result}
    except Exception as e:
        return {"error": str(e)}


search_tool = TavilySearchResults()

tools=[search_tool, calculator]

llm = ChatGroq(model="llama-3.3-70b-versatile")

llm_with_tools=llm.bind_tools(tools)

class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]
    
    
    
def chat_node(state:ChatState):
    
    messages = state['messages']
    
    response = llm_with_tools.invoke(messages)
    
    return {'messages':[response]}


### Node definition
# def tool_calling_llm(state:ChatState):
#     return {"messages":[llm_with_tools.invoke(state["messages"])]}

conn= sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
# add node
graph.add_node('chat_node', chat_node)
graph.add_node("tools", ToolNode(tools))



#add edges
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges(
    "chat_node",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
graph.add_edge("tools", 'chat_node')
graph.add_edge('chat_node', END)


chatbot= graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

import streamlit as st
from chatbot_app_mcp import chatbot, retrieve_all_threads, submit_async_task
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid
import queue


# ********************************************** Utility Functions ***********************************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id']= thread_id
    add_thread(thread_id) 
    st.session_state['message_history']= []
    
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        
def load_converstion(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id':thread_id}}).values['messages']


# st.session_state --> dict --> retain on every run

# ********************************************** Session Setup ****************************************************
CONFIG = {'configurable': {'thread_id':generate_thread_id()}}
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
   st.session_state['thread_id'] =  generate_thread_id()
   
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])   
    
# ********************************************** Sidebar UI ****************************************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    if not st.session_state['message_history']== []:
        reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        if thread_id == st.session_state['thread_id']:
            pass  # Already on this thread
        else:
            st.session_state['thread_id'] = thread_id
            messages = load_converstion(st.session_state['thread_id'])
        
            temp_messages = []
            for message in messages:
                if isinstance(message, HumanMessage):
                    role='user'
                else:
                    role='assistant'
                temp_messages.append({'role': role,'content' : message.content})
                
            st.session_state['message_history'] = temp_messages
        

# ********************************************** Main UI ****************************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
user_input = st.chat_input('Type here....')

if user_input:
    st.session_state['message_history'].append({'role':'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    CONFIG = {
        "configurable": {"thread_id": st. session_state["thread_id"]},
        "metadata": {
        "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",

        }

   # first add the message to message_history
    with st.chat_message("assistant"):
        status_holder = {'box':None}
        def ai_only_stream():
            event_queue:queue.Queue = queue.Queue()
            
            async def run_stream():
                try:
                    async for message_chunk, metadata in chatbot.astream(
                        {"messages": [HumanMessage(content=user_input) ]},
                        config=CONFIG,
                        stream_mode="messages"
                    ):
                        event_queue.put((message_chunk, metadata))
                except Exception as exc:
                    event_queue.put(("error", exc))
                finally:
                    event_queue.put(None)
                    
            submit_async_task(run_stream())
            
            while True:
                item = event_queue.get()
                if item is None:
                    break
                message_chunk, metadata = item
                if message_chunk == "error":
                    raise metadata
                        
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f" Using `{tool_name}` ... ", expanded=True)

                    else:
                        status_holder["box"].update(
                            label=f"🕘 Using {tool_name}' ... ",
                            state="running",
                            expanded=True,)



                if isinstance(message_chunk, AIMessage) :
                    # yield only assistant tokens
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())
        
        # Finalizing only if a tool was actually used
        if status_holder['box'] is not None:
            status_holder['box'].update(
                label="✅Tool finished", state="complete", expanded=False
            )

  
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
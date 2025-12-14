# Import necessary libraries
import databutton as db
import streamlit as st
from streamlit_lottie import st_lottie

# Import Langchain modules
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# Streamlit UI Callback
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langgraph.prebuilt import create_react_agent

import openai
import sympy
from ddgs import DDGS


# Import modules related to streaming response
import os
import time

# Try to get API key from databutton, fall back to environment variables
try:
    OPENAI_API_KEY = db.secrets.get(name="OPENAI_API")
except Exception:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
else:
    st.error("⚠️ OPENAI_API_KEY not found. Please set the environment variable or configure databutton secrets.")



st.title("🤖 Qu'est-ce qu'un Agent?")
st.lottie("https://lottie.host/5db2cb4f-6dbb-4a39-b2e2-d7eca7dc2989/SeQeMwtKCR.json")
st.markdown("""
### Bonjour! 👋

Un **agent** est comme un super assistant intelligent! Quand tu lui poses une question, voici ce qui se passe:

1. **L'agent écoute** ta question 👂
2. **L'agent pense** 💭 "Hmm, de quel outil j'ai besoin?"
3. **L'agent choisit un outil** 🔧 (comme une calculatrice ou Internet!)
4. **L'agent utilise l'outil** ⚙️ pour trouver la réponse
5. **L'agent te dit la réponse** 💡

Regarde ce qui se passe dans le cerveau de l'agent! ↓
""")


# Initialize the OpenAI language model and search tool
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Define tools
tool_display_names = {
    "search_internet": "Recherche Internet",
    "calculate": "Calculatrice"
}

@tool
def search_internet(query: str) -> str:
    """Useful for when you need to do a search on the internet to find information that another tool can't find. Be specific with your input or ask about something that is new and latest."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return str(results)
    except Exception as e:
        return f"Error searching: {e}"

@tool
def calculate(expression: str) -> str:
    """Useful for when you need to answer questions about math. Use this for mathematical calculations."""
    try:
        result = sympy.sympify(expression).evalf()
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"

tools = [search_internet, calculate]

# Initialize chat history if it doesn't already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create the agent with the new API
agent_executor = create_react_agent(llm, tools)

question = st.chat_input("Pose-moi une question! 🎤 (par exemple: Combien font 5 plus 3?)")

# Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process the user's question and generate a response
if question:
    # Display the user's question in the chat message container
    with st.chat_message("user"):
        st.markdown(question)
    # Add the user's question to the chat history
    st.session_state.messages.append({"role": "user", "content": question})

    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        reasoning_container = st.container()
        
        full_response = ""
        try:
            # Invoke the agent with streaming to show progressive reasoning
            reasoning_steps = []
            final_response = ""
            last_tool_used = ""
            
            with reasoning_container:
                reasoning_placeholder = st.empty()
            
            for step in agent_executor.stream(
                {"messages": [{"role": "user", "content": question}]}
            ):
                if "agent" in step:
                    # Agent's thought process and tool calls
                    messages = step["agent"]["messages"]
                    for msg in messages:
                        if hasattr(msg, 'content') and msg.content:
                            # Simplify for kids
                            thinking_text = msg.content
                            if len(thinking_text) > 150:
                                thinking_text = thinking_text[:150] + "..."
                            reasoning_steps.append(f"💭 **Cerveau de l'Agent:** \"{thinking_text}\"")
                            final_response = msg.content
                            with reasoning_container:
                                reasoning_placeholder.markdown("\n\n".join(reasoning_steps))
                            time.sleep(1.5)
                        # Check for tool calls in agent message
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get('name') if isinstance(tool_call, dict) else getattr(tool_call, 'name', None)
                                display_name = tool_display_names.get(tool_name, tool_name)
                                last_tool_used = display_name
                                args = tool_call.get('args') if isinstance(tool_call, dict) else getattr(tool_call, 'args', {})
                                
                                # Make tool selection simple for kids
                                if display_name == "Calculator":
                                    reasoning_steps.append(f"✋ **L'agent dit:** J'ai besoin de ma calculatrice! 🧮")
                                    reasoning_steps.append(f"   (Je dois calculer: {args})")
                                elif display_name == "Internet Search":
                                    reasoning_steps.append(f"✋ **L'agent dit:** J'ai besoin de chercher sur Internet! 🌐")
                                    reasoning_steps.append(f"   (Je cherche: {args})")
                                else:
                                    reasoning_steps.append(f"✋ **L'agent dit:** J'utilise {display_name}!")
                                
                                with reasoning_container:
                                    reasoning_placeholder.markdown("\n\n".join(reasoning_steps))
                                time.sleep(1.5)
                if "tools" in step:
                    # Tool results
                    for tool_result in step["tools"]["messages"]:
                        if hasattr(tool_result, 'content'):
                            result_text = str(tool_result.content)
                            # Simplify result for kids
                            if len(result_text) > 100:
                                result_text = result_text[:100] + "..."
                            reasoning_steps.append(f"⚙️ **Résultat:** {result_text}")
                            with reasoning_container:
                                reasoning_placeholder.markdown("\n\n".join(reasoning_steps))
                            time.sleep(1.5)
            
            assistance_response = final_response if final_response else "No response received"
        except Exception as e:
            assistance_response = f"Error: {str(e)}"
        
        # Clear a line and display tool used prominently in BIG letters
        st.markdown("")
        if last_tool_used:
            st.markdown(f"""
            <div style="text-align: center; background-color: #FFD700; padding: 20px; border-radius: 10px; border: 3px solid #FFA500;">
                <h1 style="color: #FF6B6B; margin: 0;">🎉 L'AGENT A CHOISI UN OUTIL! 🎉</h1>
                <h2 style="color: #4ECDC4; margin: 10px 0;">🔧 {last_tool_used}</h2>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")
        
        # Display the final response
        st.markdown("### 💡 Voici la réponse:")
        message_placeholder = st.empty()
        
        # Simulate a streaming response with a slight delay
        for chunk in str(assistance_response).split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")

        # Display the full response
        message_placeholder.info(full_response)
    
    # Add the assistant's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OPENAI"


## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant . Please repsonse to the user queries"),
        ("user","Question:{question}")
    ]
)


def generate_response(question,api_key,engine,temperature,max_tokens):
    llm=ChatOpenAI(model=engine,temperature=temperature,max_tokens=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.stream({'question':question})
    return answer

## #Title of the app
st.title("Enhanced Q&A Chatbot With OpenAI")

## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your OpenAI API Key:",type="password")
lang_chain_api_key=st.sidebar.text_input("Enter your Langchain API Key:",type="password")
## Select the OpenAI model
engine=st.sidebar.selectbox("Select Open AI model",["gpt-4o","gpt-4-turbo","gpt-4"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

os.environ["LANGCHAIN_API_KEY"]=lang_chain_api_key

## MAin interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input and api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    response=generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the Open AI API Key in the sider bar")
else:
    st.write("Please provide the user input")
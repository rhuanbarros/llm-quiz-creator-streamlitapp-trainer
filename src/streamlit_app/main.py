import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import random
import numpy as np

from supabase import create_client, Client
import json

import logging
import sys

# not working
# logging.basicConfig(level=print,  # Define o nível de log
#                     format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
#                     stream=sys.stdout)  # Define a saída do log para stdout
#                     # filename='app.log',  # Define o arquivo onde os logs serão gravados
#                     # filemode='a')  # Define o modo de escrita do arquivo de log (append)



url = "https://xoxlgvakygiyfijfeixu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveGxndmFreWdpeWZpamZlaXh1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNDkyNzU2NywiZXhwIjoyMDIwNTAzNTY3fQ.V3766GRj6hkt1Ci-52tjSiULVoF3nfCPPDnR6Hc_rT0"

supabase: Client = create_client(url, key)

st.set_page_config(
    page_title="Machine Learning Interview Preparation Trainer",
    page_icon="💪",
)

st.write(
    """
    # Machine Learning Interview Preparation Trainer
    """
)

PAGE_CONFIG_TRAIN = 0
PAGE_QUESTION = 1

if "first_run" not in st.session_state:
    st.session_state.first_run = True
    
if "page_show" not in st.session_state:
    st.session_state.page_show = PAGE_CONFIG_TRAIN
    
if "question" not in st.session_state:
    st.session_state.question = "None"

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None



def show_config_train():
    pass

def load_question():
    response = supabase.table('get_question').select("*").execute()
    if len(response.data):
        st.session_state.question = response.data[0]
    
        print("----------------- QUESTION LOADED -----------------")
        print(st.session_state.question)
        print("----------------- QUESTION LOADED -----------------")
    else:
        
    
def on_click_verify_answer(answer):
    question = st.session_state.question
    
    
    if answer == question["answer"]:
        correct_answer = "True"
    else:
        correct_answer = "False"
        # if user selected the wrong answer, make the question show again later
        data, count = supabase.table('questions').update({"show_again": True}).eq('id', question["id"]).execute()
        
    data, count = supabase.table('answers').insert({"question_id": question["id"], "correct_answer": correct_answer}).execute()
    
    st.session_state.show_explanation = True
    
def on_click_next():
    st.session_state.show_explanation = False
    load_question()
       


def show_question():
    question = st.session_state.question["question"]
    st.write(
        rf"""
        #### {question}
        """
    )
        
    _, col2, col3, _ = st.columns([9,3,3,9])    
    col2.button("False", key="btn_false", on_click=on_click_verify_answer, args=["FALSE"])
    col3.button("True", key="btn_true", on_click=on_click_verify_answer, args=["TRUE"])
    
def show_explanation():
    if st.session_state.correct_answer:
        st.success("Correct answer!")
    else:
        st.error("Wrong answer!")
        
    explanation = st.session_state.question["explanation"]
    st.write(
        rf"""
        #### Explanation
        """
    )
    
    # container = st.container()

    st.info(f'{explanation}', icon="ℹ️")
    
    st.button("Next", on_click=on_click_next)

# match st.session_state.page_show:
#     case 0:
#         show_config_train()
#     case 1:
#         show_question()
    
if st.session_state.first_run:
    load_question()
    st.session_state.first_run = False
    
show_question()

if st.session_state.show_explanation:
    show_explanation()
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

FLOW_CONFIGURATION = 0
FLOW_QUESTION = 1
FLOW_RESULTS = 2

if "first_run" not in st.session_state:
    st.session_state.first_run = True
    
if "page_flow" not in st.session_state:
    st.session_state.page_flow = FLOW_QUESTION
    
if "question" not in st.session_state:
    st.session_state.question = None

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = []



def show_config_train():
    st.write(
        rf"""
        #### Configuration
        """
    )

def load_question():
    print("----------------- LOADING QUESTION FUNCTION ------------------")
    
    response = supabase.table('get_question').select("*").execute()
    if len(response.data) > 0:
        st.session_state.question = response.data[0]
    
        print("----------------- QUESTION LOADED -----------------")
        print(st.session_state.question)
        print("----------------- QUESTION LOADED -----------------")
    else:
        st.info("No more questions available")
        st.session_state.page_flow = FLOW_RESULTS
    
    # st.rerun()

    
        
    
def on_click_verify_answer(answer):
    question = st.session_state.question
    
    
    if answer == question["answer"]:
        correct_answer = True
        # if user selected the rigth answer, make the question not show again later
        data, count = supabase.table('questions').update({"show_again": False}).eq('id', question["id"]).execute()
    else:
        correct_answer = False
        # if user selected the wrong answer, make the question show again later
        data, count = supabase.table('questions').update({"show_again": True}).eq('id', question["id"]).execute()
        
    question["correct_answer"] = correct_answer
    
    st.session_state.answered_questions.append(question)
        
    data, count = supabase.table('answers').insert({"question_id": question["id"], "correct_answer": correct_answer}).execute()
    
    st.session_state.correct_answer = correct_answer
    st.session_state.show_explanation = True
    
def on_click_next():
    st.session_state.show_explanation = False
    load_question()
    # st.rerun()
    
def on_click_end_session():
    st.session_state.page_flow = FLOW_RESULTS
       


def show_question():
    if st.session_state.question is None:
        question = "Loading..."
    else:
        question = st.session_state.question["question"]
        
    st.write(
        rf"""
        #### {question}
        """
    )
        
    _, col2, col3, _ = st.columns([9,3,3,9])    
    col2.button("False", key="btn_false", on_click=on_click_verify_answer, args=["FALSE"])
    col3.button("True", key="btn_true", on_click=on_click_verify_answer, args=["TRUE"])
    
    st.button("Ends session", key="btn_end_session", on_click=on_click_end_session, )
    
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
    
    st.button("Elaborate more the explanation")
    st.button("Next", on_click=on_click_next)
    
def show_results():
    st.write(
        rf"""
        #### Resuls
        """
    )
    
    answered_questions = st.session_state.answered_questions
    df = pd.DataFrame(answered_questions)
    
    correct_mask = df['correct_answer'] == 1
    correct_df = df.loc[ correct_mask ].groupby(["subject_matter_1", "level"])['correct_answer'].sum().reset_index()
    incorrect_mask = df['correct_answer'] == 0
    incorrect_df = df.loc[ incorrect_mask ].groupby(["subject_matter_1", "level"])['correct_answer'].count().reset_index()
    incorrect_df = incorrect_df.rename(columns={"correct_answer": "incorrect_answer"})
    
    df_results = pd.merge(correct_df, incorrect_df, on=["subject_matter_1", "level"], how='outer')
    df_results.fillna(0, inplace=True)
    df_results["correct_answer"] = df_results["correct_answer"].astype(int)
    df_results["incorrect_answer"] = df_results["incorrect_answer"].astype(int)
    df_results

    st.button("Start over again")
    

match st.session_state.page_flow:
    case 0: # FLOW_CONFIGURATION
        show_config_train()
    
    case 1: # FLOW_QUESTION
        if st.session_state.first_run:
            st.session_state.first_run = False
            load_question()
            
        show_question()

        if st.session_state.show_explanation:
            show_explanation()
    
    case 2: # FLOW_RESULTS
        show_results()
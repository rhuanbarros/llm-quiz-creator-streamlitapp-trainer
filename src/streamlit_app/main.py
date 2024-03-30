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
    st.session_state.page_flow = FLOW_CONFIGURATION
    
if "question" not in st.session_state:
    st.session_state.question = None

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = []

if "subject_matter_1s_list_selected" not in st.session_state:
    st.session_state.subject_matter_1s_list_selected = []

if "topic_descriptions_list_selected" not in st.session_state:
    st.session_state.topic_descriptions_list_selected = []

if "use_subject_matter_1_filter" not in st.session_state:
    st.session_state.use_subject_matter_1_filter = True

if "questions_available" not in st.session_state:
    st.session_state.questions_available = False

# WHEN ADD A NEW STATE VARIABLE, UPDATE THE RESET FUNCTION on_click_start_over_again


@st.cache_resource
def get_subject_matter_1s():
    response = supabase.table('get_subject_matter_1s').select("*").execute()
    data_list = ["All"]
    for row in response.data:
        data_list.append(row["subject_matter_1"])
    
    return data_list

@st.cache_resource
def get_topic_descriptions():
    response = supabase.table('get_topic_descriptions').select("*").execute()
    data_list = ["All"]
    for row in response.data:
        data_list.append(row["topic_description"])
    
    return data_list

def on_click_start(subject_matter_1s_list_selected, topic_descriptions_list_selected, use_subject_matter_1_filter):
    st.session_state.subject_matter_1s_list_selected = subject_matter_1s_list_selected
    st.session_state.topic_descriptions_list_selected = topic_descriptions_list_selected
    st.session_state.use_subject_matter_1_filter = use_subject_matter_1_filter
    
    st.session_state.page_flow = FLOW_QUESTION

def show_config_train():
    st.write(
        rf"""
        #### Configuration
        """
    )
    subject_matter_1s_list = get_subject_matter_1s()
    topic_descriptions_list = get_topic_descriptions()
    
    subject_matter_1s_list_selected = st.multiselect("Subject matter 1", subject_matter_1s_list, ["All"])
    topic_descriptions_list_selected = st.multiselect("Topic description", topic_descriptions_list, ["All"])
    
    st.button("Start Subject matter 1", on_click=on_click_start, args=[subject_matter_1s_list_selected, topic_descriptions_list_selected, True])
    st.button("Start Topic description", on_click=on_click_start, args=[subject_matter_1s_list_selected, topic_descriptions_list_selected, False])


def load_question():
    print("----------------- LOADING QUESTION FUNCTION ------------------")
    
    subject_matter_1s_list_selected = st.session_state.subject_matter_1s_list_selected
    topic_descriptions_list_selected = st.session_state.topic_descriptions_list_selected
    use_subject_matter_1_filter = st.session_state.use_subject_matter_1_filter
    
    if use_subject_matter_1_filter:
        if "All" in subject_matter_1s_list_selected:
            subject_matter_1s_list_selected.remove("All")
            
        if len(subject_matter_1s_list_selected) > 0:
            response = supabase.table('get_question').select("*").in_("subject_matter_1", subject_matter_1s_list_selected).eq('show_again', True).is_('answer_id', 'null').execute()
        else:
            response = supabase.table('get_question').select("*").eq('show_again', True).is_('answer_id', 'null').execute()        
    else:        
        if "All" in topic_descriptions_list_selected:
            topic_descriptions_list_selected.remove("All")
            
        if len(topic_descriptions_list_selected) > 0:
            response = supabase.table('get_question').select("*").in_("topic_description", topic_descriptions_list_selected).eq('show_again', True).is_('answer_id', 'null').execute()
        else:
            response = supabase.table('get_question').select("*").eq('show_again', True).is_('answer_id', 'null').execute()
    
    if len(response.data) > 0:
        st.session_state.question = response.data[0]
        
        st.session_state.questions_available = True
    
        print("----------------- QUESTION LOADED -----------------")
        print(st.session_state.question)
        print("----------------- QUESTION LOADED -----------------")
        
    else:
        st.info("No more questions available")
        st.session_state.no_more_questions_available = True
        st.session_state.page_flow = FLOW_RESULTS

    
        
    
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
    questions_available = st.session_state.questions_available
    
    if questions_available:
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
    else:
        st.button("Start over again", on_click=on_click_start_over_again)
    
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
    
def on_click_start_over_again():
    # reset app state
    st.session_state.first_run = True
    st.session_state.page_flow = FLOW_CONFIGURATION
    st.session_state.question = None
    st.session_state.show_explanation = False
    st.session_state.correct_answer = None
    st.session_state.answered_questions = []
    st.session_state.subject_matter_1s_list_selected = []
    st.session_state.topic_descriptions_list_selected = []
    st.session_state.use_subject_matter_1_filter = True
    st.session_state.questions_available = False
    
def show_results():
    st.write(
        rf"""
        #### Resuls
        """
    )
    
    answered_questions = st.session_state.answered_questions
    df = pd.DataFrame(answered_questions)
    
    if df.shape[0] > 0:        
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

    st.button("Start over again", on_click=on_click_start_over_again)
    

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
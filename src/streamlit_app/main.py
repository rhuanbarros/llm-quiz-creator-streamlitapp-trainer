import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import random
import numpy as np

from supabase import create_client, Client
import json

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

if "page_show" not in st.session_state:
    st.session_state.page_show = PAGE_CONFIG_TRAIN
    
if "question" not in st.session_state:
    st.session_state.question = "None"



def show_config_train():
    pass

def load_question():
    response = supabase.table('questions').select("*").limit(1).execute()
    st.session_state.question = response.data[0]


def show_question():
    question = st.session_state.question["question"]
    st.markdown(
        f"""
        ## {question}
        """
    )


# match st.session_state.page_show:
#     case 0:
#         show_config_train()
#     case 1:
#         show_question()
    
    
load_question()
show_question()
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import random
import numpy as np

st.set_page_config(
    page_title="Machine Learning Interview Preparation Trainer",
    page_icon="💪",
)

st.write(
    """
    # Machine Learning Interview Preparation Trainer"
    """
)

PAGE_CONFIG_TRAIN = 0
PAGE_QUESTION = 1

if "page_show" not in st.session_state:
    st.session_state.page_show = PAGE_CONFIG_TRAIN



def show_config_train():
    pass

def load_question():
    pass


def show_question():
    pass


match st.session_state.page_show:
    case 0:
        show_config_train()
    case 1:
        show_question()
        
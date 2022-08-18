import streamlit as st
import nltk
import helpy
from components.preprocess import getMostCommonFeatures
from components.util import loadFiles, transformData, readRawData
import pickle

##########
# CONFIG #
##########
st.set_page_config(page_title="Lixplore", page_icon="🔍", initial_sidebar_state="expanded")

helpy.init_session_state(
    data = transformData(readRawData()),
    pdf_files = loadFiles("../pdfs/", "pdf")
)  

###########
# SIDEBAR #
###########

with st.sidebar:
    st.title("🔍 Lixplore")
    st.caption("Made with ❤️")
    st.caption("[Source](https://github.com/dunder-1/Lixplore)")

###########
# CONTENT #
###########

helpy.greet()
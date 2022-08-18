import streamlit as st
import pdfplumber
import nltk
import helpy, components
from components.preprocess import PdfFile, getMostCommonFeatures
from components.train import LabeledText
from components.evaluation import loadClassifier
from components.util import loadFiles, transformData, readRawData
import re, pickle, random

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

METHODS = ["Introduction", "Look into dataset", "View metrics by literature", "Extract text of pdf", "Show info about classifier"]


st.title("🕵️ Get Insights")

method = st.radio("Select method", METHODS)     
st.write("---")

if method == "Introduction":
    helpy.greet(with_hello=False)

if method == "Look into dataset":
    st.caption(f"Found {len(st.session_state.data)} rows (=Unique Metrics-Indicator-Activity-Event Combo)")
    # hide table row index
    st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
    st.table(st.session_state.data)

elif method == "View metrics by literature":
    st.write("""
        Select a scientific literature to find out which Learning Events, Activities, Indicators and Metrics can be
        found in the text (according to the dataset).
        """)

    file_path = st.selectbox("Select PDF File:", st.session_state.pdf_files)
    tbl_info = [i for i in st.session_state.data if PdfFile.getCitation(file_path) in i["citation"]]

    if tbl_info:
        st.caption(f"Found {len(tbl_info)} metrics")
        # hide table row index
        st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
        st.table(tbl_info)
    else:
        st.error("Can't find any information for the selected literature!")

elif method == "Extract text of pdf":

    pdf_file = PdfFile.read(st.selectbox("Select PDF File:", st.session_state.pdf_files))
    if pdf_file.is_two_column:
        st.caption("(Pdf is two column)")
    else: 
        st.caption("(Pdf is single column)")
    st.write("---")

    for page in pdf_file.extracted_pages:
        st.write(page)

elif method == "Show info about classifier":

    st.write("I found these classifiers:")

    classifiers = loadClassifier("*")

    st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
    st.table(sorted([i.asDictTable() for i in classifiers], key=lambda x: x["accuracy"], reverse=True))
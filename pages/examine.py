import streamlit as st
import pdfplumber
import nltk
import helpy, components
from components.preprocess import PdfFile, getMostCommonFeatures
from components.train import LabeledText
from components.evaluation import loadClassifier
from components.util import loadFiles
import re, pickle, random

METHODS = ["Introduction", "Look into dataset", "View metrics by literature", "Extract text of pdf", "Show word features", "Show info about classifier"]

def renderPage():
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
        st.caption("(Pdf is two column)") if pdf_file.is_two_column else st.caption("(Pdf is single column)")
        st.write("---")

        for page in pdf_file.extracted_pages:
            st.write(page)

    elif method == "Show word features":

        #with open("../pdfs/extracted_text/[99] 2883851.2883907.pickle", "rb") as file:
        #    st.write(pickle.load(file))
        st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
        st.table([{"word":i[0], "count":i[1]} for i in st.session_state.most_common_features])


    elif method == "Show info about classifier":

        st.write("I found these classifiers:")

        classifiers = loadClassifier("*")

        st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
        st.table(sorted([i.asDictTable() for i in classifiers], key=lambda x: x["accuracy"], reverse=True))
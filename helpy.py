import streamlit as st
import nltk
import pdfplumber
import json, os, re
import components

#nltk.download("punkt")
#nltk.download("stopwords")
#nltk.download('averaged_perceptron_tagger')

def greet(with_hello=True):
    st.header("Hello 👋") if with_hello else None
    st.write("This tool provides the ability to automatically extract metrics of scientific literature.")
    st.subheader("The algorithm")
    st.write("""
        The algorithm performs the following steps:
        1. Extract the text of the literature (in PDF format)
        2. Identify specific words (metrics and/or indicators) from the text.
        3. Categorize the metrics into indicators
        4. Categorize the indicators into learning activities of the learning events
        """)
    st.write("[Github Repo](https://github.com/dunder-1/Lixplore)")

def getReferences():
    with open("../references.txt", "r", encoding="utf-8") as file:
        return [i for i in file.readlines() if len(i) > 3]

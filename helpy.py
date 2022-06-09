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
    st.subheader("Tutorial")
    st.write("""
        Use the links in the navigation bar on the left.
        - Exercise: Extract and label the text and/or train a classifier
        - Extract: Use the trained classifier to look for relevant information in the text
        - Examine: Dive into the data and get insights about the classifier
    """)
    st.subheader("The algorithm")
    st.write("""
        The algorithm performs the following steps:
        1. Extract the text of the literature (in PDF format)
        2. Search for relevant words in the extracted text
        2. Identify learning metrics/indicators/activities/events from the text.
        """)
    st.write("[Github Repo](https://github.com/dunder-1/Lixplore)")

def getReferences():
    with open("../references.txt", "r", encoding="utf-8") as file:
        return [i for i in file.readlines() if len(i) > 3]

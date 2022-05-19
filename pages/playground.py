import streamlit as st
import nltk
import pickle
import helpy
from components import *

def setFeatures(word_tokens:list[str], mcf):
    word_tokens = set(word_tokens)
    features = {}
    for word, count in mcf:
        features[f"contains({word})"] = word in word_tokens
    return features

def renderPage():
    st.title("🧸 Playground")

    with open("../classifier/event/labeled_literature_rmsw_WordNetLemmatizer.pickle", "rb") as file:
        x = pickle.load(file)

    st.write(x.labeled_literature[1])

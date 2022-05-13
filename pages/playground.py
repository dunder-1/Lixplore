import streamlit as st
import nltk
import helpy, components



def renderPage():
    st.title("🧸 Playground")

    st.write("You can test diffrent algorithms here.")


    st.code('components.filterSinglePage(page, remove_stopwords=True, stemming_algo="PorterStemmer")')

    st.write("page =")
    page = st.text_input("Text to filter:")
    remove_stopwords = st.checkbox("Remove Stopwords?")
    stemming_algo = st.radio("Select stemming algo:", [None]+components.STEMMING_ALGOS)

    st.write("Output =")
    st.write(components.filterSinglePage(page, remove_stopwords=remove_stopwords, stemming_algo=stemming_algo))

    st.write(components.filterPages([page], out_type=str, remove_stopwords=remove_stopwords, stemming_algo=stemming_algo))
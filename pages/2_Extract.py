import streamlit as st
import pdfplumber
import os, pickle
import helpy
from components.preprocess import PdfFile, getMostCommonFeatures
from components.train import getLabels
from components.evaluation import ClassifierFile, loadClassifier
from components.util import loadFiles, readRawData, transformData

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


CUT_OFF = -45.0



st.title("📄 Extract information of PDFs")

st.write("""
        Choose a pdf file to read the text and output the most probable Learning Event. 
        The following operations might be executed on the content of the pdf (depending on the trained classifier):
        - Tokenization
        - Removal of Stopwords and additional words
        - Stemming
        It might take a moment.
        """)

col1, col2 = st.columns(2)
selection_method = col1.radio("Choose the selection method:", ["Existing PDF", "Upload PDF"])
intelligent_extraction = col2.radio(
    "Try new extraction method?",
    [True, False],
    format_func = lambda x: "yes" if x else "no",
    index = 1
)
extraction_done = False

with st.form("extract"):
    if selection_method == "Existing PDF":
        pdf_file = st.selectbox("Select PDF File:", st.session_state.pdf_files)
    elif selection_method == "Upload PDF":
        pdf_file = st.file_uploader("Upload PDF File:", ["pdf"])

    st.caption("What do you want to extract?")
    col1, col2, col3, col4 = st.columns(4)
    extract_what = {
        "event": col1.checkbox("Events", disabled = intelligent_extraction),
        "activity": col2.checkbox("Activities", disabled = intelligent_extraction),
        "indicator": col3.checkbox("Indicators", disabled = intelligent_extraction),
        "metric": col4.checkbox("Metrics", disabled = intelligent_extraction)
    }

    if intelligent_extraction:
        extract_what = st.radio(
            "Choose the minimum label type to predict by machine learning. The higher level labels will then be predicted by occurences.",
            ("activity", "indicator"),
            help = "For example: If you choose 'indicator' i will predict 'event' and 'activity' by occurences."
        )

        extract_what = {extract_what: True}


    if st.form_submit_button("Extract"):            

        if not intelligent_extraction and not any(extract_what.values()):
            st.warning("Check at least one box or use new extraction method.")
        elif not pdf_file:
            st.error("Please provide a pdf file!")
        else:

            for label_type in [key for key in extract_what if extract_what[key]]:
                classifier = loadClassifier(label_type)
                most_common_features = getMostCommonFeatures(loadFiles("../pdfs/extracted_text/", "pickle", open_pickle=True),
                                                                remove_stopwords=classifier.remove_stopwords,
                                                                stemming_algo=classifier.stemming_algo)
                guessed_labels = classifier.classifyPDF(pdf_file, most_common_features)
                guessed_labels_sorted = sorted(guessed_labels.__dict__["_prob_dict"].items(), key=lambda x:x[1], reverse=True)
                guessed_labels_filtered = [{"label":i[0], "prediction":i[1]} for i in guessed_labels_sorted if i[1] > CUT_OFF]

                st.write(f"Most probable {label_type}s:")
                st.caption("Hint: Values closer to 0 are better")
                
                st.table(guessed_labels_filtered)
                
                if selection_method == "Existing PDF":
                    actual_labels = getLabels(st.session_state.data, PdfFile.getCitation(pdf_file), label_type)                

                    st.write("Label(s) according to the data:", actual_labels)
                    st.write("---")

            extraction_done = True

if intelligent_extraction and extraction_done:
    extract_what_label = extract_what.popitem()[0]
    st.write(f"According to the extracted {extract_what_label}, the following higher level labels are the most probable.")
    st.write("You can find a sorted table down below.")

    extracted_collection = dict()
    for guessed_label in guessed_labels_filtered:
        _label = guessed_label["label"].lower()
        for elem in st.session_state.data:
            if elem[extract_what_label] == _label:   
                if elem["event"] not in extracted_collection:
                    extracted_collection[elem["event"]] = dict()
                if elem["activity"] not in extracted_collection[elem["event"]]:
                    extracted_collection[elem["event"]][elem["activity"]] = dict()
                if elem["indicator"] not in extracted_collection[elem["event"]][elem["activity"]]:
                    extracted_collection[elem["event"]][elem["activity"]][elem["indicator"]] = 0
                                   
                extracted_collection[elem["event"]][elem["activity"]][elem["indicator"]] += 1

    
    #st.write(extracted_collection)
    if extract_what_label == "indicator":
        extracted_collection = [
                {
                    "Event": event, "Activity": activity, 
                    "Occurences": sum(occurences for _, occurences in indicators.items())    
                }
                for event, activities in extracted_collection.items()
                for activity, indicators in activities.items()

            ]

    elif extract_what_label == "activity":
        extracted_collection = [
                {
                    "Event": event, 
                    "Occurences": sum(occurences for activity, indicators in activities.items() for _, occurences in indicators.items())
                }
                for event, activities in extracted_collection.items()
            ]
        

    st.table(
        extracted_collection
    )

    with st.expander("Sorted by occurences:"):
        sorted_collection = sorted(
            extracted_collection,
            key = lambda x: x["Occurences"],
            reverse = True
        )
        st.table(
            sorted_collection
        )

                           
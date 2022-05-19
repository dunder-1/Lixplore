import streamlit as st
import pdfplumber
import os, pickle
import helpy
from components.preprocess import PdfFile
from components.train import getLabels
from components.evaluation import ClassifierFile, loadClassifier
from components.util import loadFiles

def renderPage():
    st.title("📄 Extract Learning Events of PDFs")

    st.write("""
            Choose a pdf file to read the text and output the most probable Learning Event. 
            The following operations will be executed on the content of the pdf:
            - Tokenization
            - Removal of Stopwords
            - Stemming
            It might take a moment.
            """)

    #st.markdown("<style> .st-co, .st-dy, .st-bd {flex-direction: row; gap: 20px}</style>", unsafe_allow_html=True)
    selection_method = st.radio("Choose the selection method:", ["Existing PDF", "Upload PDF"])
    #classifier_type = st.selectbox("Select Classifier type", ["event", "indicator", "activity", "metric"])

    with st.form("extract"):
        if selection_method == "Existing PDF":
            pdf_file = st.selectbox("Select PDF File:", st.session_state.pdf_files)
        elif selection_method == "Upload PDF":
            pdf_file = st.file_uploader("Upload PDF File:", ["pdf"])

        st.caption("What do you want to extract?")
        col1, col2, col3, col4 = st.columns(4)
        extract_what = {
            "event": col1.checkbox("Events"),
            "activity": col2.checkbox("Activities"),
            "indicator": col3.checkbox("Indicators"),
            "metric": col4.checkbox("Metrics")
        }

        if st.form_submit_button("Extract"):

            if not any(extract_what.values()):
                st.warning("Check at least one box!")
            elif not pdf_file:
                st.error("Please provide a pdf file!")
            else:

                for label_type in [key for key in extract_what if extract_what[key]]:
                    classifier = loadClassifier(label_type)
                    guessed_labels = classifier.classifyPDF(pdf_file, st.session_state.most_common_features)
                    guessed_labels_sorted = sorted(guessed_labels.__dict__["_prob_dict"].items(), key=lambda x:x[1], reverse=True)

                    st.write(f"Most probable {label_type}s:")
                    st.caption("Hint: Values closer to 0 are better")
                    
                    
                    st.table([{"label":i[0], "prediction":i[1]} for i in guessed_labels_sorted if i[1] > -45.0])
                    
                    if selection_method == "Existing PDF":
                        actual_labels = getLabels(st.session_state.data, PdfFile.getCitation(pdf_file), label_type)
                        """
                        if guessed_label in actual_labels:
                            st.success("This is correct!")
                        else:
                            st.error("Unfortunately not correct!")
                        """

                        st.write("Label(s) according to the data:", actual_labels)
                        st.write("---")                  

                #with st.expander("Show extracted text"):
                #    for i, p in enumerate(PdfFile.read(pdf_file).extracted_pages, start=1):
                #        st.subheader(f"Page {i}")
                #        st.write(p)

                """
                with st.expander("Show extracted text after pre processing"):
                    for i, p in enumerate(components.filterPages(pages, out_type=list, stemming_algo=stemming_algo), start=1):
                        st.subheader(f"Page {i}")
                        st.write(p)
                """
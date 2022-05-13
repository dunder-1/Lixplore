import streamlit as st
import pdfplumber
import os, pickle
import helpy, components

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

        st.caption("Configuration of selected classifier:")
        #st.code(f"remove_stopwords = {remove_stopwords}\nstemming_algo = {stemming_algo}")

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
            else:

                if selection_method == "Existing PDF":

                    for label_type in [key for key in extract_what if extract_what[key]]:
                        classifier, remove_stopwords, stemming_algo = components.loadClassifier(st.session_state.best_classifier[label_type])
                        guessed_label, pages = components.classifyPDF(classifier, remove_stopwords, stemming_algo, pdf_file)
                        st.write(f"Most probable {label_type}: **{guessed_label}**")
                        actual_labels = components.filterDataByCitation(st.session_state.data, pdf_file[8:].split()[0], label_type)
                        st.write(f"For label type {label_type}")
                        if guessed_label in actual_labels:
                            st.success("This is correct!")
                        else:
                            st.error("Unfortunately not correct!")

                        st.write(f"The actual {label_type}s are:", actual_labels)
                        st.write("---")
                    
                    

                    

                with st.expander("Show extracted text"):
                    for i, p in enumerate(pages, start=1):
                        st.subheader(f"Page {i}")
                        st.write(p)

                with st.expander("Show extracted text after pre processing"):
                    for i, p in enumerate(components.filterPages(pages, out_type=list, stemming_algo=stemming_algo), start=1):
                        st.subheader(f"Page {i}")
                        st.write(p)
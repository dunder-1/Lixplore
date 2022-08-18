import streamlit as st
import nltk
import helpy
from components.preprocess import PdfFile, TRASH, getMostCommonFeatures
from components.train import LABEL_TYPES, STEMMING_ALGOS, LabeledLiteratureFile
from components.evaluation import ClassifierFile
from components.util import loadFiles, readRawData, transformData
import pickle, os, random

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


st.title("🤹 Train the algorithm")

st.write("""
        The machine learning algorithm can be trained here. It is necessary to
        1. add the new document(s) in the folder `../pdfs/` 
            - (please use the correct naming convention: "[x] name.pdf" where x is the citation nr)
        2. expand the file `../data.json` with the documents metrics, indicators, activities and events.
        If this is done correctly the number of found pdfs below should be updated (default is 98 pdfs).
        """)
st.write("Finally a click on *Start* starts the selected process. It might take a moment.")

col1, col2= st.columns(2)
col1.caption("Preprocessing:")
run_training = False
extract_pdf = col1.checkbox("Extract text", 
                            help="""
                                Extracts text of all pdf files in ../pdfs/ and saves them into ../pdfs/extracted_text/
                            """)
label_text = col1.checkbox("Label text", 
                            help="""
                                Labels all texts of ../pdfs/extracted_text/ and saves them into ../classifier/<label_type>/
                            """)
col2.caption("Training:")
run_training = col2.checkbox("Run Training", 
                                disabled=label_text or extract_pdf,
                                help="""
                                Runs a training on all labeled literature files of ../classifier/<label_type>/
                                and saves the trained classifier into ../classifier/
                                """)

classifiers = []

with st.form("train_model"):

    with st.expander("Show data:"):
        st.table(st.session_state.data)

    if not any([extract_pdf, label_text, run_training]):
        st.warning("Please select at least one option above!")

    if extract_pdf:
        with st.expander(f"Show {len(st.session_state.pdf_files)} pdfs:"):
            st.write(st.session_state.pdf_files)

    if label_text:

        remove_stopwords = st.checkbox("Remove Stopwords?", value=label_text)
        stemming_algo = st.radio("Select Stemming Algorithm:", STEMMING_ALGOS, index=1)
        label_types = st.multiselect("Select Label Types", LABEL_TYPES, default=LABEL_TYPES, help="You can select multiple Types")

    elif run_training:
        classifier_label_type = st.radio("Train classifier to classify...", LABEL_TYPES)

    if st.form_submit_button("Start"):  
        
        if extract_pdf:
            st.info("Extracting text from pdf...")
            folder_extracted_text = "../pdfs/extracted_text/"
            extract_prog_bar = st.progress(0)
            for i, pdf_file_path in enumerate(st.session_state.pdf_files, start=1):
                extract_prog_bar.progress(i/len(st.session_state.pdf_files))
                pdf_file = PdfFile.read(pdf_file_path)
                with open(folder_extracted_text+pdf_file.path[8:-4]+".pickle", "wb") as file:
                    pickle.dump(pdf_file, file)
            st.success("Succesfully extracted text!")

        if label_text:
            st.info("Labeling the extracted text...")
            label_prog_bar, i = st.progress(0), 0
            most_common_features = getMostCommonFeatures(loadFiles("../pdfs/extracted_text/", "pickle", open_pickle=True),
                                                            remove_stopwords=remove_stopwords,
                                                            stemming_algo=stemming_algo)
            for label_type in label_types:
                rmsw = "rmsw" if remove_stopwords else "sw"
                path = f"../classifier/{label_type}/labeled_literature_{rmsw}_{stemming_algo}.pickle"
                lab_lit_file = LabeledLiteratureFile(path, label_type, remove_stopwords, stemming_algo, extra_removal=TRASH, labeled_literature=[])

                for file_path in loadFiles("../pdfs/extracted_text/", "pickle"):
                    with open(file_path, "rb") as file:
                        extracted_text = pickle.load(file)
                    lab_lit_file.assignLiterature(extracted_text, st.session_state.data, most_common_features)
                    i += 1
                    label_prog_bar.progress(i/(len(loadFiles("../pdfs/extracted_text/", "pickle"))*len(label_types)))
                
                with open(lab_lit_file.path, "wb") as file:
                    pickle.dump(lab_lit_file, file)

            st.success("Successfully labeled the extracted text!")
        
        elif run_training:

            st.info("Running training...")
            best_classifier, best_acc = None, -1.0
            training_prog_bar, i = st.progress(0), 0
            for file_path in loadFiles(f"../classifier/{classifier_label_type}/", "pickle"):
                #st.caption(f"file: {file_path}")
                with open(file_path, "rb") as file:
                    lab_lit_file = pickle.load(file)

                #st.write(lab_lit_file.labeled_literature[0].asTuple())

                for train_test_split in range(20, 81, 20):
                    classifier = ClassifierFile.fromLabeledLiteratureFile(lab_lit_file, train_test_split)
                    
                    classifiers.append(classifier.asDictTable())
                    if classifier.accuracy > best_acc:
                        best_classifier, best_acc = classifier, classifier.accuracy
                    i += 1
                    training_prog_bar.progress(i/(len(range(20, 81, 20))*len(loadFiles(f"../classifier/{classifier_label_type}/", "pickle"))))

            st.success("Training completed successfully!")
            st.write("Accuracy of Classifier:", best_classifier.accuracy)
            
            with open(best_classifier.path, "wb") as file:
                pickle.dump(best_classifier, file)

if classifiers:
    st.table(sorted(classifiers, key=lambda x: x["accuracy"], reverse=True))
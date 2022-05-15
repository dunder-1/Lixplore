import streamlit as st
import nltk
import helpy
from components.preprocess import PdfFile
from components.train import LABEL_TYPES, STEMMING_ALGOS, LabeledLiteratureFile, getLabeledTexts
from components.evaluation import ClassifierFile
from components.util import loadFiles
import pickle, os, random

def renderPage():
    st.title("🤹 Train the algorithm")

    st.write("""
            The machine learning algorithm can be trained here. It is necessary to
            1. add the new document(s) in the folder `../pdfs/` and
            2. to expand the file `../data.json` with the documents metrics, indicators, activities and events.
            If this is done correctly the number of found pdfs below should be updated (default is 97 pdfs).
            """)
    st.write("Finally a click on *Start Training* starts the training process. It might take a moment.")

    col1, col2= st.columns(2)
    col1.caption("Preprocessing:")
    run_training, get_best_classifier = False, False
    extract_pdf = col1.checkbox("Extract text")
    label_text = col1.checkbox("Label text")
    col2.caption("Training:")
    run_training = col2.checkbox("Run Training", disabled=label_text or extract_pdf)
    get_best_classifier = col2.checkbox("Get best classifier", disabled=label_text or extract_pdf)

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
            if not get_best_classifier:
                classifier_label_type = st.radio("Train classifier to classify...", LABEL_TYPES)
                

            else:
                st.caption("I will try to find the best classifier.")


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
                for label_type in label_types:
                    rmsw = "rmsw" if remove_stopwords else "sw"
                    path = f"../classifier/{label_type}/labeled_literature_{rmsw}_{stemming_algo}.pickle"
                    lab_lit_file = LabeledLiteratureFile(path, label_type, remove_stopwords, stemming_algo, labeled_literature=[])

                    for file_path in loadFiles("../pdfs/extracted_text/", "pickle"):
                        with open(file_path, "rb") as file:
                            extracted_text = pickle.load(file)
                        labeled_texts = getLabeledTexts(extracted_text, st.session_state.data, label_type, remove_stopwords, stemming_algo)
                        lab_lit_file.labeled_literature.extend(labeled_texts)
                        i += 1
                        label_prog_bar.progress(i/(len(loadFiles("../pdfs/extracted_text/", "pickle"))*len(label_types)))
                    
                    with open(lab_lit_file.path, "wb") as file:
                        pickle.dump(lab_lit_file, file)

                st.success("Successfully labeled the extracted text!")
            
            elif run_training:

                
                best_classifier, best_acc = None, -1.0
                for file_path in loadFiles(f"../classifier/{classifier_label_type}/", "pickle"):
                    #st.caption(f"file: {file_path}")
                    with open(file_path, "rb") as file:
                        lab_lit_file = pickle.load(file)

                    for train_test_split in range(20, 81, 20):
                        classifier = ClassifierFile.fromLabeledLiteratureFile(lab_lit_file, train_test_split)
                        
                        classifiers.append(classifier.asDictTable())
                        if classifier.accuracy > best_acc:
                            best_classifier, best_acc = classifier, classifier.accuracy

                st.success("Training completed successfully!")
                st.write("Accuracy of Classifier:", best_classifier.accuracy)
                
                with open(best_classifier.path, "wb") as file:
                    pickle.dump(best_classifier, file)

                

                #if get_best_classifier:
                #    st.session_state.best_classifier = getBestClassifer()

    st.table(sorted(classifiers, key=lambda x: x["accuracy"], reverse=True)) if classifiers else None
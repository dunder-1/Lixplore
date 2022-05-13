import streamlit as st
import nltk
import helpy, components
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

    with st.form("train_model"):
   
        with st.expander("Show data:"):
            st.table(st.session_state.data)

        if not any([extract_pdf, label_text, run_training]):
            st.warning("Please select at least one option above!")

        if extract_pdf:
            with st.expander(f"Show {len(components.getPdfFiles())} pdfs:"):
                st.write(components.getPdfFiles())

        if label_text:

            remove_stopwords = st.checkbox("Remove Stopwords?", value=label_text)
            stemming_algo = st.radio("Select Stemming Algorithm:", [None]+components.STEMMING_ALGOS, index=1)
            label_types = st.multiselect("Select Label Types", components.LABEL_TYPES, default=components.LABEL_TYPES, help="You can select multiple Types")

        elif run_training:

            labeled_file = st.selectbox("Select labeled literature file:", components.getLabeledFiles(out_type="list"), disabled=label_text,
                                                   help="rmsw = Removed Stopwords")
            train_test_split = st.slider("How many % of the labeled literature for training? (rest is for test!)", 20, 80, value=60, step=20)


        if st.form_submit_button("Start"):  
            
            if extract_pdf:
                st.info("Extracting text from pdf...")
                folder_extracted_text = "../pdfs/extracted_text/"
                extract_prog_bar = st.progress(0)
                for i, pdf_file in enumerate(components.getPdfFiles(), start=1):
                    extract_prog_bar.progress(i/len(components.getPdfFiles()))
                    with open(folder_extracted_text+pdf_file[8:-4]+".txt", "w", encoding="utf-8") as file:
                        file.write(" ".join(components.extractPdfText(pdf_file)))
                st.success("Succesfully extracted text!")

            if label_text:
                st.info("Labeling the extracted text...")
                label_prog_bar, i = st.progress(0), 0
                for label_type in label_types:
                    labeled_literature = []
                    for txt_file in components.getExtractedFiles():
                        labeled_text = components.labelExtractedText(txt_file, st.session_state.data, label_type, remove_stopwords, stemming_algo)
                        labeled_literature.extend(labeled_text)
                        i += 1
                        label_prog_bar.progress(i/(len(components.getExtractedFiles())*len(label_types)))

                    rmsw = "rmsw" if remove_stopwords else "sw"
                    with open(f"../classifier/{label_type}/labeled_literature_{rmsw}_{stemming_algo}.pickle", "wb") as file:
                        pickle.dump(labeled_literature, file)

                st.success("Succesfully labeled the extracted text!")
            
            elif run_training:
                
                with open(labeled_file, "rb") as file:
                    labeled_literature = pickle.load(file)

                random.shuffle(labeled_literature)
                train_set, test_set = labeled_literature[:train_test_split], labeled_literature[train_test_split:]
                classifier = nltk.NaiveBayesClassifier.train(train_set)
                accuracy = round(nltk.classify.accuracy(classifier, test_set), 2)                   

                st.success("Training completed successfully!")
                st.write("Accuracy of Classifier:", accuracy)

                classifier_file = labeled_file.replace("labeled_literature", "classifier")[:-7] + f"_{train_test_split}_{100-train_test_split}_{str(int(accuracy*100)).zfill(2)}"
                with open(classifier_file + ".pickle", "wb") as file:
                    pickle.dump(classifier, file)

                if get_best_classifier:
                    st.session_state.best_classifier = components.getBestClassifer()


                

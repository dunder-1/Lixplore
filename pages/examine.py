import streamlit as st
import pdfplumber
import nltk
import helpy, components
import re, pickle, random   

METHODS = ["Introduction", "Look into dataset", "View metrics by literature", "Extract text of pdf"]#, "Determine best training setting"]

def renderPage():
    st.title("🕵️ Get Insights")

    method = st.radio("Select method", METHODS)     
    st.write("---")

    if method == "Introduction":
        helpy.greet(with_hello=False)

    if method == "Look into dataset":
        st.caption(f"Found {len(st.session_state.data)} rows (=Unique Metrics-Indicator-Activity-Event Combo)")
        # hide table row index
        st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
        st.table(st.session_state.data)

    elif method == "View metrics by literature":

        st.write("""
            Select a scientific literature to find out which Learning Events, Activities, Indicators and Metrics can be
            found in the text (according to the dataset).
            """)
        
        sel_reference = st.selectbox("Select Literature", st.session_state.references, index=40)
        tbl_info = [i for i in st.session_state.data if re.findall(r"\[\d+\]", sel_reference)[0] in i["indicator"]]

        if tbl_info:
            st.caption(f"Found {len(tbl_info)} metrics")
            # hide table row index
            st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
            st.table(tbl_info)
        else:
            st.error("Can't find any information for the selected literature!")

    elif method == "Extract text of pdf":

        pdf_file = st.selectbox("Select PDF File:", st.session_state.pdf_files, index=2)
        two_col = components.isPdfTwoColumn("../pdfs/"+pdf_file) 
        st.caption("(Pdf is two column)") if two_col else st.caption("(Pdf is single column)")
        st.write("---")

        for page in components.extractPdfText("../pdfs/"+pdf_file):
            st.write(page)
    """
    elif method == "Determine best training setting":

        #####################
        MIN_TRAINING = 40   
        MAX_TRAINING = 200  
        TABLE_TOP_X = 10
        #####################

        classifier_type = st.selectbox("Select Classifier type", ["event", "indicator", "activity", "metric"])

        shuffler = st.checkbox("Shuffle labeled literature?", value=True)
        if st.button("🎲 Reshuffle!", disabled=not shuffler):
            st.experimental_rerun()

        training_results = []

        for labeled_lit_file in components.getLabeledFiles(label_types=[classifier_type], out_type="list"):
            with open(labeled_lit_file, "rb") as file:
                labeled_literature = pickle.load(file)
                random.shuffle(labeled_literature) if shuffler else None
            for i in range(len(labeled_literature)):
                if i == 0 or i > MAX_TRAINING or i < MIN_TRAINING: continue
                train_set, test_set = labeled_literature[:i], labeled_literature[i:]
                classifier = nltk.NaiveBayesClassifier.train(train_set)
                accuracy = round(nltk.classify.accuracy(classifier, test_set), 2)

                training_results.append({"Removed Stopwords":labeled_lit_file.split("_")[-2] == "rmsw",
                                         "Stemming Algo":labeled_lit_file.split("_")[-1], 
                                         "Train data":i, 
                                         "Test data":len(labeled_literature)-i,
                                         "Accuracy":accuracy})
        
        st.write(f"Stemming Algorithms: {components.STEMMING_ALGOS}")
        st.write(f"Found {len(components.LABELED_LIT_FILES)} labeled literature")
    
        st.subheader(f"Top {TABLE_TOP_X} Training Settings")
        st.caption(f"With between {MIN_TRAINING} and {MAX_TRAINING} labeled literature used for training!")
        # hide table row index
        #st.markdown("<style>tbody th {display:none} .blank {display:none}</style> ", unsafe_allow_html=True)
        st.table(sorted(training_results, key=lambda x: x["Accuracy"], reverse=True)[:TABLE_TOP_X])
    """
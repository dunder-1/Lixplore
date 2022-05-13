import nltk
import os
from . import *

LABEL_TYPES = ["event", "activity", "indicator", "metric"]
STEMMING_ALGOS = ["PorterStemmer", "WordNetLemmatizer"]
STOPWORDS = set(nltk.corpus.stopwords.words("english"))

CLASSIFIER_FILES = [i.split(".")[0] for i in os.listdir("../classifier/") if i.startswith("classifier")]
LABELED_LIT_FILES = [i.split(".")[0] for i in os.listdir("../classifier/") if i.startswith("labeled_literature")]

def getLabeledFiles(label_types=LABEL_TYPES, out_type="dict"):
    _ = {} if out_type == "dict" else []
    for label_type in LABEL_TYPES:
        if out_type == "dict":
            _[label_type] = [f"../classifier/{label_type}/"+file_name for file_name in os.listdir(f"../classifier/{label_type}/") if file_name.startswith("labeled_literature")]
        else:
            _.extend([f"../classifier/{label_type}/"+file_name for file_name in os.listdir(f"../classifier/{label_type}/") if file_name.startswith("labeled_literature")])
    return _


def filterDataByCitation(data, citation, label_type):
    # label_type = "Event", "Activity", "Indicator", "Metric"
    return set([i[label_type] for i in data if i["citation"] == citation])

def labelText(pdf_file, data, label_type, remove_stopwords=True, stemming_algo=STEMMING_ALGOS[0]):
    # label_type = "Event", "Activity", "Indicator", "Metric"

    pages = preprocess.extractPdfText(pdf_file)
    filtered_pages = filterPages(pages, remove_stopwords, stemming_algo)
    pages = {"pages":" ".join(filtered_pages)}
    labeled_text = [(pages, label) for label in filterDataByCitation(data, pdf_file[8:].split()[0], label_type)]
    return labeled_text

def labelExtractedText(file_name, data, label_type, remove_stopwords, stemming_algo):
    with open(file_name, "r", encoding="utf-8") as file:
        filtered_text = filterText(file.read(), remove_stopwords, stemming_algo)
        return [({"text": filtered_text}, label) for label in filterDataByCitation(data, file_name[23:].split()[0], label_type)]


def tagToWordNetTag(tag):
    mappy = {"J":"a", "V":"v", "R":"r", "N":"n"}
    return mappy[tag[0]] if tag[0] in mappy else "n"

def filterText(text, remove_stopwords=True, stemming_algo="PorterStemmer"):

    word_tokens = nltk.tokenize.word_tokenize(text)

    if stemming_algo == "PorterStemmer":
        if remove_stopwords:
            filtered_page = [nltk.stem.PorterStemmer().stem(w) for w in word_tokens if w.lower() not in STOPWORDS]
        else:
            filtered_page = [nltk.stem.PorterStemmer().stem(w) for w in word_tokens]
    
    elif stemming_algo == "WordNetLemmatizer":
        tagged_tokens = nltk.pos_tag(word_tokens)
        if remove_stopwords:
            filtered_page = [nltk.stem.WordNetLemmatizer().lemmatize(w, pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens if w.lower() not in STOPWORDS]
        else:
            filtered_page = [nltk.stem.WordNetLemmatizer().lemmatize(w, pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens]        
    
    else:
        if remove_stopwords:
            filtered_page = [w.lower() for w in word_tokens if w.lower() not in STOPWORDS]
        else:
            filtered_page = [w.lower() for w in word_tokens]

    return " ".join(filtered_page)

def filterPages(page_list, out_type=str, remove_stopwords=True, stemming_algo=nltk.stem.PorterStemmer()):
    filtered_pages = [filterText(p, remove_stopwords, stemming_algo) for p in page_list]
    if out_type == list:
        return filtered_pages
    return " ".join(filtered_pages)
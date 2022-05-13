import os, pickle
from . import preprocess, train

CLASSIFIER_TYPES = ["event", "activity", "indicator", "metric"]

def loadClassifier(classifier_file):

    remove_stopwords = classifier_file.split("_")[1] == "rmsw"
    stemming_algo = classifier_file.split("_")[2]

    with open(classifier_file, "rb") as file:
        return (pickle.load(file), remove_stopwords, stemming_algo)


def getClassifierFiles(classifier_types=CLASSIFIER_TYPES, out_type="dict"):
    _ = {} if out_type == "dict" else []
    for classifier_type in CLASSIFIER_TYPES:
        if out_type == "dict":
            _[classifier_type] = [f"../classifier/{classifier_type}/"+file_name for file_name in os.listdir(f"../classifier/{classifier_type}/") if file_name.startswith("classifier")]
        else:
            _.extend([f"../classifier/{classifier_type}/"+file_name for file_name in os.listdir(f"../classifier/{classifier_type}/") if file_name.startswith("classifier")])
    return _

def getBestClassifer():

    _ = {}
    for classifier_type in getClassifierFiles():
        best_classifer, accuracy = None, 0
        for classifier in getClassifierFiles()[classifier_type]:
            if int(classifier.split("_")[-1].split(".")[0]) >= accuracy:
                best_classifer = classifier
                accuracy = int(classifier.split("_")[-1].split(".")[0])

        _[classifier_type] = best_classifer

    return _


def classifyPDF(classifier, remove_stopwords, stemming_algo, pdf_file):
    pages = preprocess.extractPdfText(pdf_file)
    return (classifier.classify({"pages":train.filterPages(pages, remove_stopwords, stemming_algo)}), pages)
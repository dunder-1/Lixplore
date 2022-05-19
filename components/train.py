import nltk
import os
from . import *
from dataclasses import dataclass

LABEL_TYPES = ["event", "activity", "indicator", "metric"]
STEMMING_ALGOS = ["PorterStemmer", "WordNetLemmatizer"]

@dataclass
class LabeledText:
    """Represents the features and labels"""
    features: dict[str, bool] # the features of the text
    label: str                # a label for the literature

    def asTuple(self) -> tuple:
        return (self.features, self.label)

def getLabels(data:list[dict], citation:str, label_type:str) -> set:
    """Helper function that returns all labels for a specific literature (according to 'citation')"""
    return set([i[label_type] for i in data if i["citation"] == citation])

def setFeatures(word_tokens:list[str], most_common_features:list[list]) -> dict[str, bool]:
    """
    Determines for all most common feature if it exists in the passed word tokens or not.

    :param word_tokens: list of tokens
    :param most_common_features: the most common features of all documents (result of preprocess.getMostCommonFeatures())

    :return: a dictionary with structure e.g. {"contains(feature_0)":True, "contains(feature_1)":False, ...}
    """

    word_tokens = set(word_tokens)
    features = {}
    for word, count in most_common_features:
        features[f"contains({word})"] = word in word_tokens
    return features

@dataclass
class LabeledLiteratureFile:
    """Represents a file containing all labeled literature"""
    path: str                # path to file
    label_type: str          # what kind of label is used (one of ["event", "activity", "indicator", "metric"])
    remove_stopwords: bool   # True if stopwords are removed
    stemming_algo: str       # the chosen stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    extra_removal: list[str] # additional strings that will be removed
    labeled_literature: list[LabeledText] # list with labeled literature (1 element = 1 (literature+label))

    def assignLiterature(self, pdf_file:PdfFile, data:list[dict], most_common_features:list[str]):
        """
        Determines the features of a pdf text and assigns a LabeledText object to self.labeled_literature

        :param pdf_file: PdfFile object
        :param data: the database (return of util.transformData(util.readRawData()))
        :param most_common_features: the most common features of all documents (result of preprocess.getMostCommonFeatures())

        :return: None
        """

        features = setFeatures(getFilteredWordTokens(pdf_file.extracted_pages, 
                                                     self.remove_stopwords, 
                                                     self.stemming_algo, 
                                                     self.extra_removal), 
                               most_common_features)
        label_list = getLabels(data, citation=pdf_file.citation, label_type=self.label_type)
        for label in label_list:
            self.labeled_literature.append(LabeledText(features=features, label=label))



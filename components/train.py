import nltk
import os
from . import *
from dataclasses import dataclass

LABEL_TYPES = ["event", "activity", "indicator", "metric"]
STEMMING_ALGOS = ["PorterStemmer", "WordNetLemmatizer"]

@dataclass
class LabeledText:
    """Represents the extracted and filtered pages"""
    pages: list[str]    # the extracted & filtered pages of the literature
    label: str          # a label for the literature

    @classmethod
    def fromPdfFile(cls, pdf_file:PdfFile, label:str, remove_stopwords:bool, stemming_algo:str):
        """
        Filters the pages of pdf_file and finally constructs a LabeledText object.

        :param pdf_file: a PdfFile object representing the literature
        :param label: the label that will be set for this literature
        :param remove_stopwords: is True if stopwords should be removed
        :param stemming_algo: the chosen stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
        """
        return cls(pages=pdf_file.filterPages(remove_stopwords, stemming_algo), 
                   label=label)

    def asTuple(self):
        """Formats the instance to a tuple (used for training)"""
        return ({"text":" ".join(self.pages)}, self.label)

def getLabeledTexts(pdf_file: PdfFile, data:list[dict], label_type:str, remove_stopwords:bool, stemming_algo:str) -> list[tuple]:
    """
    Creates a list of LabeledText objects (as tuples!) by the passed label_type 

    :param pdf_file: a PdfFile object representing the literature
    :param data: the dataset in the transformed format (see util.transformData())
    :param label_type: type of label that should be accessed (one of ["event", "activity", "indicator", "metric"])
    :param remove_stopwords: is True if stopwords should be removed
    :param stemming_algo: the chosen stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    
    :return: a list of tuples for training 
    """
    labels_by_citation = getLabels(data, pdf_file.citation, label_type)
    return [LabeledText.fromPdfFile(pdf_file, label, remove_stopwords, stemming_algo).asTuple() for label in labels_by_citation]

def getLabels(data:list[dict], citation:str, label_type:str) -> set:
    """Helper function that returns all labels for a specific literature (according to 'citation')"""
    return set([i[label_type] for i in data if i["citation"] == citation])

@dataclass
class LabeledLiteratureFile:
    """Represents a file containing all labeled literature"""
    path: str               # path to file
    label_type: str         # what kind of label is used (one of ["event", "activity", "indicator", "metric"])
    remove_stopwords: bool  # True if stopwords are removed
    stemming_algo: str      # the chosen stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    labeled_literature: list[LabeledText] # list with labeled literature (1 element = 1 (literature+label))




from nltk import NaiveBayesClassifier
from nltk import classify
from . import *
import pickle, random
from dataclasses import dataclass

@dataclass
class ClassifierFile:
    """Represents a classifier file with all the necessary information"""
    path: str                # path to file
    label_type: str          # what kind of label is used (one of ["event", "activity", "indicator", "metric"])
    remove_stopwords: bool   # True if stopwords are removed
    stemming_algo: str       # the chosen stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    extra_removal: list[str] # additional strings that will be removed
    classifier: NaiveBayesClassifier # the trained classifier
    train_test_split: int    # % of texts that are used for training (100-train_test_split for testing)
    accuracy: float          # accuracy of the trained classifier (rounded to 2 decimals)

    @classmethod
    def fromLabeledLiteratureFile(cls, lab_lit:LabeledLiteratureFile, train_test_split:int):
        """
        Trains a nltk.NaiveBayesClassifier by splitting the data into train & test data and calculates accuracy

        :param lab_lit: a LabeledLiteratureFile with all the necessary data
        :param train_test_split: % of texts that are used for training (100-train_test_split % for testing)
        """
        
        feature_set = [i.asTuple() for i in lab_lit.labeled_literature]


        random.shuffle(feature_set)

        def splitList(l:list, split:int):
            """Splits list into two by param split"""
            return l[:split*len(l)//100], l[split*len(l)//100:]

        train_set, test_set = splitList(feature_set, train_test_split)
        classifier = NaiveBayesClassifier.train(train_set)
        accuracy = round(classify.accuracy(classifier, test_set), 2)

        return cls(path=f"../classifier/{lab_lit.label_type}_classifier.pickle",
                   classifier=classifier, 
                   label_type=lab_lit.label_type, 
                   remove_stopwords=lab_lit.remove_stopwords, 
                   stemming_algo=lab_lit.stemming_algo,
                   extra_removal=lab_lit.extra_removal, 
                   train_test_split=train_test_split, 
                   accuracy=accuracy)

    def classifyPDF(self, pdf_path: str, most_common_features:list[str]) -> dict:
        """
        Classifies a pdf by creating a PdfFile object
        
        :param pdf_path: string that represents path to file OR BytesIO object
        
        :return: A probability distribution for all labels
        """
        pdf_file = PdfFile.read(pdf_path)
        features = setFeatures(getFilteredWordTokens(pdf_file.extracted_pages, 
                                                     self.remove_stopwords, 
                                                     self.stemming_algo, 
                                                     self.extra_removal), 
                               most_common_features)

        return self.classifier.prob_classify(features)

    def asDictTable(self) -> dict:
        """Returns a dictionary representation of the relevant infos"""
        return {
            "label_type": self.label_type,
            "remove_stopwords": self.remove_stopwords,
            "stemming_algo": self.stemming_algo,
            "train_test_split": self.train_test_split,
            "accuracy": self.accuracy
        }

def loadClassifier(label_type:str) -> ClassifierFile:
    """Loads a trained classifier according to the label_type (one of ["event", "activity", "indicator", "metric"])"""
    if label_type == "*":
        return [loadClassifier(i) for i in LABEL_TYPES]

    with open(f"../classifier/{label_type}_classifier.pickle", "rb") as file:
        return pickle.load(file)
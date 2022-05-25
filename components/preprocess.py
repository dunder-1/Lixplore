import pdfplumber
from nltk import pos_tag, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
from dataclasses import dataclass

STOPWORDS = set(stopwords.words("english"))
PUNCTUATION = {",", ".", "(", ")", "[", "]", "’", ":", "%", "*", "&", "?", "!", ";", "@"}
DIGITS = {str(i) for i in range(10)}
TRASH = PUNCTUATION.union(DIGITS)

@dataclass
class PdfFile:
    """Represents the pdf file and its extracted text"""
    path: str                   # path to pdf file
    citation: str               # citation nr e.g. [52]
    extracted_pages: list[str]  # list of pages with extracted text
    is_two_column: bool         # True if file is in two column format

    def __repr__(self):
        return f"PdfFile(citation={self.citation}, is_two_column={self.is_two_column})"

    @classmethod
    def read(cls, file_path:str):
        """
        Constructs a PdfFile object by file_path.

        :param file_path: string that represents path to file (OR BytesIO object)

        :return: PdfFile object 
        """
        citation = cls.getCitation(file_path) if isinstance(file_path, str) else ""

        with pdfplumber.open(file_path) as pdf:

            out_pages = []
            page = pdf.pages[0]
            is_two_column = page.crop((0.49 * page.width, 0.5 * page.height, 0.5 * page.width, 0.51 * page.height)).extract_text() == ""

            # pdf is two-column
            if is_two_column:
                for page in pdf.pages:
                    left = page.crop((0, 0, 0.5 * page.width, page.height))
                    right = page.crop((0.5 * page.width, 0, page.width, page.height))
                    out_pages.append(left.extract_text(x_tolerance=1) + " " + right.extract_text(x_tolerance=1))
            
            # pdf is single-column
            else:
                for page in pdf.pages:
                    out_pages.append(page.extract_text(x_tolerance=1))

        return cls(path=file_path,
                   citation=citation, 
                   extracted_pages=out_pages,
                   is_two_column=is_two_column)

    @staticmethod
    def getCitation(file_path:str) -> str:
        """Returns the citation nr of a file path"""
        return re.findall(r"\[[\d]*\]", file_path).pop()


def getFilteredWordTokens(pages:list[str], remove_stopwords:bool, stemming_algo:str, extra_removal:list) -> list[str]:
    """
    Filters words of pages according to the passed configuration parameters


    :param pages: list that represents the extracted text (e.g. PdfFile().extracted_pages)
    :param remove_stopwords: True if stopwords should be removed
    :param stemming_algo: the stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    :param extra_removal: additional strings that will be removed

    :return: a list of word tokens filtered & stemmed by the configuration parameters
    """
    def tagToWordNetTag(tag:str):
        """Helper function for correct part of speech tagging"""
        mappy = {"J":"a", "V":"v", "R":"r", "N":"n"}
        return mappy[tag[0]] if tag[0] in mappy else "n"

    for page in pages:
        word_tokens = word_tokenize(page)

        if stemming_algo == "PorterStemmer":
            if remove_stopwords:
                return [PorterStemmer().stem(w.lower()) for w in word_tokens if w.lower() not in STOPWORDS and w.lower() not in extra_removal]
            else:
                return [PorterStemmer().stem(w.lower()) for w in word_tokens if w.lower() not in extra_removal]

        elif stemming_algo == "WordNetLemmatizer":
            tagged_tokens = pos_tag(word_tokens)
            if remove_stopwords:
                return [WordNetLemmatizer().lemmatize(w.lower(), pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens if w.lower() not in STOPWORDS and w.lower() not in extra_removal]
            else:
                return [WordNetLemmatizer().lemmatize(w.lower(), pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens if w.lower() not in extra_removal]

        else:
            if remove_stopwords:
                return [w.lower() for w, tag in word_tokens if w.lower() not in STOPWORDS and w.lower() not in extra_removal]
            else:
                return [w.lower() for w, tag in word_tokens if w.lower() not in extra_removal]



def getMostCommonFeatures(pdf_files: list[PdfFile], method="bow", cut_off=500, remove_stopwords=True, stemming_algo="PorterStemmer", extra_removal=TRASH) -> list[list]:
    """
    Determine the most common features of all pdf files by using a passed method and cut off

    :param pdf_files: list of extracted PdfFile objects
    :param method: the used calculation method (one of ["bow"])
    :param cut_off: return how many features
    :param remove_stopwords: True if stopwords should be removed
    :param stemming_algo: the stemming algorithm (one of ["PorterStemmer", "WordNetLemmatizer"])
    :param extra_removal: additional strings that will be removed

    :return: a list with the most common features (each element is list with [feature, count])
    """

    if method == "bow":
        all_words = []
        for pdf_file in pdf_files:
            all_words.extend([w for w in getFilteredWordTokens(pdf_file.extracted_pages, remove_stopwords, stemming_algo, extra_removal)])
        
        word_features = FreqDist(w for w in all_words).most_common()[:cut_off]

    return word_features

        
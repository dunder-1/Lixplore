import pdfplumber
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
from dataclasses import dataclass

STOPWORDS = set(stopwords.words("english"))

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

    def filterPages(self, remove_stopwords:bool, stemming_algo:str) -> list[str]:
        """
        Filters the text of self.extracted_pages according to the parameters

        :param remove_stopwords: removes stop words if True
        :param stemming_algo: stems every word according to the passed stemmer

        :return: the filtered pages
        """
        def tagToWordNetTag(tag:str):
            mappy = {"J":"a", "V":"v", "R":"r", "N":"n"}
            return mappy[tag[0]] if tag[0] in mappy else "n"

        filtered_pages = []

        for page_text in self.extracted_pages:

            word_tokens = word_tokenize(page_text)

            if stemming_algo == "PorterStemmer":
                if remove_stopwords:
                    filtered_page = [PorterStemmer().stem(w.lower()) for w in word_tokens if w.lower() not in STOPWORDS]
                else:
                    filtered_page = [PorterStemmer().stem(w.lower()) for w in word_tokens]
            
            elif stemming_algo == "WordNetLemmatizer":
                tagged_tokens = pos_tag(word_tokens)
                if remove_stopwords:
                    filtered_page = [WordNetLemmatizer().lemmatize(w.lower(), pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens if w.lower() not in STOPWORDS]
                else:
                    filtered_page = [WordNetLemmatizer().lemmatize(w.lower(), pos=tagToWordNetTag(tag)) for w, tag in tagged_tokens]        
            
            else:
                if remove_stopwords:
                    filtered_page = [w.lower() for w in word_tokens if w.lower() not in STOPWORDS]
                else:
                    filtered_page = [w.lower() for w in word_tokens]

            filtered_pages.append(" ".join(filtered_page))

        return filtered_pages

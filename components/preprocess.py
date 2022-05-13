import pdfplumber
import os, json, re

# data.json
def readRawData():
    with open("../data.json", encoding="utf-8") as file:
        return json.load(file)

def transformData(data):
    out_data = []

    for event in data:
        for activity in event["LearningActivities"]:
            for indicator in activity["indicator"]:

                citation = set(re.findall(r"\[[\d]*\]", indicator["indicatorName"])).pop()
                
                metrics = [m.replace(citation[:-1], "").strip() for m in indicator["metrics"].split("],")]
                metrics[-1] = metrics[-1][:-1].strip()
                
                for metric in metrics:

                    out_data.append({
                            "event": event["LearningEvents"],
                            "activity": activity["Name"],
                            "indicator": indicator["indicatorName"],
                            "metric": metric,
                            "citation": citation
                        })

    return out_data


# pdf files
def getPdfFiles():
    return ["../pdfs/"+file_name for file_name in os.listdir("../pdfs/") if file_name[-3:] == "pdf"]

def getExtractedFiles():
    return ["../pdfs/extracted_text/"+file_name for file_name in os.listdir("../pdfs/extracted_text/") if file_name[-3:] == "txt"]

def isPdfTwoColumn(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        page = pdf.pages[0]
        return page.crop((0.49 * page.width, 0.5 * page.height, 0.5 * page.width, 0.51 * page.height)).extract_text() == ""

def extractPdfText(pdf_file_path):

    with pdfplumber.open(pdf_file_path) as pdf:

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

        return out_pages


# rest
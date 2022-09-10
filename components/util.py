import os, json, re, pickle

def loadFiles(folder:str, extension:str, open_pickle=False) -> list[str]:
    """Loads all files found in 'folder' ending with 'extension'
    
    :param folder: e.g. "../pdfs/" or "../pdfs/extracted_text/"
    
    :return: a list with all the matching files
    """
    if open_pickle:
        _ = []
        for file_name in os.listdir(folder):
            if file_name.endswith(extension):
                with open(folder+file_name, "rb") as file:
                    _.append(pickle.load(file))
        return _
        
    return [folder+file_name for file_name in os.listdir(folder) if file_name.endswith(extension)]


def readRawData():
    """Opens the data file as dict"""
    with open("../data.json", encoding="utf-8") as file:
        return json.load(file)

def transformData(data):
    """Reformats the data into a more table-like format and adds the citation nr
    
    Example:
    
        This:
        
            {
                "LearningEvents": "Create", 
                "LearningActivities": {
                    "Name": "Design",
                    "indicator": [
                        {
                            "indicatorName": "Course Assessments [55]",
                            "metrics": "Number of Students [55],..."
                        }
                    ]
                }
            },
            ...

        becomes:

            [
                {
                    "event": "Create", 
                    "activity": "Design", 
                    "indicator:", "Course Assessments [55]", 
                    "metric": "Number of Students [55]"
                    "citation": "[55]"
                },
                ...
            ]
    """

    out_data = []
    for event in data:
        for activity in event["LearningActivities"]:
            for indicator in activity["indicator"]:

                citation = set(re.findall(r"\[[\d]*\]", indicator["indicatorName"])).pop()
                
                metrics = [m.replace(citation[:-1], "").strip() for m in indicator["metrics"].split("],")]
                metrics[-1] = metrics[-1][:-1].strip()
                
                #_indicator = indicator["indicatorName"].replace(citation, ",")[:-1] 
                _indicator = [i.strip() for i in indicator["indicatorName"].split(citation) if i != ""]
                _indicator = ", ".join(_indicator)

                for metric in metrics:

                    out_data.append({
                            "event": event["LearningEvents"].lower(),
                            "activity": activity["Name"].lower(),
                            "indicator": _indicator.lower(),
                            "metric": metric.lower(),
                            "citation": citation
                        })

    return out_data
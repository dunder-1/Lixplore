import nltk
import components
import os, pickle, random, csv

CONFIG = {
    "extract_pdf": False,
    "label_text": False,
    "run_training": True,
}

PDF_FILES = components.getPdfFiles()
EXTRACTED_FILES = components.getExtractedFiles()
LABELED_FILES = components.getLabeledFiles()
DATA = components.transformData(components.readRawData())

if __name__ == '__main__':

    if CONFIG["extract_pdf"]:

        folder_extracted_text = "../pdfs/extracted_text/"
        for i, pdf_file in enumerate(PDF_FILES, start=1):
            print(f"extracting PDF '{pdf_file[8:]}' ({i} of {len(PDF_FILES)})...")
            with open(folder_extracted_text+pdf_file[8:-4]+".txt", "w", encoding="utf-8") as file:
                file.write(" ".join(components.extractPdfText(pdf_file)))

    if CONFIG["label_text"]:

        for label_type in components.LABEL_TYPES:
            for remove_stopwords in [True, False]:
                for stemming_algo in components.STEMMING_ALGOS:
                    label_config = {"label_type": label_type, "remove_stopwords": remove_stopwords, "stemming_algo": stemming_algo}
                    print(f"labeling all {len(EXTRACTED_FILES)} files with config = {label_config} ...")
                    labeled_literature = []
                    for txt_file in EXTRACTED_FILES:
                        labeled_text = components.labelExtractedText(txt_file, DATA, label_type, remove_stopwords, stemming_algo)
                        labeled_literature.extend(labeled_text)
                    rmsw = "rmsw" if remove_stopwords else "sw"
                    with open(f"../classifier/{label_type}/labeled_literature_{rmsw}_{stemming_algo}.pickle", "wb") as file:
                        pickle.dump(labeled_literature, file)
    
    if CONFIG["run_training"]:

        results = [("Label type", "Removed Stopwords", "Stemming Algorithm", "Train/Test split in %", "Accuracy")]
        for labeled_file in LABELED_FILES:
            for elem in LABELED_FILES[labeled_file]:
                for train_test_split in range(20, 100, 20):
                    with open(elem, "rb") as file:
                        labeled_literature = pickle.load(file)
                    
                    random.shuffle(labeled_literature)
                    train_set, test_set = labeled_literature[:train_test_split], labeled_literature[train_test_split:]
                    classifier = nltk.NaiveBayesClassifier.train(train_set)
                    accuracy = round(nltk.classify.accuracy(classifier, test_set), 2)

                    ######################################################
                    label_type = elem.split("/")[2]
                    filename_infos = elem.split("/")[3].split("_")
                    rmsw = "yes" if filename_infos[2] == "rmsw" else "no"
                    stemming_algo = filename_infos[3].split(".")[0]
                    if accuracy > 0.1:
                        results.append((label_type, rmsw, stemming_algo, f"{train_test_split}/{100-train_test_split}", accuracy))
                    ######################################################

                    print(f"Trained classifier from {elem} with accuracy {accuracy}")
                    classifier_file = elem.replace("labeled_literature", "classifier")[:-7] + f"_{train_test_split}_{100-train_test_split}"
                    with open(classifier_file + ".pickle", "wb") as file:
                        pickle.dump(classifier, file)



        with open("results.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(results)










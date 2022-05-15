# 🔍 Lixplore

This Tool offers the possibility to automatically:
- read literature from pdf
- identify key words from text
- categorize the text based on key words

### ⚠ Required structure

This project requires the following folder structure. The folder pdfs should contain all the pdfs with `[nr] ` as prefix. The data.json file should be in the main folder. 

```bash
main
+-- Lixplore Repo
+-- pdfs
	[1] foo.pdf
	[69] bar.pdf
	...
	+-- extracted_text
+-- classifier
	+-- event
	+-- activity
	+-- indicator
	+-- metric
data.json
```

### ⚙ Technology

Python `3.10.1`

pdfplumber `0.6.2`
streamlit `1.5.0`
nltk `3.7`


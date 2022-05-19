# 🔍 Lixplore

This Tool offers the possibility to automatically:
- read literature from pdf
- identify key words from text
- categorize the text based on key words

## Getting Started

1. The first step is to create the project folder. The name is not important therefore you can name it as you like. I will use the name `main`.

   - In the main folder you have to create a folder `pdfs` with a subfolder `extracted text`.
   - In the main folder you have to create a folder `classifier` with subfolders `event`, `activity`, `indicator` and `metric`.

2. Now put the files into the correct location:

   - The pdf files have to be inside the folder `main/pdfs/` and **need the correct structure with the citation nr in square brackets in front and a whitespace after it (e.g. [42] xyz.pdf)!** This is very important otherwise the training can't be done correctly.
   - The `data.json` file has to be inside the folder `main/`.

3. Now you can clone the repository into a subfolder e.g. `Lixplore` by 

   ```bash
   git clone git@github.com:dunder-1/Lixplore.git
   ```

4. When you're done with first 3 steps your project structure will look like this:

```bash
main
+-- Lixplore
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

5. Navigate into the repository and install the necessary libraries:

   ````bash
   pip install -r requirements.txt
   ````

6. Run the streamlit application:

   `````bash
   streamlit run app.py
   `````

If done correctly your browser should automatically run and navigate to `http://localhost:8501/?page=start` (if not then you can do it manually).

Now you should see this page:

![image-20220519121811141](/img/tut_landing_page.png)

## Train a classifier

To train a classifier click on `Exercise` in the navigation bar on the left. You should see this page:

![image-20220519122304588](/img/tut_training.png)

There you have three checkboxes:

- Extract text: This will read the pdf files (in `main/pdfs/`), extract their texts and save them into `main/pdfs/extracted_text/` as pickle files
- Label text: This will access the previously extracted texts (in `main/pdfs/extracted_text/`) and assign a label on every text. After that, all the labeled files are saved according to the label type (e.g. `main/classifier/event/` for label type `event`).
  - You can choose different setups here (generally you get best results by checking `Remove Stopwords?` and selecting `PorterStemmer`)
  - For label types please select all four!
- Run Training: This will run a training by accessing the labeled literature and *learning* how the features and the labels correlate.
  - You can choose different types of labels to train. **Attention:** Training a classifier is a complex task and therefore might take a while (especially when training a `metric`-classifier, it might take up to 30 minutes!) 



#### Next steps

Please do the following tasks:

1. Check both `Extract text` and `Label text` and click on `Start`:

![image-20220519123814125](/img/tut_labeling.png)

2. After this is finished, click on `Run Training` (you have to uncheck the other two options first), choose `event` and click on start:

![image-20220519124634520](/img/tut_run_training.png)

3. Now rerun step 2 again for every other label type (`metric` might take up to 30 minutes!)

🎉 Congratulations! You have trained 4 different classifiers and can now predict `events`, `activities`, `indicators` and even `metrics` of new pdfs!

## Predict labels of new pdf files

Choose `Extract` in the navigation bar and you should be see this screen:

![image-20220519124429056](/img/tut_predict.png)

To predict labels of new pdf files:

1. choose `Upload PDF` and either by drag and drop  `Browse files`. You should see an information below the upload area  about the uploaded file.
2. Now select all the label types you want to extract.
3. Click on Extract. 

Your output should look like this (Depends on what you chose in step 2):

![image-20220519125119392](/img/tut_extraction_output.png)

This shows the most probable label with a prediction value. This number represents the distance of the assigned label to the learned feature-label pairs of the classifier. Therefore a value closer to 0.0 is better. The cut off here is -45.0 to provide a variety of different labels.

## Misc

Choose `Examine` to dive into the data and see some interesting statistics. 

## ⚙ Technology

Python `3.10.1`

pdfplumber `0.6.2`
streamlit `1.5.0`
nltk `3.7`

